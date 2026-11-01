---
doc_id: INFRA-004
baslik: Üretim Ortamı Olay Müdahale (Incident) Prosedürü
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Altyapı
erisim: muhendislik
versiyon: 2.2
yururluk_tarihi: 2025-06-01
---

# Üretim Ortamı Olay Müdahale Prosedürü

## 1. Amaç ve kapsam
Bu prosedür, üretim ortamında yaşanan kesinti ve performans sorunlarında izlenecek adımları tanımlar. Tüm Altyapı çalışanları ve nöbetçi mühendisler için geçerlidir.

## 2. Olay seviyeleri
| Seviye | Tanım | İlk müdahale | Müşteri bilgilendirmesi |
|---|---|---|---|
| SEV1 | Tüm müşterileri etkileyen kesinti | 5 dakika | 15 dakika içinde |
| SEV2 | Bir özellik veya müşteri grubu etkileniyor | 15 dakika | 1 saat içinde |
| SEV3 | Müşteriyi etkilemeyen, izlenmesi gereken sorun | 4 saat | Gerekmez |

API hata oranı 5 dakika boyunca %5'in üzerinde kalırsa olay otomatik olarak SEV2 açılır. Hata oranı %20'yi aşarsa SEV1'e yükseltilir.

## 3. Müdahale adımları
1. **Doğrula:** Alarmın gerçek olduğunu Grafana panosu ve loglardan kontrol et (INFRA-006).
2. **Olayı aç:** #incidents kanalında başlık ve seviyeyi yaz, bir Olay Yöneticisi belirle. SEV1'de bu rol Altyapı Müdürü veya atadığı kişidir.
3. **Etkiyi sınırla:** Son 2 saat içinde deploy yapıldıysa önce geri alma değerlendirilir.
4. **Neden ara ve düzelt:** Kök neden araştırması, hizmeti geri getirmekten sonra gelir.
5. **Doğrula ve kapat:** Metrikler 15 dakika boyunca normal kalırsa olay kapatılır.

Kubernetes'te son sürüme dönmek için:

    kubectl rollout undo deployment/api-gateway -n production
    kubectl rollout status deployment/api-gateway -n production

Veritabanı geri yüklemesi yalnızca Altyapı Müdürü onayıyla yapılır.

## 4. İletişim
- SEV1 ve SEV2'de durum güncellemesi her **30 dakikada bir** #incidents kanalına yazılır.
- Müşteri bilgilendirmesini Destek ekibi durum sayfasından yapar, metin taslağını Altyapı sağlar.
- Olayda güvenlik ihlali şüphesi varsa süreç Güvenlik ve BT ile birlikte yürütülür (GUV-006, temel kurallar GUV-001).

## 5. Olay sonrası inceleme
SEV1 ve SEV2 olayları için **5 iş günü içinde** suçlamasız (blameless) bir postmortem yazılır. Şablon ve süreç INFRA-012'dedir.

## 6. İletişim
Altyapı: infra@penguincloud.example, Slack: #infra
