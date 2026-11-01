---
doc_id: GUV-003
baslik: Erişim Yönetimi ve Yetkilendirme Politikası
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Güvenlik ve BT
erisim: muhendislik
versiyon: 1.5
yururluk_tarihi: 2025-05-12
---

# Erişim Yönetimi ve Yetkilendirme Politikası

## 1. Amaç ve kapsam
Bu politika, şirket sistemlerine ve müşteri ortamlarına erişimin nasıl verildiğini, izlendiğini ve geri alındığını düzenler. Altyapı ile Güvenlik ve BT çalışanları için geçerlidir. Sunucu ve Kubernetes erişiminin teknik ayrıntıları INFRA-009'dadır.

## 2. Temel ilkeler
- **En az yetki:** Çalışan yalnızca işi için gereken erişime sahip olur.
- Paylaşılan hesap kullanılamaz, her erişim kişiye özeldir.
- Yönetici yetkili hesaplar, günlük kullanım hesabından ayrıdır ve MFA ile korunur.

## 3. Erişim talebi
1. Talep, BT portalından açılır ve talep sahibinin yöneticisi onaylar.
2. Sistem sahibi (ilgili ekip lideri) ikinci onayı verir.
3. Üretim (production) ortamına erişim yalnızca Platform ve SRE ekiplerine verilir.

## 4. Geçici erişim
Acil durumlar için verilen geçici üretim erişimi en fazla **8 saat** geçerlidir ve süre sonunda otomatik kapanır. Erişimin gerekçesi olay numarasıyla kaydedilir.

## 5. Müşteri ortamına erişim
Müşteri ortamına yalnızca müşterinin destek talebi (ticket) üzerine ve talep numarası belirtilerek erişilir. Tüm erişim kayıtları 12 ay saklanır.

## 6. Periyodik gözden geçirme
Tüm yetkili erişimler 3 ayda bir gözden geçirilir. Kullanılmayan erişimler kaldırılır. SSH anahtarları 12 ayda bir yenilenir.

## 7. Ayrılma ve görev değişikliği
Çalışan ayrıldığında erişimleri çıkış günü saat 18:00'e kadar kapatılır. Görev değiştiren çalışanın eski yetkileri yeni göreve geçişte kaldırılır.

## 8. İletişim
Güvenlik: guvenlik@penguincloud.example
