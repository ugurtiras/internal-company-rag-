---
doc_id: GUV-001
baslik: Bilgi Güvenliği ve Şifre Politikası
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Güvenlik ve BT
erisim: tum_calisanlar
versiyon: 3.0
yururluk_tarihi: 2025-02-10
---

# Bilgi Güvenliği ve Şifre Politikası

## 1. Amaç ve kapsam
Bu politika, şirket ve müşteri verilerinin, sistemlerinin ve cihazlarının korunması için uyulması gereken kuralları belirler. Tüm çalışanlar, stajyerler ve dış hizmet sağlayıcılar için geçerlidir.

## 2. Şifre kuralları
- Şifreler en az 12 karakter olmalı, büyük harf, küçük harf, rakam ve özel karakter içermelidir.
- Şifreler **90 günde bir** değiştirilir. Son 5 şifre tekrar kullanılamaz.
- Aynı şifre birden fazla iş sisteminde kullanılamaz.
- Şifreler paylaşılamaz. BT ekibi hiçbir koşulda şifre istemez.
- 5 hatalı giriş denemesinden sonra hesap 30 dakika kilitlenir.

## 3. Çok faktörlü doğrulama (MFA)
E-posta, İK Portalı, Masraf Portalı ve VPN için MFA zorunludur. Doğrulama kodları yalnızca şirketin onayladığı kimlik doğrulama uygulamasından alınır. SMS yalnızca yedek yöntemdir.

## 4. Cihaz güvenliği
1. Şirket bilgisayarlarında disk şifreleme açık olmalıdır ve kapatılamaz.
2. Ekran 5 dakika hareketsizlikte otomatik kilitlenir.
3. USB bellek varsayılan olarak engellidir. İş gereği kullanım için BT portalından talep açılır.
4. Yazılım kurulumları yalnızca BT'nin onayladığı listeden yapılır.
5. Kişisel cihazlardan şirket e-postasına yalnızca onaylı mobil uygulama ile erişilir.

## 5. Uzaktan erişim
Ofis dışından şirket sistemlerine erişim yalnızca şirket VPN'i ile yapılır. Uzaktan çalışma koşulları IK-005'tedir.

## 6. Oltalama ve şüpheli durumlar
- Şüpheli e-posta, bağlantı veya dosya fark eden çalışan **1 saat içinde** guvenlik@penguincloud.example adresine bildirimde bulunur.
- Şüpheli bağlantıya tıklanmışsa çalışan bilgisayarı ağdan çıkarır ve BT Destek hattını arar.
- Oltalama farkındalık eğitimi yılda 2 kez verilir ve yeni çalışanlar için oryantasyonun parçasıdır (IK-001).

## 7. Cihaz kaybı veya çalınması
Cihaz kaybolduğunda veya çalındığında çalışan **aynı gün** BT Destek hattına bildirimde bulunur. BT cihazı uzaktan kilitler ve verilerini siler. Üretim ortamını etkileyebilecek durumlar Olay Müdahale Prosedürü'ne göre yürütülür (INFRA-004).

## 8. BT destek talepleri
| Öncelik | Örnek | İlk yanıt süresi |
|---|---|---|
| Kritik | E-posta veya VPN erişimi yok | 1 saat |
| Yüksek | Tek kullanıcının hesabı kilitli | 4 saat |
| Normal | Yazılım kurulum talebi | 1 iş günü |

BT Destek hattı iş günlerinde 08:30–18:00 arasında hizmet verir.

## 9. İletişim
BT Destek: bt-destek@penguincloud.example, Güvenlik: guvenlik@penguincloud.example
