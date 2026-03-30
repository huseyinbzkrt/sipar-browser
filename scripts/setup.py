#!/usr/bin/env python3
"""
Sipar Browser — Build Ortamı Kurulum Scripti
Kullanım: python3 scripts/setup.py
"""

import os
import sys
import subprocess
import platform

UNGOOGLED_REPO = "https://github.com/ungoogled-software/ungoogled-chromium.git"
UNGOOGLED_WINDOWS_REPO = "https://github.com/ungoogled-software/ungoogled-chromium-windows.git"
UNGOOGLED_LINUX_REPO = "https://github.com/ungoogled-software/ungoogled-chromium-portablelinux.git"

BUILD_DIR = "build"
SRC_DIR = os.path.join(BUILD_DIR, "src")
CACHE_DIR = os.path.join(BUILD_DIR, "download_cache")
UNGOOGLED_DIR = os.path.join(BUILD_DIR, "ungoogled-chromium")


def run(cmd, cwd=None):
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"  ❌ Hata: {cmd}")
        sys.exit(1)
    return result


def check_requirements():
    print("📋 Gereksinimler kontrol ediliyor...")
    
    system = platform.system()
    print(f"  Platform: {system}")
    
    required = {
        "git": "git --version",
        "python3": "python3 --version",
    }
    
    if system == "Linux":
        required.update({
            "clang": "clang --version",
            "ninja": "ninja --version",
        })
    
    for name, cmd in required.items():
        try:
            subprocess.run(cmd.split(), capture_output=True, check=True)
            print(f"  ✅ {name}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ❌ {name} bulunamadı — lütfen kurun")
            sys.exit(1)


def clone_ungoogled():
    print("\n📦 Ungoogled-Chromium indiriliyor...")
    
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    if os.path.exists(UNGOOGLED_DIR):
        print("  ✅ Zaten mevcut, güncelleniyor...")
        run("git pull", cwd=UNGOOGLED_DIR)
    else:
        run(f"git clone --depth=1 {UNGOOGLED_REPO} {UNGOOGLED_DIR}")
    
    # Versiyon bilgisi
    version_file = os.path.join(UNGOOGLED_DIR, "chromium_version.txt")
    if os.path.exists(version_file):
        with open(version_file) as f:
            version = f.read().strip()
        print(f"  📌 Chromium versiyonu: {version}")


def apply_sipar_patches():
    print("\n🛡️ Sipar patch'leri uygulanıyor...")
    
    patches_dir = os.path.join(os.path.dirname(__file__), "..", "patches", "core")
    
    if not os.path.exists(patches_dir):
        print("  ⚠️ Patch klasörü boş, atlanıyor")
        return
    
    patch_files = sorted([f for f in os.listdir(patches_dir) if f.endswith(".patch")])
    
    if not patch_files:
        print("  ⚠️ Henüz patch yok")
        return
    
    for patch in patch_files:
        patch_path = os.path.join(patches_dir, patch)
        print(f"  Applying: {patch}")
        run(f"git apply {patch_path}", cwd=SRC_DIR)
    
    print(f"  ✅ {len(patch_files)} patch uygulandı")


def main():
    print("🛡️ Sipar Browser — Build Ortamı Kurulumu")
    print("=" * 50)
    
    check_requirements()
    clone_ungoogled()
    apply_sipar_patches()
    
    print("\n✅ Kurulum tamamlandı!")
    print("\nSonraki adım:")
    print("  python3 scripts/build.py --platform windows")


if __name__ == "__main__":
    main()
