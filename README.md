# Türkiye İl Notları

Türkiye il haritası üzerinden **kitap notu** tutan, Raspberry Pi 5 / Home Assistant OS
üzerinde Docker ile çalışan küçük bir web uygulaması.

İle dokunursunuz, o il için kitap adı ve notunuzu yazarsınız. Kaydı olmayan iller
gri kalır; ilk kitap girildiğinde il kendi rengine boyanır.

![Uygulama ikonu](static/icons/icon-192.png)

## Özellikler

- **81 il** — tıklanabilir/dokunulabilir SVG harita, harici harita servisi veya CDN yok
- **Gri → renkli** — notu olmayan il gri, kayıt girilen il kendi rengine boyanır, üstünde kayıt sayısı rozeti
- **İki renk modu** — “Her il farklı renk” ve “Kitap yoğunluğu” (ısı haritası + efsane)
- **İl başına birden fazla kayıt** — kitap adı + isteğe bağlı not + tarih, tek tek silinebilir
- **Kitap adı otomatik tamamlama** — daha önce girilen kitaplar öneri olarak gelir
- **İl arama** — yazıp Enter'a basınca o ile yakınlaşır ve panelini açar
- **iPad uygulaması gibi** — ana ekrana eklenince tam ekran açılır (PWA), çift parmak pinch-zoom,
  tek parmak kaydırma, 44px dokunma hedefleri, çentik/safe-area uyumu, çevrimdışı önbellek
- **Bağımlılık yok** — Chart.js/Leaflet vb. kullanılmaz; harita GeoJSON'dan tarayıcıda çizilir,
  dolayısıyla Pi'de internet olmasa da çalışır

## Portainer ile kurulum

Portainer → **Stacks → Add stack → Repository**

| Alan | Değer |
|------|-------|
| Repository URL | bu reponun URL'si |
| Repository reference | `refs/heads/main` |
| Compose path | `docker-compose.yml` |

**Deploy the stack** deyin. Ardından arayüz: `http://<raspberry-pi-ip>:5000`

## iPad'e kısayol ekleme

1. Safari ile `http://<raspberry-pi-ip>:5000` adresini açın
2. Paylaş → **Ana Ekrana Ekle**
3. Kısayol, tam ekran uygulama olarak açılır (Safari arayüzü görünmez)

> Çevrimdışı önbellek (service worker) yalnızca HTTPS veya `localhost` üzerinden etkinleşir.
> Düz `http://<ip>:5000` adresinde uygulama normal çalışır, sadece çevrimdışı desteği devre dışı kalır.

## Manuel kurulum

```bash
docker compose up -d --build
```

## Veri kalıcılığı

SQLite veritabanı konteyner içinde `/data/notlar.db` yolundadır ve `il-notlari-data`
adlı named volume'a bağlıdır; stack yeniden kurulsa bile kayıtlar korunur.

Yedek almak için:

```bash
docker cp turkiye-il-notlari:/data/notlar.db ./notlar-yedek.db
```

Ya da tüm kayıtları JSON olarak: `http://<pi-ip>:5000/api/export`

## Yerel geliştirme

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
DB_PATH=./notlar.db python app.py
```

> macOS'ta 5000 numaralı portu AirPlay Receiver kullanır; test için
> `DB_PATH=./notlar.db flask --app app run --port 5055` kullanabilirsiniz.

## Veritabanı şeması

`notes` tablosu:

| Sütun | Tip | Açıklama |
|-------|-----|----------|
| `id` | INTEGER | Birincil anahtar |
| `province` | TEXT | İl adı (zorunlu) |
| `province_code` | INTEGER | Plaka kodu |
| `book` | TEXT | Kitap adı (zorunlu) |
| `text` | TEXT | Not (isteğe bağlı) |
| `timestamp` | TEXT | `YYYY-MM-DD HH:MM:SS` |

## HTTP uçları

| Yöntem | Yol | Açıklama |
|--------|-----|----------|
| GET | `/` | Harita arayüzü |
| GET | `/api/summary` | `{ "İl": kayıt_sayısı }` — haritayı renklendirmek için |
| GET | `/api/notes?province=X` | O ilin kayıtları (yeniden eskiye) |
| POST | `/api/notes` | Kayıt ekler — `{province, province_code, book, text}` |
| DELETE | `/api/notes/<id>` | Kaydı siler |
| GET | `/api/books` | Girilmiş kitap adları (otomatik tamamlama) |
| GET | `/api/export` | Tüm kayıtlar (yedekleme) |

## İkonlar

`static/icons/` altındaki ikonlar (açık kitap + içinde renkli Türkiye haritası)
`tools/ikon_uret.py` ile üretilir:

```bash
pip install pillow
python tools/ikon_uret.py
```

## Notlar ve kaynaklar

- Zaman dilimi `docker-compose.yml` içindeki `TZ` değişkeniyle ayarlanır (varsayılan `Europe/Istanbul`).
- Uygulama Flask'ın geliştirme sunucusuyla çalışır — ev ağında kullanım için yeterlidir, internete açmayın.
- İl sınırı verisi: [alpers/Turkey-Maps-GeoJSON](https://github.com/alpers/Turkey-Maps-GeoJSON),
  Apache-2.0 lisanslı. Ayrıntı: [`static/tr-cities.SOURCE.txt`](static/tr-cities.SOURCE.txt)
