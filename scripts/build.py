#!/usr/bin/env python3
"""
Sipar Browser — Build & Package Script
Setup sonrası çalışır: chrome_dir içindeki Ungoogled-Chromium'u
Sipar olarak paketler.
"""

import os
import sys
import shutil
import zipfile
import platform
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(ROOT, "build")
CHROME_DIR = os.path.join(BUILD_DIR, "chrome")
DIST_DIR = os.path.join(ROOT, "dist")


def detect_platform():
    if "--platform" in sys.argv:
        idx = sys.argv.index("--platform")
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    system = platform.system().lower()
    return "windows" if system == "windows" else "linux"


def apply_branding_windows(chrome_dir):
    """Windows binary'sine Sipar branding uygula."""
    print("🎨 Windows branding uygulanıyor...")

    # Windows'da exe ikonunu değiştirmek için rcedit gerekir
    # GitHub Actions'da bunu otomatik yaparız
    rcedit_url = "https://github.com/nicedoc/nicedoc.io/raw/refs/heads/master/assets/rcedit-x64.exe"

    icon_path = os.path.join(ROOT, "branding", "logo.png")

    # Şimdilik branding bilgilerini bir dosyaya yazalım
    branding_info = {
        "name": "Sipar Browser",
        "company": "Sipar Project",
        "description": "Gizlilik odaklı açık kaynak tarayıcı",
        "version": get_version(),
        "copyright": "© 2026 Sipar Project. MIT License.",
    }

    with open(os.path.join(chrome_dir, "sipar_branding.json"), "w") as f:
        json.dump(branding_info, f, indent=2)

    print("  ✅ Branding bilgileri yazıldı")


def apply_branding_linux(chrome_dir):
    """Linux binary'sine Sipar branding uygula."""
    print("🎨 Linux branding uygulanıyor...")

    # .desktop dosyası
    desktop = f"""[Desktop Entry]
Name=Sipar Browser
Comment=Gizlilik odaklı açık kaynak tarayıcı
Exec={chrome_dir}/chrome --no-default-browser-check %U
Terminal=false
Icon={os.path.join(ROOT, "branding", "logo.png")}
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
StartupWMClass=chromium-browser
"""

    desktop_path = os.path.join(chrome_dir, "sipar-browser.desktop")
    with open(desktop_path, "w") as f:
        f.write(desktop)

    # Wrapper script
    wrapper = f"""#!/bin/bash
# Sipar Browser Launcher
SIPAR_DIR="$(dirname "$(readlink -f "$0")")"
exec "$SIPAR_DIR/chrome" \\
    --no-default-browser-check \\
    --no-first-run \\
    --flag-switches-begin \\
    --disable-features=MediaRouter \\
    --enable-features=GlobalPrivacyControl \\
    --flag-switches-end \\
    "$@"
"""

    wrapper_path = os.path.join(chrome_dir, "sipar")
    with open(wrapper_path, "w") as f:
        f.write(wrapper)
    os.chmod(wrapper_path, 0o755)

    print("  ✅ .desktop + launcher yazıldı")


def get_version():
    version_file = os.path.join(ROOT, "VERSION")
    if os.path.exists(version_file):
        with open(version_file) as f:
            return f.read().strip()
    return "0.1.0-alpha"


def package_windows(chrome_dir, dist_dir):
    """Windows için zip paketle."""
    print("\n📦 Windows paketi oluşturuluyor...")

    version = get_version()
    zip_name = f"sipar-browser-{version}-windows-x64.zip"
    zip_path = os.path.join(dist_dir, zip_name)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(chrome_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join("sipar-browser", os.path.relpath(file_path, chrome_dir))
                zf.write(file_path, arcname)

    size_mb = os.path.getsize(zip_path) / 1024 / 1024
    print(f"  ✅ {zip_name} ({size_mb:.0f} MB)")
    return zip_path


def package_linux(chrome_dir, dist_dir):
    """Linux için tar.xz paketle."""
    print("\n📦 Linux paketi oluşturuluyor...")

    version = get_version()
    tar_name = f"sipar-browser-{version}-linux-x64.tar.xz"
    tar_path = os.path.join(dist_dir, tar_name)

    import subprocess
    subprocess.run([
        "tar", "cJf", tar_path,
        "-C", BUILD_DIR,
        "--transform", "s/^chrome/sipar-browser/",
        "chrome"
    ], check=True)

    size_mb = os.path.getsize(tar_path) / 1024 / 1024
    print(f"  ✅ {tar_name} ({size_mb:.0f} MB)")
    return tar_path


def main():
    plat = detect_platform()
    version = get_version()
    print(f"🛡️  Sipar Browser Build — v{version}")
    print(f"📦 Platform: {plat}")
    print("=" * 55)

    if not os.path.exists(CHROME_DIR):
        print("❌ Build klasörü bulunamadı. Önce setup.py çalıştırın:")
        print("   python3 scripts/setup.py")
        sys.exit(1)

    os.makedirs(DIST_DIR, exist_ok=True)

    # Branding
    if plat == "windows":
        apply_branding_windows(CHROME_DIR)
    else:
        apply_branding_linux(CHROME_DIR)

    # Package
    if "--package" in sys.argv:
        if plat == "windows":
            pkg = package_windows(CHROME_DIR, DIST_DIR)
        else:
            pkg = package_linux(CHROME_DIR, DIST_DIR)

        print(f"\n{'=' * 55}")
        print(f"✅ Sipar Browser v{version} paketlendi!")
        print(f"📁 Çıktı: {pkg}")
    else:
        print(f"\n✅ Branding uygulandı. Paketlemek için:")
        print(f"   python3 scripts/build.py --platform {plat} --package")


if __name__ == "__main__":
    main()
