---
doc_id: INFRA-010
baslik: Felaket Kurtarma Planı (RPO/RTO)
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Altyapı
erisim: muhendislik
versiyon: 1.7
yururluk_tarihi: 2026-03-02
---

# Felaket Kurtarma Planı

## 1. Amaç ve kapsam
Bu plan, ana veri merkezi bölgesinin kullanılamaz hale gelmesi durumunda hizmetlerin ikincil bölgede nasıl yeniden ayağa kaldırılacağını tanımlar. Yedekleme detayları INFRA-007'dedir. Şirket genelindeki kriz yönetimi yapısı YON-005'te tanımlıdır.

## 2. Kurtarma hedefleri
| Paket | RPO (kabul edilebilir veri kaybı) | RTO (geri dönüş süresi) |
|---|---|---|
| Standart | 24 saat | 8 saat |
| Gelişmiş | 4 saat | 4 saat |
| Kurumsal | 1 saat | 1 saat |

## 3. Felaket ilanı
- Felaket ilanı yetkisi **Altyapı Müdürü**'ndedir. Müdür ulaşılamıyorsa yetki Genel Müdür Yardımcısı'na geçer.
- Felaket durumu SEV1 olarak yönetilir. Müşteri bilgilendirmesi 15 dakika içinde yapılır (INFRA-004).

## 4. Kurtarma sırası
Hizmetler ikincil bölgede şu sırayla geri getirilir:
1. Kurumsal paket müşterileri
2. Gelişmiş paket müşterileri
3. Standart paket müşterileri

Her aşama için hedef, ilgili paketin RTO süresidir.

## 5. Kurtarma adımları
1. İkincil bölgedeki altyapı şablonlarından kaynaklar oluşturulur.
2. En son yedek veya anlık görüntüden veriler geri yüklenir.
3. DNS ikincil bölgeye yönlendirilir.
4. Servis sağlığı doğrulanır ve Destek ekibine bilgi verilir.

## 6. Tatbikat
Felaket kurtarma tatbikatı yılda 2 kez, **Nisan** ve **Ekim** aylarında yapılır. Tatbikat sonuç raporu 10 iş günü içinde hazırlanır. RPO veya RTO hedefi tutturulamazsa aksiyon planı çıkarılır.

## 7. İletişim
Altyapı: infra@penguincloud.example
