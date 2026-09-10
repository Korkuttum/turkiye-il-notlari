# Türkiye İl Notları — Home Assistant eklenti deposu

Türkiye il haritası üzerinden kitap notu tutan bir Home Assistant eklentisi.
İle dokunursunuz, açılan pencerede o il için kitap adı ve notunuzu kaydedersiniz.
Kaydı olmayan iller gri kalır; ilk kitap girildiğinde il kendi rengine boyanır.

## Kurulum

1. Home Assistant → **Ayarlar → Eklentiler → Eklenti Mağazası**
2. Sağ üstteki **⋮ → Depolar**
3. Şu adresi ekleyin:

   ```
   https://github.com/Korkuttum/turkiye-il-notlari
   ```

4. **Ekle** → pencereyi kapatın → sayfayı yenileyin
5. Listede **Türkiye İl Notları** çıkar → **Kur**
6. Kurulum bitince **Başlat**, ardından **Kenar çubuğunda göster** açık olsun

İlk kurulumda imaj cihazınızda derlenir; Raspberry Pi'de birkaç dakika sürebilir.

## Neden eklenti?

Home Assistant OS, Supervisor'ın yönetmediği konteynerleri "ekstra yazılım" sayar ve
kurulumu **Unsupported** işaretler. Eklenti olarak kurulduğunda Supervisor yönettiği için
bu sorun oluşmaz — ayrıca sol menüde kendi ikonuyla açılır ve ingress sayesinde uzaktan da
erişilebilir olur.

## Özellikler

- **81 il** — dokunmatik SVG harita, harici harita servisi veya CDN yok
- **iPad öncelikli arayüz** — ile dokununca ortada açılır pencere, büyük dokunma hedefleri,
  çift parmak pinch-zoom, tek parmak kaydırma, çentik/safe-area uyumu
- **İl başına birden fazla kitap** — tarihli, tek tek silinebilir, kitap adları otomatik tamamlanır
- **İki renk modu** — her il farklı renk / kitap yoğunluğu ısı haritası
- **Bağımlılık yok** — harita GeoJSON'dan tarayıcıda çizilir, internet olmadan da çalışır

## Home Assistant olmadan çalıştırmak

Depo kökündeki `docker-compose.yml` düz Docker kurulumları içindir:

```bash
docker compose up -d --build
```

> Home Assistant üzerinde bunu **kullanmayın** — yukarıdaki eklenti yolunu izleyin,
> aksi halde kurulumunuz Unsupported işaretlenir.

## Veritabanı şeması

`notes` tablosu:

| Sütun | Tip | Açıklama |
|-------|-----|----------|
| `id` | INTEGER | Birincil anahtar |
| `province` | TEXT | İl adı |
| `province_code` | INTEGER | Plaka kodu |
| `book` | TEXT | Kitap adı (zorunlu) |
| `text` | TEXT | Not (isteğe bağlı) |
| `timestamp` | TEXT | `YYYY-MM-DD HH:MM:SS` |

## HTTP uçları

| Yöntem | Yol | Açıklama |
|--------|-----|----------|
| GET | `/` | Harita arayüzü |
| GET | `/api/summary` | `{ "İl": kitap_sayısı }` |
| GET | `/api/notes?province=X` | O ilin kayıtları |
| POST | `/api/notes` | Kayıt ekler — `{province, province_code, book, text}` |
| DELETE | `/api/notes/<id>` | Kaydı siler |
| GET | `/api/books` | Girilmiş kitap adları |
| GET | `/api/export` | Tüm kayıtlar (yedekleme) |

## İkonlar

```bash
pip install pillow
python tools/ikon_uret.py
```

## Kaynaklar

İl sınırı verisi: [alpers/Turkey-Maps-GeoJSON](https://github.com/alpers/Turkey-Maps-GeoJSON),
Apache-2.0 lisanslı. Ayrıntı: [`turkiye-il-notlari/static/tr-cities.SOURCE.txt`](turkiye-il-notlari/static/tr-cities.SOURCE.txt)
