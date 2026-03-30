# Sipar Browser — Tüm Özellikler Listesi

*Hüseyin onaylı tam özellik seti — 2026-03-30*

---

## ✅ v1.0.0-beta (Bu gece build alınıyor)

- Sıfır telemetri (Ungoogled-Chromium base)
- Pencere adı, about sayfası, profil klasörü → Sipar branded
- **Sipar Shield** (uBlock rebrand) — toolbar'da kalkan
- DNS-over-HTTPS (Quad9 9.9.9.9)
- 3rd party cookie varsayılan kapalı
- Brave Search varsayılan
- Özel New Tab sayfası (saat, arama, kısayollar, tracker sayacı)
- Google Safe Browsing kapalı
- Google Translate kapalı

---

## 🔜 v1.1.0 (2 Hafta)

- **sipar://settings** — 9 bölüm, Brave'in 20+ maddesine karşı
- **Privacy Shield Popup** — adres çubuğu kalkan butonu + popup
  - Master on/off toggle
  - Reklam / tracker / betik sayacı
  - Per-site override
- **Onboarding** — 3 adım (default browser, import, arama motoru)
- **Türkçe arayüz** — tam Türkçe dil desteği

---

## 🔜 v1.2.0 (1 Ay)

### AI Asistan — Kendi Key'ini Gir ⭐
```
Sağ panelde chat kutusu:
- OpenAI API key → ChatGPT
- Anthropic API key → Claude  
- Yerel → Ollama (Llama/Mistral, internet bağlantısı gerekmez)

Özellikler:
- Sayfa içeriğini özetle (1 tıkla)
- Seçili metni açıkla/çevir
- Kod yardımı
- VERİ DIŞ ÇIKMAZ — direkt kendi API'ne gider
```

### Tracker Aylık Raporu
```
"Mart 2026'da:
✅ 12,400 tracker engellendi
⏱️  Tahminen 3.2 saat kazandın
📦 870 MB data tasarrufu
💰 Tahminen $4.20 reklam geliri engelledik"
```

### Cookie Vault
- "Sadece bu oturum için" modu
- Tarayıcı kapanınca çerezler silinir
- Whitelist: Netflix, Gmail kalıcı kalsın

### Privacy Score Kartı
- Her site için 0-10 puan
- "Bu site seni 7.2/10 izliyor"
- Canvas fingerprinting tespiti

---

## 🔜 v2.0.0 (3 Ay)

### Session Container (Sekme İzolasyonu)
```
Her sekmeye renk/profil:
🔴 İş    🔵 Kişisel    🟢 Alışveriş
Amazon çerezleri Facebook'a sızmaz.
Sürükle-bırak ile organize et.
```

### Sipar Sync (Zero-Knowledge)
- QR kod ile cihazlar arası sync
- Sunucumuz GÖRMEZ (E2E şifreli)
- Yer imi, şifre, ayar, sekme grubu

### Geçmiş Temizleme Modları
- Standart: normal
- Oturum Modu: sekme kapanınca her şey silinir
- Misafir Modu: hiç iz bırakmaz (RAM'de)
- Paranoyak Mod: şifreli + Tor

### macOS Build
- Universal binary (Intel + Apple Silicon)

---

## 🔜 v2.5.0 (6 Ay)

### Sipar VPN (WireGuard)
- No-log, bağımsız audit edilmiş
- Kill switch (VPN düşünce internet kesilir)
- DNS leak koruması
- 5+ lokasyon

### Tor Sekme
- Sağ tık → "Tor üzerinden aç"
- Ayrı program gerekmez

### Bağımsız Güvenlik Auditi
- Şeffaflık raporu yayınla
- "Güven bize" değil, "Koda bak"

### Android Yol Haritası

---

## 🔜 v3.0.0 (1 Yıl)

### Premium Plan
| Plan | Fiyat | İçerik |
|------|-------|--------|
| Temel | Ücretsiz | Tüm tarayıcı, gizlilik |
| Sync | 3$/ay | E2E Sync, 5 cihaz |
| Pro | 6$/ay | Sync + VPN |
| Aile | 9$/ay | Pro, 5 kullanıcı |

### Ekosistem
- Sipar Shield Store (topluluk filtreleri)
- Blog + şeffaflık raporları
- Çoklu dil (Arapça, Kürtçe, Farsça)
- iOS araştırması

---

## Rakip Analizi

| Özellik | Sipar | Brave | Firefox | Chrome |
|---------|-------|-------|---------|--------|
| Sıfır telemetri | ✅ | ⚠️ | ⚠️ | ❌ |
| Kendi AI key'i | ✅ | ❌ | ❌ | ❌ |
| Kripto/BAT yok | ✅ | ❌ | ✅ | ✅ |
| Session container | ✅ | ❌ | ✅ | ❌ |
| VPN dahil | ✅ (Pro) | ✅ (ücretli) | ❌ | ❌ |
| Zero-knowledge sync | ✅ | ❌ | ❌ | ❌ |
| Tracker raporu | ✅ | ✅ | ❌ | ❌ |
| Tor sekme | ✅ | ✅ | ❌ | ❌ |
| Açık kaynak | ✅ | ✅ | ✅ | ⚠️ |
| Türkçe öncelik | ✅ | ❌ | ❌ | ❌ |

---

*"Brave'den saf. Chrome'dan özgür. Sadece tarayıcı."*
