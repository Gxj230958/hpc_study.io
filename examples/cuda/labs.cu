#include <cuda_runtime.h>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>

#define CUDA(call) do { cudaError_t e = (call); if (e != cudaSuccess) { \
    std::fprintf(stderr, "%s:%d %s\n", __FILE__, __LINE__, cudaGetErrorString(e)); \
    std::exit(2); } } while (0)

__global__ void add(const float *a, const float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}

__global__ void reduce(const float *a, float *partial, int n) {
    __shared__ float tile[256];
    int t = threadIdx.x, i = blockIdx.x * blockDim.x + t;
    tile[t] = i < n ? a[i] : 0.0f;
    __syncthreads();
    for (int step = blockDim.x / 2; step; step /= 2) {
        if (t < step) tile[t] += tile[t + step];
        __syncthreads();
    }
    if (t == 0) partial[blockIdx.x] = tile[0];
}

__global__ void matmul(const float *a, const float *b, float *c, int n) {
    __shared__ float as[16][16], bs[16][16];
    int x = threadIdx.x, y = threadIdx.y;
    int row = blockIdx.y * 16 + y, col = blockIdx.x * 16 + x;
    float sum = 0.0f;
    for (int k = 0; k < n; k += 16) {
        as[y][x] = row < n && k+x < n ? a[row*n+k+x] : 0;
        bs[y][x] = k+y < n && col < n ? b[(k+y)*n+col] : 0;
        __syncthreads();
        for (int j = 0; j < 16; ++j) sum += as[y][j] * bs[j][x];
        __syncthreads();
    }
    if (row < n && col < n) c[row*n+col] = sum;
}

void vectors(int n) {
    std::vector<float> a(n), b(n), c(n);
    for (int i = 0; i < n; ++i) { a[i] = (i % 17) * 0.125f; b[i] = (i % 13) * 0.25f; }
    float *da, *db, *dc, *dp;
    size_t bytes = size_t(n) * sizeof(float);
    int blocks = (n+255)/256;
    CUDA(cudaMalloc(&da, bytes)); CUDA(cudaMalloc(&db, bytes)); CUDA(cudaMalloc(&dc, bytes));
    CUDA(cudaMalloc(&dp, blocks*sizeof(float)));
    auto start = std::chrono::steady_clock::now();
    CUDA(cudaMemcpy(da, a.data(), bytes, cudaMemcpyHostToDevice));
    CUDA(cudaMemcpy(db, b.data(), bytes, cudaMemcpyHostToDevice));
    add<<<blocks,256>>>(da,db,dc,n);
    CUDA(cudaGetLastError());
    CUDA(cudaMemcpy(c.data(), dc, bytes, cudaMemcpyDeviceToHost));
    double end_to_end_ms = std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-start).count();
    for (int i = 0; i < n; ++i) if (c[i] != a[i]+b[i]) std::exit(1);
    for (int i = 0; i < 5; ++i) add<<<blocks,256>>>(da,db,dc,n);
    CUDA(cudaGetLastError()); CUDA(cudaDeviceSynchronize());
    cudaEvent_t begin, end;
    CUDA(cudaEventCreate(&begin)); CUDA(cudaEventCreate(&end));
    std::vector<float> times;
    for (int r = 0; r < 20; ++r) {
        CUDA(cudaEventRecord(begin));
        for (int i = 0; i < 100; ++i) add<<<blocks,256>>>(da,db,dc,n);
        CUDA(cudaGetLastError()); CUDA(cudaEventRecord(end)); CUDA(cudaEventSynchronize(end));
        float ms; CUDA(cudaEventElapsedTime(&ms,begin,end)); times.push_back(ms/100);
    }
    std::printf("vector n=%d kernel_samples_ms=[", n);
    for (size_t i = 0; i < times.size(); ++i)
        std::printf("%s%.6f", i ? "," : "", times[i]);
    std::printf("]\n");
    std::sort(times.begin(), times.end());
    reduce<<<blocks,256>>>(da,dp,n);
    CUDA(cudaGetLastError());
    std::vector<float> partial(blocks);
    CUDA(cudaMemcpy(partial.data(), dp, blocks*sizeof(float), cudaMemcpyDeviceToHost));
    double actual = 0, expected = 0;
    for (float x: partial) actual += x;
    for (float x: a) expected += x;
    if (!std::isfinite(actual) || !std::isfinite(expected) ||
        std::abs(actual-expected) > 1e-5 * std::max(1.0,std::abs(expected))) std::exit(1);
    std::printf("vector n=%d kernel_median_ms=%.6f first_transfer_and_kernel_ms=%.6f reduction_error=%.6g PASS\n",
                n,(times[9]+times[10])/2,end_to_end_ms,std::abs(actual-expected));
    CUDA(cudaEventDestroy(begin)); CUDA(cudaEventDestroy(end));
    CUDA(cudaFree(da)); CUDA(cudaFree(db)); CUDA(cudaFree(dc)); CUDA(cudaFree(dp));
}

void matrices(int n) {
    std::vector<float> a(n*n), b(n*n), c(n*n);
    for (int i=0; i<n*n; ++i) { a[i] = (i%7-3)*0.125f; b[i] = (i%11-5)*0.0625f; }
    float *da, *db, *dc;
    size_t bytes = a.size()*sizeof(float);
    CUDA(cudaMalloc(&da,bytes)); CUDA(cudaMalloc(&db,bytes)); CUDA(cudaMalloc(&dc,bytes));
    CUDA(cudaMemcpy(da,a.data(),bytes,cudaMemcpyHostToDevice));
    CUDA(cudaMemcpy(db,b.data(),bytes,cudaMemcpyHostToDevice));
    matmul<<<dim3((n+15)/16,(n+15)/16),dim3(16,16)>>>(da,db,dc,n);
    CUDA(cudaGetLastError()); CUDA(cudaMemcpy(c.data(),dc,bytes,cudaMemcpyDeviceToHost));
    double error=0;
    for(int r=0;r<n;++r) for(int col=0;col<n;++col) {
        double expected=0;
        for(int k=0;k<n;++k) expected+=double(a[r*n+k])*b[k*n+col];
        if (!std::isfinite(c[r*n+col]) || !std::isfinite(expected)) std::exit(1);
        error=std::max(error,std::abs(c[r*n+col]-expected));
    }
    if(error>1e-4) std::exit(1);
    std::printf("matmul n=%d max_abs_error=%.6g PASS\n",n,error);
    CUDA(cudaFree(da)); CUDA(cudaFree(db)); CUDA(cudaFree(dc));
}

int main() {
    cudaDeviceProp prop; CUDA(cudaGetDeviceProperties(&prop,0));
    std::printf("device=%s compute=%d.%d\n",prop.name,prop.major,prop.minor);
    for(int n: {1,255,256,257,100003}) vectors(n);
    for(int n: {1,15,16,17,65}) matrices(n);
    return 0;
}
