---
doc_id: INFRA-007
baslik: Yedekleme ve Saklama Prosedürü
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Altyapı
erisim: muhendislik
versiyon: 2.1
yururluk_tarihi: 2025-05-19
---

# Yedekleme ve Saklama Prosedürü

## 1. Amaç ve kapsam
Bu prosedür, Penguin Yedek hizmeti kapsamındaki müşteri verilerinin ve şirket sistemlerinin yedekleme, saklama ve geri yükleme kurallarını tanımlar. Felaket durumundaki toplam kurtarma planı INFRA-010'dadır.

## 2. Yedekleme sıklığı
- **Günlük artımlı yedek:** her gün 01:00
- **Haftalık tam yedek:** her Pazar 02:00
- Gelişmiş pakette ek olarak 4 saatte bir, Kurumsal pakette saatlik anlık görüntü (snapshot) alınır. Anlık görüntüler 7 gün saklanır.

Bu sıklıklar paketlerin kayıp kabul edilebilir süresi (RPO) ile uyumludur: Standart 24 saat, Gelişmiş 4 saat, Kurumsal 1 saat.

## 3. Saklama
Günlük ve haftalık yedekler **30 gün** saklanır. Yedekler AES-256 ile şifrelenir ve farklı bir bölgedeki depolamaya da kopyalanır.

## 4. İzleme
Yedekleme işleri izlenir. Art arda 2 başarısız yedek kritik alarm üretir (INFRA-006). Başarısız yedek, 24 saat içinde yeniden çalıştırılır.

## 5. Geri yükleme testi
Her ay rastgele seçilen bir müşteri ortamı için geri yükleme testi yapılır ve sonucu kayda geçirilir. Müşteri talebiyle yapılan geri yükleme, müşteri kimlik doğrulaması tamamlandıktan sonra başlar.

## 6. İletişim
Altyapı: infra@penguincloud.example
