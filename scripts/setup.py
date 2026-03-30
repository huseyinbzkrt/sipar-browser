#!/usr/bin/env python3
"""
Sipar Browser — Setup Script
Ungoogled-Chromium portable binary indirir ve Sipar dosya yapısını hazırlar.
"""

import os
import sys
import json
import shutil
import urllib.request
import zipfile
import tarfile
import platform

# --- Config ---
CHROMIUM_VERSION = "146.0.7680.164"

DOWNLOADS = {
    "windows": {
        "url": "https://github.com/ungoogled-software/ungoogled-chromium-windows/releases/download/146.0.7680.164-1.1/ungoogled-chromium_146.0.7680.164-1.1_windows_x64.zip",
        "filename": "ungoogled-chromium_146.0.7680.164-1.1_windows_x64.zip",
    },
    "linux": {
        "url": "https://github.com/ungoogled-software/ungoogled-chromium-portablelinux/releases/download/146.0.7680.164-1/ungoogled-chromium-146.0.7680.164-1-x86_64_linux.tar.xz",
        "filename": "ungoogled-chromium-146.0.7680.164-1-x86_64_linux.tar.xz",
    },
}

# uBlock Origin latest (gorhill/uBlock official release)
UBLOCK_URL = "https://github.com/gorhill/uBlock/releases/download/1.70.0/uBlock0_1.70.0.chromium.zip"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(ROOT, "build")
CACHE_DIR = os.path.join(BUILD_DIR, "cache")
DIST_DIR = os.path.join(ROOT, "dist")


def detect_platform():
    if "--platform" in sys.argv:
        idx = sys.argv.index("--platform")
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    return "linux"


def download(url, dest):
    if os.path.exists(dest):
        print(f"  ✅ Cache'de mevcut: {os.path.basename(dest)}")
        return
    print(f"  ⬇️  İndiriliyor: {os.path.basename(dest)}")
    urllib.request.urlretrieve(url, dest, reporthook=lambda c, b, t: print(f"\r  {c*b/1024/1024:.0f} MB", end=""))
    print()


def extract_windows(archive, target):
    print("  📦 Windows ZIP çıkartılıyor...")
    with zipfile.ZipFile(archive, 'r') as zf:
        zf.extractall(target)
    # Ungoogled-Chromium ZIP içinde bir klasör oluşturur, onu bul
    items = os.listdir(target)
    if len(items) == 1 and os.path.isdir(os.path.join(target, items[0])):
        inner = os.path.join(target, items[0])
        for item in os.listdir(inner):
            shutil.move(os.path.join(inner, item), os.path.join(target, item))
        os.rmdir(inner)


def extract_linux(archive, target):
    print("  📦 Linux tar.xz çıkartılıyor...")
    with tarfile.open(archive, 'r:xz') as tf:
        tf.extractall(target)
    items = os.listdir(target)
    if len(items) == 1 and os.path.isdir(os.path.join(target, items[0])):
        inner = os.path.join(target, items[0])
        for item in os.listdir(inner):
            shutil.move(os.path.join(inner, item), os.path.join(target, item))
        os.rmdir(inner)


def download_ublock(cache_dir):
    dest = os.path.join(cache_dir, "ublock.zip")
    print("\n🚫 uBlock Origin indiriliyor...")
    download(UBLOCK_URL, dest)
    return dest


def apply_master_preferences(chrome_dir, plat):
    """Varsayılan ayarları master_preferences ile enjekte et."""
    print("\n⚙️  Master preferences yazılıyor...")

    prefs = {
        "homepage": "https://sipar.io",
        "homepage_is_newtabpage": False,
        "browser": {
            "show_home_button": True,
            "check_default_browser": False,
        },
        "dns_over_https": {
            "mode": "secure",
            "templates": "https://dns.quad9.net/dns-query",
        },
        "default_search_provider": {
            "enabled": True,
            "name": "Brave Search",
            "keyword": "brave",
            "search_url": "https://search.brave.com/search?q={searchTerms}",
            "suggest_url": "https://search.brave.com/api/suggest?q={searchTerms}",
            "favicon_url": "https://cdn.search.brave.com/serp/v2/_app/immutable/assets/favicon.CKPNbKi6.ico",
        },
        "privacy": {
            "do_not_track": True,
            "global_privacy_control": True,
        },
        "profile": {
            "default_content_setting_values": {
                "cookies": 1,
                "third_party_cookies": 2,  # Block 3rd party
            },
        },
        "webkit": {
            "webprefs": {
                "hyperlink_auditing": False,
            },
        },
        "net": {
            "network_prediction_options": 2,  # Disabled
        },
        "safebrowsing": {
            "enabled": False,  # Google Safe Browsing kapalı — lokal koruma kullanılacak
        },
        "translate": {
            "enabled": False,  # Google Translate kapalı
        },
        "distribution": {
            "import_bookmarks": True,
            "import_history": True,
            "import_search_engine": False,
            "make_chrome_default_for_user": False,
            "suppress_first_run_bubble": True,
            "skip_first_run_ui": True,
        },
    }

    prefs_file = "master_preferences" if plat == "windows" else "initial_preferences"
    prefs_path = os.path.join(chrome_dir, prefs_file)
    with open(prefs_path, "w") as f:
        json.dump(prefs, f, indent=2)
    print(f"  ✅ {prefs_file} yazıldı")


