#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
project_root="$PWD"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1
mkdir -p .tools build/reference
test -x /usr/bin/mpicc
test -x /usr/bin/mpiexec
if [ ! -d .tools/hpl-2.3 ]; then
    curl -fL --retry 2 -o .tools/hpl-2.3.tar.gz https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz
    tar -xzf .tools/hpl-2.3.tar.gz -C .tools
fi
if [ ! -d .tools/hpcg/.git ]; then
    git clone https://github.com/hpcg-benchmark/hpcg.git .tools/hpcg
fi
git -C .tools/hpcg checkout --detach 114602d458d1034faa52b71e4c15aba9b3a17698
cp .tools/hpl-2.3/setup/Make.Linux_PII_CBLAS .tools/hpl-2.3/Make.Linux_PII_CBLAS
make -C .tools/hpl-2.3 -j1 arch=Linux_PII_CBLAS \
    TOPdir="$project_root/.tools/hpl-2.3" MPinc= MPlib= LAlib=-lopenblas \
    CC=/usr/bin/mpicc LINKER=/usr/bin/mpicc > build/reference/hpl-build.txt 2>&1
mkdir -p build/reference/hpl
cp examples/benchmark/HPL.dat build/reference/hpl/
(
    cd build/reference/hpl
    /usr/bin/mpiexec -n 1 "$project_root/.tools/hpl-2.3/bin/Linux_PII_CBLAS/xhpl" | tee output.txt
)
mkdir -p build/reference/hpcg-compile
(
    cd build/reference/hpcg-compile
    "$project_root/.tools/hpcg/configure" MPI_GCC_OMP
    make -j4 CXX=/usr/bin/mpicxx LINKER=/usr/bin/mpicxx \
        CXXFLAGS="-I$project_root/.tools/hpcg/src -O2 -fopenmp" LINKFLAGS='-O2 -fopenmp'
) > build/reference/hpcg-build.txt 2>&1
hpcg_run_dir="build/reference/hpcg-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$hpcg_run_dir"
cp examples/benchmark/hpcg.dat "$hpcg_run_dir/"
(
    cd "$hpcg_run_dir"
    /usr/bin/mpiexec -n 1 "$project_root/build/reference/hpcg-compile/bin/xhpcg" | tee output.txt
)
git -C .tools/hpcg rev-parse HEAD > build/reference/hpcg-revision.txt
sha256sum .tools/hpl-2.3.tar.gz > build/reference/hpl-archive-sha256.txt
grep -q '1 tests completed and passed residual checks' build/reference/hpl/output.txt
grep -q 'HPCG result is VALID' "$hpcg_run_dir"/HPCG-Benchmark*.txt
echo 'Reference runs finished. Inspect residual and validity reports; short runs are not official scores.'
