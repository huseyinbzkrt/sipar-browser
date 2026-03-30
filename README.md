# 🛡️ Sipar Browser

> **Sipar** — Kürtçe "kalkan" anlamına gelir.

Sipar, gizlilik, performans ve şeffaflığı ön planda tutan açık kaynaklı bir web tarayıcısıdır. [Ungoogled-Chromium](https://github.com/ungoogled-software/ungoogled-chromium) üzerine inşa edilmiştir.

---

## ✨ Özellikler

- 🚫 Sıfır telemetry — hiçbir verin bize gönderilmez
- 🛡️ Gelişmiş reklam & tracker engelleme (uBlock Origin yerleşik)
- 🔒 Varsayılan olarak güvenli DNS (Quad9)
- 🎨 Tam özelleştirilebilir arayüz
- 📊 Şeffaf kaynak kodu — herkes denetleyebilir
- ⚡ Şişirilmemiş, performans öncelikli

## 💰 Fiyatlandırma

| Plan | Fiyat | İçerik |
|------|-------|--------|
| Temel | Ücretsiz | Tam tarayıcı |
| Sync | 10$/yıl | E2E şifreli senkronizasyon |
| Pro | 20$/yıl | VPN + Sync |
| Aile | 30$/yıl | 5 cihaz, tüm özellikler |

## 🏗️ Mimarî

```
sipar-browser/
├── patches/          # Chromium üzerine uygulanan yamalar
├── branding/         # Logo, ikonlar, splash screen
├── src/              # Sipar'a özel kaynak kodlar
│   ├── newtab/       # Özel New Tab sayfası
│   ├── settings/     # sipar://settings arayüzü
│   └── shield/       # Privacy Shield göstergesi
├── scripts/          # Build & release scriptleri
└── docs/             # Dokümantasyon
```

## 🚀 Build

> Yakında

## 🤝 Katkı

Pull request'ler açık. Önce bir issue aç.

## 📄 Lisans

MIT

---

**sipar.io** | Made with 🛡️
