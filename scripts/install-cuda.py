"""Install selected official CUDA redistributables locally, checking SHA256."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile

p = argparse.ArgumentParser()
p.add_argument("--nsys", action="store_true")
args = p.parse_args()
root = Path(__file__).resolve().parents[1] / ".tools"
root.mkdir(exist_ok=True)
base = "https://developer.download.nvidia.com/compute/cuda/redist/"
manifest = root / "redistrib_12.4.1.json"
subprocess.run(["curl", "-fL", "--retry", "3", "-o", str(manifest), base + manifest.name], check=True)
data = json.loads(manifest.read_text())
components = ["cuda_nvcc", "cuda_cudart", "cuda_cccl", "cuda_sanitizer_api"]
if args.nsys:
    components.append("nsight_systems")
for key in components:
    item = data[key]["linux-x86_64"]
    archive = root / Path(item["relative_path"]).name
    if not archive.exists() or hashlib.sha256(archive.read_bytes()).hexdigest() != item["sha256"]:
        subprocess.run(["curl", "-fL", "--retry", "3", "-o", str(archive), base + item["relative_path"]], check=True)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != item["sha256"]:
        raise RuntimeError(f"Checksum failed: {archive}")
    dest = root / ("nsys" if key == "nsight_systems" else "cuda")
    dest.mkdir(exist_ok=True)
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            parts = Path(member.name).parts[1:]
            if not parts:
                continue
            member.name = str(Path(*parts))
            if key == "nsight_systems" and "/bin/" in member.name and (member.issym() or member.islnk()):
                continue
            if not (dest / member.name).resolve().is_relative_to(dest.resolve()):
                raise RuntimeError("Unsafe archive member")
            tar.extract(member, dest, filter="data")
    print(f"INSTALLED {key} {data[key]['version']} sha256={item['sha256']}")
lib64 = root / "cuda" / "lib64"
if not lib64.exists():
    lib64.symlink_to("lib", target_is_directory=True)
