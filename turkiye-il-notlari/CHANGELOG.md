# Değişiklikler

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
