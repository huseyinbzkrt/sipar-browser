# Sipar Browser — Teknik Mimari

## Genel Bakış

Sipar, **Ungoogled-Chromium** üzerine inşa edilmiş bir tarayıcıdır.

```
Chromium (Google)
    └── Ungoogled-Chromium (Google kaldırıldı)
            └── Sipar Browser (bizim katmanımız)
```

## Katman Yapısı

### 1. Ungoogled-Chromium Base
- Google hesap entegrasyonu kaldırılmış
- Google Update servisi yok
- Telemetry yok
- Safe Browsing lokal mod

### 2. Sipar Patch Katmanı
- Branding (isim, ikon, renkler)
- Varsayılan ayarlar
- Özel New Tab sayfası
- Privacy Shield UI
- Özel ayarlar sayfası

### 3. Sipar Özellikleri
- Privacy Score sistemi
- Tema motoru
- Profil sistemi
- (İleride) Sync, VPN

## Build Süreci

```
ungoogled-chromium kaynak kodu
    ↓
sipar patch'leri uygulanır
    ↓
GN ile derleme (ninja)
    ↓
Platform installer oluşturulur
    ↓
GitHub Release
```

## Platform Desteği

| Platform | Durum | Build Aracı |
|----------|-------|-------------|
| Windows x64 | Faz 1 | NSIS Installer |
| Linux x64 | Faz 1 | .tar.xz + .deb |
| macOS | Faz 3 | .dmg |
| Android | Faz 4 | APK |

## Klasör Yapısı

```
sipar-browser/
├── patches/              # Chromium yamaları
│   ├── core/             # Zorunlu (branding, ayarlar)
│   └── extra/            # Opsiyonel özellikler
├── branding/             # Görsel kimlik
│   ├── icons/            # Ikon setleri (16-512px)
│   ├── themes/           # Renk temaları
│   └── splash/           # Açılış ekranı
├── src/                  # Sipar'a özel kaynak kodlar
│   ├── newtab/           # New Tab sayfası (HTML/CSS/JS)
│   ├── settings/         # sipar://settings
│   └── shield/           # Privacy Shield bileşeni
├── scripts/              # Build & yardımcı scriptler
│   ├── build.py          # Ana build scripti
│   ├── package.py        # Installer oluşturucu
│   └── apply_patches.py  # Patch uygulayıcı
├── ci/                   # GitHub Actions
│   └── workflows/
├── docs/                 # Dokümantasyon
└── tests/                # Testler
```
