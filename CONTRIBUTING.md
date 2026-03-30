# Sipar'a Katkı Rehberi

## Geliştirme Ortamı

### Gereksinimler
- Python 3.10+
- Git
- **Windows:** Visual Studio 2022 + Windows SDK 10
- **Linux:** clang, ninja-build, bağımlılıklar (bkz. ci/workflows/build.yml)

### Kurulum
```bash
git clone https://github.com/huseyinbzkrt/sipar-browser
cd sipar-browser
python3 scripts/setup.py
```

### Build

```bash
# Windows
python scripts/build.py --platform windows

# Linux
python3 scripts/build.py --platform linux

# Build + paket oluştur
python3 scripts/build.py --platform linux --package
```

## Patch Yazma Kuralları

Patch dosyaları `patches/core/` veya `patches/extra/` altına konur.

İsimlendirme: `NN-açıklama.patch` (NN = 01, 02, ...)

Şablon:
```
Description: Ne yapıyor
Author: İsim
---
--- a/dosya/yolu
+++ b/dosya/yolu
@@ açıklama @@
- eski satır
+ yeni satır
```

## Commit Mesajları

```
feat: yeni özellik ekle
fix: hata düzelt
patch: chromium yaması ekle/güncelle
branding: görsel değişiklik
docs: dokümantasyon güncelle
ci: build/CI değişikliği
```

## Dal Stratejisi

- `main` → stabil, her zaman çalışır
- `dev` → aktif geliştirme
- `feature/xxx` → yeni özellikler
- `patch/xxx` → yeni yamalar

## Issue Açma

Bug bildirirken şunları yaz:
1. İşletim sistemi + versiyon
2. Ne yapmaya çalıştın
3. Ne oldu
4. Ne olmasını bekliyordun
