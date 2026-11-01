---
doc_id: INFRA-006
baslik: İzleme ve Alarm Standartları
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Altyapı
erisim: muhendislik
versiyon: 1.8
yururluk_tarihi: 2025-07-14
---

# İzleme ve Alarm Standartları

## 1. Amaç ve kapsam
Bu doküman, Penguin Cloud altyapısında hangi metriklerin izleneceğini ve alarmların hangi eşiklerle tetikleneceğini belirler. Tüm Altyapı çalışanları için geçerlidir.

## 2. Araçlar
Metrikler ve panolar Grafana üzerinden izlenir. Alarmlar PagerDuty ile nöbetçilere iletilir. Müşteri ortamları için sunulan Penguin İzle hizmeti aynı standartları kullanır.

## 3. Alarm seviyeleri ve eşikler
| Metrik | Eşik | Süre | Seviye |
|---|---|---|---|
| API hata oranı | %5 üzeri | 5 dakika | SEV2 olay açılır |
| API hata oranı | %20 üzeri | 5 dakika | SEV1'e yükselir |
| API gecikmesi (p95) | 800 ms üzeri | 10 dakika | Uyarı |
| CPU kullanımı | %85 üzeri | 15 dakika | Uyarı |
| Disk doluluk | %80 üzeri | Anlık | Uyarı |
| Disk doluluk | %90 üzeri | Anlık | Kritik |
| Yedekleme işi | 2 ardışık başarısızlık | Anlık | Kritik |
| Sertifika bitişi | 30 gün kala | Günlük kontrol | Uyarı |

Uyarı seviyesi alarmlar #infra kanalına yazılır. Kritik alarmlar nöbetçiye PagerDuty ile iletilir (INFRA-005). Olay seviyeleri ve müdahale adımları INFRA-004'tedir.

## 4. Alarm kalitesi
- Her alarmın bir müdahale rehberi (runbook) bağlantısı olmalıdır.
- Aksiyon gerektirmeyen alarmlar kapatılır veya eşikleri güncellenir. Nöbet devir notunda alarm ayarı değişiklikleri belirtilir.

## 5. Saklama
Metrikler 13 ay, loglar 90 gün saklanır.

## 6. İletişim
Altyapı: infra@penguincloud.example, Slack: #infra
