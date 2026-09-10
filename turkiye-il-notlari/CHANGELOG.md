# Değişiklikler

## 1.0.4

- **Tüm Kitaplar listesi** eklendi. Sağ alttaki liste düğmesiyle açılır; her kayıt tek
  satırda görünür (il rengi, kitap adı, il, tarih, sil).
- Kitap veya il adına göre arama
- İki sıralama: **A → Z** (varsayılan, Türkçe harf sırasına göre) ve **Yeniden eskiye**
- Bir satıra dokununca liste kapanır, harita o ile yakınlaşır ve ilin penceresi açılır

## 1.0.3

- Derleme hatası giderildi (`pip: not found`). `build.yaml` içindeki `python:3.11-slim`
  Supervisor'ın beklediği `ad/imaj` kalıbına uymadığı için reddediliyor, HA kendi Alpine
  tabanlı varsayılan imajına düşüyordu. Kullanımdan kalkmış `build.yaml` kaldırıldı,
  temel imaj doğrudan Dockerfile'a yazıldı.

## 1.0.2

- Eklenti mağazada görünmüyordu: `image: null` alanı kaldırıldı. Yerelde derlenen
  eklentilerde bu alan hiç bulunmamalı, `null` değeri şema doğrulamasını düşürüyordu.

## 1.0.1

- Kaydı olmayan iller daha koyu gri: eski ton deniz rengine çok yakındı, harita seçilmiyordu

## 1.0.0

- İlk sürüm: Türkiye il haritası üzerinden kitap notu tutma
- Home Assistant eklentisi olarak paketlendi (Supervisor yönetir, ingress destekler)
- Sol menüden ingress ile, istenirse 5000 portundan doğrudan erişim
- Veriler `/data/notlar.db` içinde kalıcı
