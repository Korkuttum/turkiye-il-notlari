# Türkiye İl Notları

Türkiye il haritası üzerinden kitap notu tutmanızı sağlayan eklenti.

## Kullanım

Sol menüdeki **İl Notları**'na tıklayın. Haritada bir ile dokunduğunuzda ortada bir
pencere açılır; **kitap adını** (zorunlu) ve isterseniz bir **not** girip **Ekle** deyin.

- Kaydı olmayan iller **gri** kalır, ilk kitap girildiğinde il kendi rengine boyanır
- İlin üstündeki rozet o ildeki kitap sayısını gösterir
- Sağ alttaki palet düğmesi renklendirmeyi **kitap yoğunluğu** ısı haritasına çevirir
- Çift parmakla yakınlaştırıp tek parmakla kaydırabilirsiniz

## Erişim

- **Sol menüden** (ingress) — Home Assistant girişiyle korunur, uzaktan da çalışır
- **Doğrudan porttan** — `http://<ha-ip>:5000`. Bu yolda kimlik doğrulama **yoktur**;
  istemiyorsanız eklenti ayarlarından port alanını boşaltın, sadece sol menüden açılsın.

iPad'de tam ekran uygulama gibi kullanmak için doğrudan port adresini Safari'de açıp
**Paylaş → Ana Ekrana Ekle** deyin.

## Veriler

Kayıtlar eklentinin `/data/notlar.db` dosyasında (SQLite) tutulur ve eklenti
güncellemelerinde korunur. Tüm kayıtları yedeklemek için `/api/export` adresini açın.
