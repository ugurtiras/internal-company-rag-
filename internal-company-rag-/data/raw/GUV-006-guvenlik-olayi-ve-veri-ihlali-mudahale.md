---
doc_id: GUV-006
baslik: Güvenlik Olayı ve Veri İhlali Müdahale Prosedürü
sirket: Penguin Cloud Teknoloji A.Ş.
departman: Güvenlik ve BT
erisim: muhendislik
versiyon: 2.0
yururluk_tarihi: 2025-11-03
---

# Güvenlik Olayı ve Veri İhlali Müdahale Prosedürü

## 1. Amaç ve kapsam
Bu prosedür, güvenlik olaylarında ve kişisel veri ihlali şüphesinde izlenecek adımları tanımlar. Altyapı ile Güvenlik ve BT çalışanları için geçerlidir.

## 2. Bildirim
Bir güvenlik olayı veya veri ihlali şüphesi fark eden herkes **1 saat içinde** Güvenlik ekibine (guvenlik@penguincloud.example) bildirimde bulunur. Güvenlik İzleme ekibi bildirimi kaydeder ve olay yöneticisini belirler. Olay yöneticisi Güvenlik ve BT Müdürü veya onun atadığı kişidir.

## 3. Müdahale adımları
1. **Doğrula ve sınıflandır:** Olayın gerçek olduğu ve hangi verileri etkilediği belirlenir.
2. **Sınırla:** Etkilenen hesaplar, cihazlar veya sistemler izole edilir.
3. **Delilleri koru:** Loglar ve disk görüntüleri silinmeden saklanır.
4. **Kök nedeni bul ve gider.**
5. **Normale dön:** Sistemler doğrulanarak servise geri alınır.

Olay üretim hizmetini de etkiliyorsa güvenlik süreci, Olay Müdahale Prosedürü ile eşzamanlı yürütülür (INFRA-004).

## 4. Kritik olaylarda bilgilendirme
Kritik seviyedeki güvenlik olaylarında Genel Müdür Yardımcısı **1 saat içinde** bilgilendirilir.

## 5. Kişisel veri ihlali ve yasal bildirim
- Hukuk, ihlali **24 saat içinde** değerlendirir.
- Bildirim gerekiyorsa KVKK Kurulu'na ve etkilenen müşterilere en geç **72 saat içinde** bildirim yapılır. Müşteri bildirim metni Hukuk onayıyla gönderilir.
- Yasal çerçeve KVKK ve Kişisel Veri İşleme Politikası'ndadır (HUK-004).

## 6. Olay sonrası
Olayın ardından 5 iş günü içinde olay raporu hazırlanır. Raporda zaman çizelgesi, kök neden, etki ve alınacak aksiyonlar yer alır. Olay kayıtları 5 yıl saklanır.

## 7. İletişim
Güvenlik: guvenlik@penguincloud.example
