# Sipar Patches

Bu klasör, Ungoogled-Chromium üzerine uygulanan Sipar'a özel yamaları içerir.

## Patch Listesi

| Dosya | Açıklama |
|-------|----------|
| `01-branding.patch` | İsim, ikon, splash screen |
| `02-default-settings.patch` | Varsayılan gizlilik ayarları |
| `03-dns.patch` | Quad9 varsayılan DNS |
| `04-newtab.patch` | Özel New Tab entegrasyonu |

## Nasıl Uygulanır

```bash
cd ungoogled-chromium
git apply ../patches/*.patch
```