def apply_policies(chrome_dir, plat):
    """Kurumsal policy ile zorunlu gizlilik ayarları."""
    print("\n🔒 Gizlilik politikaları yazılıyor...")

    policies = {
        "AutofillAddressEnabled": False,
        "AutofillCreditCardEnabled": False,
        "BackgroundModeEnabled": False,
        "BlockThirdPartyCookies": True,
        "BrowserSignin": 0,  # Disable
        "DnsOverHttpsMode": "secure",
        "DnsOverHttpsTemplates": "https://dns.quad9.net/dns-query",
        "EnableMediaRouter": False,  # Cast disabled
        "HttpsOnlyMode": "force_enabled",
        "MetricsReportingEnabled": False,
        "PasswordManagerEnabled": True,
        "PromotionalTabsEnabled": False,
        "SafeBrowsingProtectionLevel": 0,
        "SearchSuggestEnabled": True,
        "SpellcheckEnabled": True,
        "SyncDisabled": True,  # Google Sync kapalı — Sipar Sync gelecek
        "TranslateEnabled": False,
        "UrlKeyedAnonymizedDataCollectionEnabled": False,
    }

    if plat == "windows":
        policies_dir = os.path.join(chrome_dir, "policies", "managed")
    else:
        policies_dir = "/etc/chromium/policies/managed"
        # Linux'da local build için de yazalım
        local_policies = os.path.join(chrome_dir, "policies", "managed")
        os.makedirs(local_policies, exist_ok=True)
        with open(os.path.join(local_policies, "sipar_privacy.json"), "w") as f:
            json.dump(policies, f, indent=2)
        print(f"  ✅ Local policies yazıldı")

    os.makedirs(policies_dir, exist_ok=True)
    with open(os.path.join(policies_dir, "sipar_privacy.json"), "w") as f:
        json.dump(policies, f, indent=2)
    print(f"  ✅ Privacy policies yazıldı")


def install_ublock(chrome_dir, ublock_zip):
    """uBlock Origin'i yerleşik uzantı olarak kur."""
    print("\n🚫 uBlock Origin kuruluyor...")

    ext_dir = os.path.join(chrome_dir, "Extensions", "ublock")
    os.makedirs(ext_dir, exist_ok=True)

    with zipfile.ZipFile(ublock_zip, 'r') as zf:
        zf.extractall(ext_dir)

    # external_extensions.json ile otomatik yükleme
    ext_json_dir = os.path.join(chrome_dir, "external_extensions")
    os.makedirs(ext_json_dir, exist_ok=True)

    # uBlock Origin'in Chrome Web Store ID'si
    ublock_id = "cjpalhdlnbpafiamejdnhcphjbkeiagm"
    ext_json = {
        "external_crx": os.path.join(ext_dir),
        "external_version": "1.0.0",
    }

    print(f"  ✅ uBlock Origin yerleştirildi")


def install_newtab(chrome_dir):
    """Sipar New Tab sayfasını extension olarak paketle."""
    print("\n🏠 New Tab uzantısı kuruluyor...")

    newtab_src = os.path.join(ROOT, "src", "newtab")
    newtab_ext = os.path.join(chrome_dir, "Extensions", "sipar-newtab")
    os.makedirs(newtab_ext, exist_ok=True)

    # manifest.json
    manifest = {
        "manifest_version": 3,
        "name": "Sipar New Tab",
        "version": "1.0.0",
        "description": "Sipar Browser özel yeni sekme sayfası",
        "chrome_url_overrides": {
            "newtab": "index.html"
        },
        "icons": {
            "128": "icon.png"
        },
    }

    with open(os.path.join(newtab_ext, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    # HTML ve diğer dosyaları kopyala
    for fname in os.listdir(newtab_src):
        src = os.path.join(newtab_src, fname)
        dst = os.path.join(newtab_ext, fname)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

    # Logo'yu icon olarak kopyala
    logo = os.path.join(ROOT, "branding", "logo.png")
    if os.path.exists(logo):
        shutil.copy2(logo, os.path.join(newtab_ext, "icon.png"))

    print(f"  ✅ Sipar New Tab extension hazır")


def main():
    plat = detect_platform()
    print(f"🛡️  Sipar Browser Setup — Platform: {plat}")
    print(f"📌 Chromium base: v{CHROMIUM_VERSION}")
    print("=" * 55)

    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)

    chrome_dir = os.path.join(BUILD_DIR, "chrome")
    if os.path.exists(chrome_dir):
        shutil.rmtree(chrome_dir)
    os.makedirs(chrome_dir)

    # 1. Ungoogled-Chromium indir
    info = DOWNLOADS[plat]
    archive = os.path.join(CACHE_DIR, info["filename"])
    print(f"\n📥 Ungoogled-Chromium indiriliyor...")
    download(info["url"], archive)

    # 2. Çıkart
    if plat == "windows":
        extract_windows(archive, chrome_dir)
    else:
        extract_linux(archive, chrome_dir)

    # 3. uBlock Origin
    ublock_zip = download_ublock(CACHE_DIR)
    install_ublock(chrome_dir, ublock_zip)

    # 4. New Tab extension
    install_newtab(chrome_dir)

    # 5. Master preferences
    apply_master_preferences(chrome_dir, plat)

    # 6. Policies
    apply_policies(chrome_dir, plat)

    print("\n" + "=" * 55)
    print(f"✅ Sipar Browser hazır: {chrome_dir}")
    print(f"\nSonraki adım:")
    print(f"  python3 scripts/build.py --platform {plat}")


if __name__ == "__main__":
    main()
