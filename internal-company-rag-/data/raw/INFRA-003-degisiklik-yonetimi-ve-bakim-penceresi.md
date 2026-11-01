---
doc_id: INFRA-003
baslik: Değişiklik Yönetimi ve Bakım Penceresi
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Altyapı
erisim: muhendislik
versiyon: 1.6
yururluk_tarihi: 2025-06-16
---

# Değişiklik Yönetimi ve Bakım Penceresi

## 1. Amaç ve kapsam
Bu doküman, müşteri hizmetlerini etkileyebilecek altyapı değişikliklerinin nasıl planlanıp onaylanacağını ve planlı bakım penceresini tanımlar. Günlük deploy kuralları INFRA-002'dedir.

## 2. Değişiklik türleri
| Tür | Tanım | Onay |
|---|---|---|
| Standart | Önceden onaylı, düşük riskli, tekrarlanan değişiklik | Ekip lideri |
| Normal | Müşteri etkisi olabilecek planlı değişiklik | Değişiklik Danışma Kurulu (CAB) |
| Acil | Süregiden bir olayı çözmek için yapılan değişiklik | Altyapı Müdürü |

## 3. Değişiklik Danışma Kurulu (CAB)
CAB her hafta **Çarşamba 14:00**'te toplanır. Normal değişiklik talepleri, toplantıdan en az 2 iş günü önce yazılı olarak sunulur. Talepte etki analizi, geri alma planı ve bakım süresi bulunmalıdır.

## 4. Planlı bakım penceresi
- Müşteri hizmetini etkileyen planlı bakımlar yalnızca her **Salı 02:00–05:00** arasında yapılır.
- Bakım, müşterilere **en az 5 iş günü önceden** duyurulur. Duyuru süreci INFRA-016'dadır.
- Bakım penceresinin aşılma ihtimali varsa, müşteriler pencere bitmeden 30 dakika önce bilgilendirilir.
- Planlı bakım süresi, SLA erişilebilirlik hesabına dahil edilmez.

## 5. Dondurma dönemi
15 Aralık – 5 Ocak arasında yalnızca acil değişikliklere izin verilir.

## 6. İletişim
Altyapı: infra@penguincloud.example
