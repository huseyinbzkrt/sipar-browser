#!/usr/bin/env python3
"""
Sipar Browser — Build Scripti
Kullanım: python3 scripts/build.py --platform [windows|linux|mac]
"""

import os
import sys
import subprocess
import argparse
import shutil
import platform as _platform

BUILD_DIR = "build"
SRC_DIR = os.path.join(BUILD_DIR, "src")
OUT_DIR = os.path.join(SRC_DIR, "out", "Sipar")
UNGOOGLED_DIR = os.path.join(BUILD_DIR, "ungoogled-chromium")

SIPAR_VERSION = "1.0.0"

# GN build flags — gizlilik ve performans için optimize
GN_FLAGS = """
# Sipar Browser Build Flags

# Branding
chromium_branding_path = "//sipar/branding"

# Google servisleri kapat
google_api_key = "no"
google_default_client_id = "no"
google_default_client_secret = "no"

# Telemetry kapat
enable_reporting = false
enable_background_mode = false

# Performans
is_official_build = true
is_debug = false
symbol_level = 0
enable_nacl = false
blink_symbol_level = 0

# Güvenlik
enable_linux_installer = true
"""


def run(cmd, cwd=None, check=True):
    print(f"  $ {cmd[:80]}...")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if check and result.returncode != 0:
        print(f"  ❌ Build hatası!")
        sys.exit(1)
    return result


def check_setup():
    if not os.path.exists(SRC_DIR):
        print("❌ Build ortamı kurulmamış!")
        print("   Önce: python3 scripts/setup.py")
        sys.exit(1)


def write_gn_flags(extra_flags=""):
    gn_path = os.path.join(SRC_DIR, "out", "Sipar", "args.gn")
    os.makedirs(os.path.dirname(gn_path), exist_ok=True)
    
    with open(gn_path, "w") as f:
        f.write(GN_FLAGS)
        if extra_flags:
            f.write(extra_flags)
    
    print(f"  ✅ args.gn yazıldı")


def build_windows():
    print("\n🪟 Windows build başlıyor...")
    
    extra_flags = """
target_os = "win"
target_cpu = "x64"
"""
    write_gn_flags(extra_flags)
    run("gn gen out/Sipar", cwd=SRC_DIR)
    run("ninja -C out/Sipar chrome", cwd=SRC_DIR)


def build_linux():
    print("\n🐧 Linux build başlıyor...")
    
    extra_flags = """
target_os = "linux"
target_cpu = "x64"
"""
    write_gn_flags(extra_flags)
    run("gn gen out/Sipar", cwd=SRC_DIR)
    run("ninja -C out/Sipar chrome", cwd=SRC_DIR)


def package(platform_name):
    print(f"\n📦 {platform_name} paketi oluşturuluyor...")
    
    dist_dir = f"dist/sipar-{SIPAR_VERSION}-{platform_name}"
    os.makedirs(dist_dir, exist_ok=True)
    
    if platform_name == "windows":
        # NSIS installer
        print("  NSIS installer oluşturuluyor...")
        # TODO: NSIS script
    elif platform_name == "linux":
        # tar.xz + .deb
        print("  Linux paketi oluşturuluyor...")
        # TODO: deb packaging
    
    print(f"  ✅ Paket hazır: {dist_dir}/")


def main():
    parser = argparse.ArgumentParser(description="Sipar Browser Build Scripti")
    parser.add_argument("--platform", choices=["windows", "linux", "mac"], 
                       default=_platform.system().lower())
    parser.add_argument("--package", action="store_true", help="Build sonrası paket oluştur")
    parser.add_argument("--clean", action="store_true", help="Build klasörünü temizle")
    args = parser.parse_args()
    
    print(f"🛡️ Sipar Browser v{SIPAR_VERSION} — {args.platform} build")
    print("=" * 50)
    
    if args.clean:
        print("🧹 Temizleniyor...")
        shutil.rmtree(OUT_DIR, ignore_errors=True)
    
    check_setup()
    
    if args.platform == "windows":
        build_windows()
    elif args.platform == "linux":
        build_linux()
    elif args.platform == "mac":
        print("❌ macOS build henüz hazır değil (Faz 3)")
        sys.exit(1)
    
    if args.package:
        package(args.platform)
    
    print(f"\n✅ Build tamamlandı! → {OUT_DIR}/chrome")


if __name__ == "__main__":
    main()
