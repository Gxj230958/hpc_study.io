# Source from any directory: source /path/to/hpc_study.io/scripts/activate-study.sh
STUDY_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source "$STUDY_ROOT/.venv/bin/activate"
export PATH="$STUDY_ROOT/.tools/cuda/bin:$STUDY_ROOT/.tools/nsys/nsight-systems/2023.4.4/target-linux-x64:$PATH"
export OMP_NUM_THREADS=10
export OPENBLAS_NUM_THREADS=10
export MKL_NUM_THREADS=10
# The course compares FP32 results at tolerances that TF32 cannot satisfy.
export NVIDIA_TF32_OVERRIDE=0
export TORCH_ALLOW_TF32_CUBLAS_OVERRIDE=0
unset STUDY_ROOT
