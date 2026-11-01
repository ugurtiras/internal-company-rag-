---
doc_id: INFRA-005
baslik: Nöbet (On-Call) Düzeni ve Devir Teslim
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Altyapı
erisim: muhendislik
versiyon: 1.4
yururluk_tarihi: 2025-09-08
---

# Nöbet (On-Call) Düzeni ve Devir Teslim

## 1. Amaç ve kapsam
Bu doküman, Altyapı SRE ekibinin nöbet düzenini ve devir teslim kurallarını teknik açıdan tanımlar. Çalışma saatleri, dinlenme ve prim konuları Vardiya ve Nöbet Çalışma Kuralları'ndadır (IK-008).

## 2. Düzen
- Nöbet haftalıktır. Her hafta bir **birincil** ve bir **ikincil** nöbetçi atanır.
- Nöbet çizelgesi PagerDuty üzerinden yönetilir ve her çeyrek başında 3 ay için ilan edilir.
- Nöbet devri her **Pazartesi 10:00**'da yapılır.

## 3. Alarm yönlendirme
1. Alarm önce birincil nöbetçiye gider. Nöbetçi **5 dakika** içinde yanıt vermelidir.
2. Yanıt gelmezse alarm ikincil nöbetçiye yönlenir.
3. **10 dakika** içinde yanıt gelmezse alarm Altyapı Müdürü'ne yönlenir.

Nöbetçi, alarm sonrası 15 dakika içinde VPN ile bağlanıp çalışmaya başlayabilecek durumda olmalıdır.

## 4. Olay yönetimi
Olay seviyeleri ve müdahale adımları Olay Müdahale Prosedürü'ndedir (INFRA-004). SEV1 ve SEV2 olaylarında nöbetçi, durum güncellemelerini her 30 dakikada bir yazar.

## 5. Devir teslim
Nöbetçi, nöbet haftasının sonunda devir notunu #infra-oncall kanalına yazar. Notta açık olaylar, süren riskler, alarm ayarı değişiklikleri ve takip edilmesi gereken işler yer alır.

## 6. Nöbet takası
Takas, en az 2 iş günü önceden ve yönetici onayıyla PagerDuty üzerinden yapılır.

## 7. Dinlenme
Gece saatlerinde SEV1 müdahalesi yapan nöbetçi ertesi gün saat 11:00'e kadar izinli sayılır.

## 8. İletişim
Slack: #infra-oncall, infra@penguincloud.example
