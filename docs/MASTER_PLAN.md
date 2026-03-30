# 🛡️ Sipar Browser — Tam Mimari & Yol Haritası

> *"Gizlilik herkesin hakkı. Sipar bunu teknik bilgisi olmayan herkese ulaştırır."*

---

## 📋 İçindekiler

1. [Vizyon & Felsefe](#vizyon)
2. [Bugün Yapılanlar](#yapılanlar)
3. [Teknik Mimari](#mimari)
4. [Kullanıcı Deneyimi Tasarımı](#ux)
5. [Gizlilik Katmanları](#gizlilik)
6. [Build Sistemi](#build)
7. [Faz Planı — Detaylı](#fazlar)
8. [Gelir Modeli](#gelir)
9. [Dağıtım & Güncelleme](#dagitim)
10. [Topluluk & Büyüme](#topluluk)

---

## 1. Vizyon & Felsefe {#vizyon}

### Neden Sipar?

Bugün kullandığımız tarayıcıların büyük çoğunluğu bizi gözetliyor:

- **Chrome**: Google'ın reklam makinesinin bir parçası. Her tıklama, her arama, her sayfa ziyareti Google sunucularına gönderiliyor.
- **Edge**: Microsoft telemetrisi. Windows'a entegre, kaçış zor.
- **Brave**: İyi niyetle başladı ama BAT (kripto token) sistemi ve kendi reklam ağıyla yoldan çıktı.
- **Firefox**: En iyi alternatiflerden biri ama varsayılan ayarlar hâlâ zayıf, telemetry var.

**Sipar'ın farkı:**

```
Sipar = Ungoogled-Chromium + Sıfır Telemetry + Yerleşik Koruma + Herkes İçin UX
```

Sipar sadece "gizlilik tarayıcısı" olmak istemiyor. Amacımız:

> Teknik bilgisi sıfır olan bir kişinin de açıp kullanabileceği, varsayılan olarak güvenli, hızlı ve güzel bir tarayıcı yapmak.

### Temel İlkeler

| İlke | Açıklama |
|------|----------|
| **Sıfır telemetry** | Hiçbir kullanım verisi toplanmaz, asla |
| **Varsayılan güvenlik** | Kurulumdan sonra hiçbir ayar yapmadan korunma aktif |
| **Şeffaflık** | Her satır kod açık, bağımsız audit edilebilir |
| **Erişilebilirlik** | 60 yaşındaki biri de kullanabilmeli |
| **Performans** | Şişirilmemiş, hızlı, az RAM |
| **Türkçe öncelik** | Türk kullanıcılar için optimize, yerel özellikler |

---

## 2. Bugün Yapılanlar {#yapılanlar}

> 30 Mart 2026 — Projenin ilk günü

### ✅ Tamamlananlar

**Altyapı:**
- GitHub repo oluşturuldu: `github.com/huseyinbzkrt/sipar-browser`
- Proje klasör yapısı kuruldu
- GitHub Actions CI/CD pipeline yazıldı (Windows + Linux build)
- MIT lisansı belirlendi

**Geliştirme Dosyaları:**
- `scripts/setup.py` — Ungoogled-Chromium indirme + kurulum scripti
- `scripts/build.py` — Platform bazlı build scripti (Windows/Linux/Mac)
- `patches/core/01-branding.patch` — İsim, ikon değişim yaması
- `patches/core/02-default-settings.patch` — Gizlilik ayarları yaması
- `docs/ARCHITECTURE.md` — Teknik mimari belgesi
- `docs/ROADMAP.md` — Faz planı
- `CONTRIBUTING.md` — Katkı rehberi

**Kullanıcı Arayüzü:**
- `src/newtab/index.html` — Özel New Tab sayfası
  - Logo + arama kutusu
  - Arama motoru toggle (Brave/DuckDuckGo/Google)
  - 5 kısayol (özelleştirilebilir)
  - Saat + tarih
  - Privacy stats (tracker/reklam sayacı)
  - Lucide ikonlar

**Landing Page (sipar.huseyinbozkurt.com):**
- Tam responsive dark theme site
- Hero section (logo + punch copy + floating badge'ler)
- 4 feature section (Banana AI görselleriyle)
- Karşılaştırma tablosu (Chrome/Brave/Firefox vs Sipar)
- Waitlist formu (PHP backend, sunucuda CSV)
- FAQ bölümü
- TR/EN dil desteği (localStorage'a kaydedilir)
- Lucide icon sistemi
- SSL sertifikası (Let's Encrypt)

**Branding:**
- Logo v3: 3D mavi kalkan + S harfi, şeffaf PNG
- Renk paleti belirlendi (Navy #0A0D14, Electric Blue #4F8EF7)
- Tipografi: system-ui / Inter

---

## 3. Teknik Mimari {#mimari}

### Katman Yapısı

```
┌─────────────────────────────────────────────┐
│              KULLANICI ARAYÜZÜ               │
│   New Tab · Settings · Shield UI · Temalar  │
├─────────────────────────────────────────────┤
│           SİPAR ÖZELLİK KATMANI             │
│  Privacy Score · Sync · VPN · Profiller     │
├─────────────────────────────────────────────┤
│         SİPAR YAMA KATMANI (Patches)        │
│  Branding · DNS · Default Settings · UI     │
├─────────────────────────────────────────────┤
│          UNGOOGLED-CHROMIUM BASE             │
│  Google telemetrisi kaldırılmış Chromium    │
├─────────────────────────────────────────────┤
│              CHROMIUM CORE                   │
│  Blink Engine · V8 JS · Network Stack       │
└─────────────────────────────────────────────┘
```

### Neden Ungoogled-Chromium?

1. **Hazır temiz altyapı**: Google servisleri, update mekanizması, telemetry kaldırılmış
2. **Chrome uyumluluğu**: Tüm web standartlarını destekler, uzantılar çalışır
3. **Aktif geliştirme**: Her Chromium güncellemesinde hızla güncelleniyor
4. **MIT lisanslı**: Ticari kullanım serbest

### Klasör Yapısı (Tam)

```
sipar-browser/
│
├── .github/
│   └── workflows/
│       └── build.yml          # CI/CD — Windows + Linux otomatik build
│
├── patches/
│   ├── core/                  # Zorunlu yamalar
│   │   ├── 01-branding.patch          # İsim, ikon
│   │   ├── 02-default-settings.patch  # Gizlilik ayarları
│   │   ├── 03-dns.patch               # Quad9 varsayılan DNS
│   │   ├── 04-newtab.patch            # New Tab entegrasyonu
│   │   └── 05-search.patch            # Brave Search varsayılan
│   └── extra/                 # Opsiyonel yamalar
│       ├── 01-fingerprint.patch       # Parmak izi koruması
│       └── 02-https-upgrade.patch     # Tüm bağlantıları HTTPS'e yükselt
│
├── branding/
│   ├── logo.png               # Ana logo (şeffaf PNG)
│   ├── icon_16.png            # Favicon
│   ├── icon_32.png
│   ├── icon_48.png
│   ├── icon_128.png
│   ├── icon_256.png           # Windows installer
│   ├── icon_512.png
│   ├── icon.ico               # Windows multi-size
│   ├── icon.icns              # macOS
│   ├── splash.png             # Açılış ekranı
│   └── README.md              # Renk paleti, tasarım rehberi
│
├── src/
│   ├── newtab/                # Özel New Tab sayfası
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   │
│   ├── settings/              # sipar://settings
│   │   ├── index.html
│   │   ├── sections/
│   │   │   ├── privacy.html   # Gizlilik ayarları
│   │   │   ├── appearance.html # Tema, yazı tipi
│   │   │   ├── search.html    # Arama motoru seçimi
│   │   │   ├── shortcuts.html # New Tab kısayolları
│   │   │   └── about.html     # Sürüm, lisans
│   │   └── style.css
│   │
│   ├── shield/                # Privacy Shield bileşeni
│   │   ├── shield.js          # Tracker sayacı, anlık skor
│   │   └── ui.html            # Adres çubuğundaki popup
│   │
│   └── onboarding/            # İlk açılış rehberi
│       ├── index.html         # Hoş geldin ekranı
│       └── steps/             # Adım adım kurulum rehberi
│
├── scripts/
│   ├── setup.py               # Build ortamı kurulumu
│   ├── build.py               # Platform build scripti
│   ├── apply_patches.py       # Patch uygulayıcı
│   ├── package.py             # Installer oluşturucu
│   └── release.py             # GitHub release otomasyonu
│
├── website/                   # sipar.io landing page
│   ├── index.html
│   └── assets/
│       ├── logo.png
│       └── features/
│           ├── feat1-ads.jpg
│           ├── feat2-speed.jpg
│           ├── feat3-code.jpg
│           └── feat4-setup.jpg
│
├── docs/
│   ├── ROADMAP.md
│   ├── ARCHITECTURE.md
│   ├── MASTER_PLAN.md         # Bu dosya
│   └── BUILD_GUIDE.md         # Adım adım build rehberi
│
├── tests/
│   ├── privacy/               # Gizlilik testleri
│   └── ui/                    # Arayüz testleri
│
├── README.md
├── CONTRIBUTING.md
├── LICENSE (MIT)
└── .gitignore
```

---

## 4. Kullanıcı Deneyimi Tasarımı {#ux}

### Tasarım Felsefesi

> "En iyi gizlilik aracı, kullanılmak istenen araçtır."

Sipar'ın UX'i şu sorularla şekilleniyor:

- Annem bu tarayıcıyı kurup kullanabilir mi?
- Bir ayar değiştirmek için dokümantasyon okumak gerekiyor mu?
- Her özellik nerede olduğu belli mi?

### New Tab Sayfası

```
┌──────────────────────────────────────────────────────┐
│ 🛡 Korumalı · Quad9          [Pazartesi, 30 Mart]  ⏰│
├──────────────────────────────────────────────────────┤
│                                                      │
│                    [LOGO]                            │
│                   S İ P A R                         │
│                                                      │
│         ┌──────────────────────────────┐             │
│         │ 🔍  Ara veya adres gir... [Brave▼]│        │
│         └──────────────────────────────┘             │
│                                                      │
│    [GitHub] [SiberBakış] [YouTube] [Twitter] [Mail]  │
│                                                      │
│                                                      │
│  🚫 34 tracker   🚫 12 reklam   🔒 Sipar Browser    │
└──────────────────────────────────────────────────────┘
```

**Özellikler:**
- Arama motoru toggle: Brave Search → DuckDuckGo → Google → (özel)
- Kısayollar: sürükle-bırak ile sırala, + butonuyla ekle
- Saat/Tarih: kullanıcı kapatabilir
- Privacy stats: session bazlı, her açılışta sıfırlanır (ileride kümülatif)
- Dark/Light/Sistem teması

### Adres Çubuğu — Privacy Shield

```
┌─────────────────────────────────────────────────┐
│  🛡️ 34  │  https://example.com  │  ⭐ ⚙️ ↻  │
└─────────────────────────────────────────────────┘
```

Kalkan ikonuna tıklanınca popup:

```
┌──────────────────────────┐
│  🛡️ Sipar Koruması       │
│  ─────────────────────  │
│  ✅ 34 tracker engellendi │
│  ✅ 12 reklam engellendi  │
│  ✅ HTTPS aktif           │
│  ✅ Parmak izi koruması   │
│                          │
│  Privacy Skoru: ██████░  │
│                 8.5/10   │
│                          │
│  [Bu site için ayarlar]  │
└──────────────────────────┘
```

### Settings Sayfası — sipar://settings

Sol sidebar + sağ içerik alanı. Bölümler:

**🔒 Gizlilik**
- Tracker engelleme seviyesi (slider: Kapalı → Normal → Katı → Paranoyak)
- Çerez yönetimi (3rd party varsayılan kapalı)
- Parmak izi koruması (açık/kapalı)
- Global Privacy Control (GPC) — açık/kapalı
- Otomatik HTTPS yükseltme

**🔍 Arama & DNS**
- Varsayılan arama motoru (Brave/DDG/Google/Özel)
- DNS sağlayıcısı (Quad9/Cloudflare/OpenDNS/Özel)
- DNS-over-HTTPS zorunlu mu?

**🎨 Görünüm**
- Tema (Koyu / Açık / Sistem)
- Aksan rengi (6 seçenek + özel)
- Yazı tipi boyutu
- New Tab özelleştirme

**👤 Profiller**
- Profil ekle/sil/düzenle
- Her profil: ayrı uzantılar, ayrı çerezler, ayrı ayarlar
- "İş Profili" / "Kişisel Profil" presetleri

**🔄 Sync** (Faz 3)
- E2E şifreli senkronizasyon
- Sync edilen veriler: yer imleri, şifreler, ayarlar, geçmiş
- Cihaz yönetimi

**ℹ️ Hakkında**
- Sipar versiyonu
- Chromium base versiyonu
- Açık kaynak lisansları
- Güvenlik raporu linki

### Onboarding (İlk Açılış)

5 adımlı kurulum rehberi:

```
1. Hoş Geldiniz  →  2. Eski tarayıcıdan import  →  3. Arama motoru seç
→  4. Gizlilik seviyeni belirle  →  5. Hazırsın!
```

Her adım max 2 buton, 1 görsel, 30 kelime açıklama. Teknik terim yok.

---

## 5. Gizlilik Katmanları {#gizlilik}

### Katman 1 — Ungoogled-Chromium Base
- Google hesap entegrasyonu: ❌ Kaldırıldı
- Google güncelleyici: ❌ Kaldırıldı
- Google Safe Browsing (cloud): ❌ Kaldırıldı → Lokal liste kullanılır
- WebRTC IP sızıntısı koruması: ✅
- Google fonts CDN: ❌ → Lokal font fallback

### Katman 2 — Sipar Gizlilik Yamaları
- **Varsayılan DNS**: Quad9 (9.9.9.9) + DNS-over-HTTPS
- **3rd party cookie**: Varsayılan kapalı
- **Do Not Track**: Varsayılan açık
- **Global Privacy Control**: Varsayılan açık
- **Referrer Policy**: Strict — hangi siteden geldiğin paylaşılmaz
- **WebRTC**: Yalnızca genel IP, yerel IP sızdırılmaz

### Katman 3 — Yerleşik uBlock Origin
- Varsayılan filtre listeleri:
  - EasyList (reklam)
  - EasyPrivacy (tracker)
  - uBlock Filters (zararlı)
  - Turkish ABP List (Türkçe siteler için özel)
- Özelleştirilebilir kural ekleme
- Element gizleme modu
- Scriptlet injection koruması

### Katman 4 — Parmak İzi Koruması
- Canvas parmak izi: randomize edilir
- Audio parmak izi: randomize edilir
- WebGL vendor/renderer: gizlenir
- Ekran çözünürlüğü: yuvarlatılır
- Font listesi: sınırlandırılır
- Timezone spoofing (opsiyonel)

### Katman 5 — Ağ Güvenliği
- HTTPS-Only modu: tüm bağlantıları şifreli yapar
- HSTS preload listesi dahil
- Mixed content engelleme
- Güvensiz form engelleme (HTTP'den POST)

### Katman 6 — VPN (Faz 3, Premium)
- WireGuard protokolü
- No-log politikası, bağımsız audit
- Kill switch (VPN düşünce internet kesilir)
- 5 konum seçeneği (başlangıç için)
- DNS leak koruması

---

## 6. Build Sistemi {#build}

### Gereksinimler

| Platform | Araç | Süre |
|----------|------|------|
| Windows x64 | Visual Studio 2022 + Windows SDK | 4-6 saat |
| Linux x64 | clang + ninja + bağımlılıklar | 3-5 saat |
| macOS | Xcode + depot_tools | 4-6 saat |

### Build Akışı

```
1. Ungoogled-Chromium kaynağını indir
   └── scripts/setup.py

2. Sipar patch'lerini uygula
   └── scripts/apply_patches.py
   └── patches/core/*.patch

3. Branding dosyalarını yerleştir
   └── branding/ → chromium/chrome/app/theme/

4. GN flags yaz (gizlilik + performans)
   └── scripts/build.py --generate-flags

5. Derleme (ninja)
   └── ninja -C out/Sipar chrome
   └── ~4 saat, 8 core ile

6. Paketleme
   └── Windows: NSIS installer (.exe)
   └── Linux: .tar.xz + .deb + .AppImage
   └── macOS: .dmg

7. GitHub Release
   └── scripts/release.py
   └── Otomatik changelog
```

### GitHub Actions — Otomatik Build

Her `v*` tag push'unda tetiklenir:

```yaml
on:
  push:
    tags: ['v*']
```

Paralel build: Windows + Linux aynı anda.
Release oluşturulur, binary'ler eklenir, changelog otomatik.

### Disk & RAM Gereksinimleri

| Platform | Disk | RAM | CPU |
|----------|------|-----|-----|
| Windows | 100 GB | 16 GB | 8+ core |
| Linux | 80 GB | 16 GB | 8+ core |
| GitHub Actions | ✅ Runner üstlenip | bedava | (2000 dk/ay) |

---

## 7. Faz Planı — Detaylı {#fazlar}

### 🔵 Faz 0 — Temel Altyapı (TAMAMLANDI ✅)

| Görev | Durum |
|-------|-------|
| GitHub repo | ✅ |
| Proje iskeleti | ✅ |
| Build scripts | ✅ |
| CI/CD pipeline | ✅ |
| Landing page | ✅ |
| Waitlist backend | ✅ |
| New Tab prototipi | ✅ |
| Logo v1 | ✅ |
| Lucide icon sistemi | ✅ |
| TR/EN dil desteği | ✅ |

---

### 🟡 Faz 1 — MVP (Hafta 1-2)

**Hedef:** İndirilebilir, çalışan, branded bir Sipar Binary

| Görev | Öncelik | Süre |
|-------|---------|------|
| Build ortamı kur (GitHub Actions) | 🔴 Kritik | 1 gün |
| Branding patch'ini tamamla (gerçek dosyalar) | 🔴 Kritik | 2 gün |
| İkon seti oluştur (16-512px) | 🔴 Kritik | 1 gün |
| Default settings patch'ini test et | 🔴 Kritik | 1 gün |
| İlk Windows build al | 🔴 Kritik | 1 gün (CI'da) |
| İlk Linux build al | 🟠 Önemli | 1 gün (CI'da) |
| uBlock Origin yerleşik entegre et | 🔴 Kritik | 2 gün |
| sipar.io domain al | 🟠 Önemli | Para gelince |
| v0.1.0 GitHub Release | 🔴 Kritik | CI otomatik |

---

### 🟠 Faz 2 — Kimlik (Hafta 3-6)

**Hedef:** Sipar kendine has bir tarayıcı gibi hissettiriyor

| Görev | Öncelik | Süre |
|-------|---------|------|
| New Tab sayfasını Chromium'a entegre et | 🔴 Kritik | 3 gün |
| Privacy Shield UI (adres çubuğu popup) | 🔴 Kritik | 5 gün |
| sipar://settings sayfası | 🟠 Önemli | 1 hafta |
| Gizlilik seviye slider'ı | 🟠 Önemli | 3 gün |
| Onboarding (ilk açılış rehberi) | 🟠 Önemli | 3 gün |
| Türkçe dil desteği (tarayıcı içi) | 🟡 Normal | 2 gün |
| Tema sistemi (Dark/Light) | 🟡 Normal | 3 gün |
| macOS build | 🟡 Normal | CI'a ekle |
| sipar.io landing page taşınması | 🟡 Normal | 1 gün |
| v0.2.0 Public Beta | 🔴 Kritik | — |

---

### 🟢 Faz 3 — Premium Özellikler (Ay 2-3)

**Hedef:** Sürdürülebilir gelir modeli, güçlü özellikler

| Görev | Öncelik | Süre |
|-------|---------|------|
| Sipar Sync backend (E2E şifreli) | 🔴 Kritik | 2 hafta |
| Sync: yer imi, şifre, ayar | 🔴 Kritik | 1 hafta |
| Stripe ödeme entegrasyonu | 🔴 Kritik | 3 gün |
| Kullanıcı hesabı sistemi | 🔴 Kritik | 1 hafta |
| Sipar VPN (WireGuard) | 🟠 Önemli | 3 hafta |
| Aile paketi (5 cihaz) | 🟡 Normal | 1 hafta |
| v1.0.0 Stable | 🔴 Kritik | — |

---

### 🔵 Faz 4 — Ekosistem (Ay 3+)

**Hedef:** Topluluk, büyüme, mobil

| Görev | Öncelik | Süre |
|-------|---------|------|
| Bağımsız güvenlik auditi | 🔴 Kritik | 1 ay |
| Şeffaflık raporu yayınla | 🟠 Önemli | 1 gün |
| Sipar Shield Store (topluluk filtreleri) | 🟡 Normal | 2 hafta |
| Android yol haritası | 🟡 Normal | 6 ay+ |
| Çoklu dil (Arapça, Kürtçe, Farsça) | 🟡 Normal | 2 hafta |
| Blog: teknik yazılar | 🟡 Normal | Sürekli |

---

## 8. Gelir Modeli {#gelir}

### Fiyatlandırma (Faz 3'te açılır)

| Plan | Fiyat | İçerik |
|------|-------|--------|
| **Temel** | Ücretsiz | Tam tarayıcı, tüm gizlilik özellikleri |
| **Sync** | 3$/ay · 28$/yıl | E2E senkronizasyon, 5 cihaz |
| **Pro** | 6$/ay · 55$/yıl | Sync + VPN (WireGuard, 5 konum) |
| **Aile** | 9$/ay · 80$/yıl | Pro özellikleri, 5 kullanıcı hesabı |

### Neden Bu Model?

- Temel tarayıcı **her zaman ücretsiz** — gizlilik bir ücret gerektirmemeli
- Premium özellikler isteğe bağlı, zorla satış yok
- Reklam yok, kullanıcı verisi satışı yok
- Şeffaf: "Nasıl para kazanıyorsunuz?" sorusunun cevabı net

### Alternatif Gelir Kaynakları

- **Bağış**: GitHub Sponsors, OpenCollective
- **Kurumsal lisans**: Şirketlere toplu lisans (50+ kullanıcı)
- **Özel dağıtım**: Şirketlere özel konfigürasyon hizmeti

---

## 9. Dağıtım & Güncelleme {#dagitim}

### Dağıtım Kanalları

| Kanal | Platform | Öncelik |
|-------|----------|---------|
| sipar.io direkt indirme | Windows/Linux/Mac | 🔴 Birincil |
| GitHub Releases | Windows/Linux/Mac | 🔴 Birincil |
| winget (Windows) | Windows | 🟠 Faz 2 |
| Homebrew (Mac) | macOS | 🟠 Faz 2 |
| .deb / .rpm / AUR | Linux | 🟠 Faz 2 |
| Flathub (Flatpak) | Linux | 🟡 Faz 3 |

### Güncelleme Sistemi

Chromium'un kendi güncelleme mekanizması kaldırıldı. Sipar kendi güncelleme sistemini kullanır:

```
1. Başlangıçta (veya günde 1 kez): sipar.io/api/version kontrol
2. Yeni sürüm var mı? → Bildirim göster (zorla değil)
3. Kullanıcı onayıyla indir
4. Arka planda sessiz güncelleme
5. Yeniden başlat
```

Güncelleme sunucusu: Hetzner VPS (halihazırda var)

---

## 10. Topluluk & Büyüme {#topluluk}

### Launch Stratejisi

**Faz 1 (Şimdi — Beta öncesi):**
- sipar.huseyinbozkurt.com waitlist toplama
- Reddit duyurusu: r/privacy, r/de_privatize, r/turkey
- Twitter/X: @sipar_browser hesabı aç
- SiberBakış'ta tanıtım yazısı
- GitHub'da star kampanyası

**Faz 2 (Beta):**
- Product Hunt launch
- HackerNews "Show HN" post
- YouTube review'larına ulaş
- Privacy odaklı Discord/Telegram grupları

**Faz 3 (v1.0):**
- Basın bülteni (Türk tech medyası)
- Siber güvenlik konferansları (BSIDES İstanbul vs.)
- Bağımsız güvenlik audit raporu yayınla

### Topluluk Kanalları

- GitHub Issues — bug bildirimi, özellik isteği
- GitHub Discussions — genel tartışma
- Discord sunucusu (Faz 2)
- sipar.io/blog — şeffaflık raporları, teknik yazılar

---

## Özet: Sipar'ı Diğerlerinden Ayıran 5 Şey

1. **Sıfır uzlaşma**: Telemetry, reklam, kripto — hiçbiri. Asla.
2. **Herkes için**: 60 yaşındaki anne de kullanabilir. Teknik bilgi gerekmez.
3. **Türkçe öncelik**: Türk kullanıcılar, Türk tehdit modeli, Türkçe arayüz.
4. **Kanıtlanabilir gizlilik**: "Güven bize" değil, "Koda bak."
5. **Sürdürülebilir**: Reklam değil, kullanıcı desteğiyle ayakta durur.

---

*Bu belge yaşayan bir dokümandır. Her faz sonunda güncellenir.*

*Son güncelleme: 2026-03-30*
