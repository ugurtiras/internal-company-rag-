---
doc_id: INFRA-002
baslik: Üretim Deploy ve Sürüm Politikası
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Altyapı
erisim: muhendislik
versiyon: 2.0
yururluk_tarihi: 2025-08-01
---

# Üretim Deploy ve Sürüm Politikası

## 1. Amaç ve kapsam
Bu politika, Penguin Cloud'un iç sistemlerine ve müşteri ortamlarını yöneten platform bileşenlerine yapılan üretim (production) deploy'larının kurallarını belirler. Altyapı ekibinin tüm üyeleri için geçerlidir. Müşteri etkili bakımlar Değişiklik Yönetimi ve Bakım Penceresi dokümanında ayrıca düzenlenmiştir (INFRA-003).

## 2. Deploy zamanı
- Üretim deploy'ları yalnızca **iş günlerinde 10:00–16:00** arasında yapılır.
- **Cuma günleri deploy yapılmaz.**
- Değişiklik dondurma döneminde (15 Aralık – 5 Ocak) deploy yapılmaz. Acil düzeltmeler yalnızca Altyapı Müdürü onayıyla yapılabilir.

## 3. Deploy öncesi koşullar
1. Değişiklik, en az bir ekip üyesi tarafından kod incelemesinden (code review) geçmiş olmalıdır. Kritik servislerde (API ağ geçidi, kimlik doğrulama, yedekleme) 2 onay gerekir.
2. Otomatik testler (CI) başarıyla tamamlanmış olmalıdır.
3. Geri alma (rollback) planı yazılı olmalıdır.

## 4. Deploy yöntemi
- Sürümler önce **canary** olarak trafiğin %10'una açılır ve 30 dakika izlenir. Hata oranı ve gecikme normal kalırsa tam dağıtım yapılır.
- Sürümler semantik versiyon numarası (ana.ikincil.yama) ile etiketlenir.
- Deploy sonrası 60 dakika boyunca ilgili Grafana panosu izlenir. İzleme standartları INFRA-006'dadır.

## 5. Geri alma
Deploy sonrası sorun çıkarsa ve son deploy 2 saatten yeni ise önce geri alma değerlendirilir. Geri alma kararını nöbetçi mühendis verir. Olay açılırsa Olay Müdahale Prosedürü uygulanır (INFRA-004).

## 6. Kayıt
Her deploy; sürüm numarası, yapan kişi, zaman ve sonuçla birlikte deploy kaydına yazılır.

## 7. İletişim
Altyapı: infra@penguincloud.example, Slack: #infra
