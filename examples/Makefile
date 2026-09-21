BUILD := ../build
CC := gcc
CFLAGS := -O2 -Wall -Wextra -Werror -fopenmp
NVCC ?= nvcc
CUDA_ARCH ?= native
.PHONY: cpu cuda
cpu: $(BUILD)/sum $(BUILD)/memory
$(BUILD):
	mkdir -p $@
$(BUILD)/sum: cpu/sum.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@
$(BUILD)/memory: cpu/memory.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@
cuda: $(BUILD)/cuda_labs
$(BUILD)/cuda_labs: cuda/labs.cu | $(BUILD)
	$(NVCC) -O2 -std=c++17 -arch=$(CUDA_ARCH) $< -o $@
