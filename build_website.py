#!/usr/bin/env python3
"""
build_website.py — 一键构建: R 数据 → zarr → Vitessce → 静态网站
"""

import subprocess
import os
from pathlib import Path

PROJECT = Path("/home/data/Projects/2026/Ran_SCI")
WEBSITE = PROJECT / "website"
BUILD = WEBSITE / "build"
DATA = WEBSITE / "data"
PYTHON = "/home/bio/miniconda3/envs/vitessce/bin/python"


def run_step(name, cmd, cwd=None):
    print(f"\n{'=' * 60}")
    print(f"Step: {name}")
    print(f"{'=' * 60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        raise RuntimeError(f"Failed: {name}")
    if result.stdout:
        print(result.stdout)
    print(f"✓ {name}")


def main():
    # Step 1: 确保 zarr 数据已转换
    zarr_file = DATA / "own" / "own_data.h5ad.zarr"
    if not zarr_file.exists():
        print("Zarr file not found. Running data conversion...")
        run_step("Convert own data to zarr",
                 f"{PYTHON} src/data_prep/convert_own_data.py",
                 cwd=WEBSITE)
    else:
        size_mb = sum(f.stat().st_size for f in zarr_file.rglob("*") if f.is_file()) / 1e6
        print(f"Zarr file exists: {zarr_file} ({size_mb:.0f} MB)")

    # Step 2: 创建 build 目录并链接数据
    BUILD.mkdir(parents=True, exist_ok=True)
    data_link = BUILD / "data"
    if data_link.exists() or data_link.is_symlink():
        data_link.unlink()
    os.symlink("../data", str(data_link))
    print(f"Linked data/ -> build/data/")

    # Step 3: 生成 Vitessce 配置
    config_py = WEBSITE / "src/config/build_config.py"
    if config_py.exists():
        run_step("Build Vitessce config (remote mode)",
                 f"{PYTHON} src/config/build_config.py remote",
                 cwd=WEBSITE)

    # Step 4: 复制静态文件到 build/
    run_step("Copy static files",
             f"cp -r {WEBSITE}/src/static/* {BUILD}/")

    # Step 5: 生成 requirements.txt
    req = WEBSITE / "requirements.txt"
    req.write_text("vitessce==3.4.0\nscanpy\nanndata\nnumpy\npandas\nh5py\nzarr\nscipy\n")

    print(f"\n{'=' * 60}")
    print(f"Build complete!")
    print(f"  Output: {BUILD}")
    print(f"  Preview: python {WEBSITE}/preview.py")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
