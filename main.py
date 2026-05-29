import json
import random
import os
import datetime

# 1. Seri Sistemi ve Tarih Kontrolü
if not os.path.exists("durum.json"):
    with open("durum.json", "w") as f:
        json.dump({"seri_gun": 0, "son_oynama_tarihi": ""}, f)

with open("durum.json", "r") as f:
    durum = json.load(f)

bugun = str(datetime.date.today())
son_tarih = durum.get("son_oynama_tarihi", "")

# Tarih kontrolü: Eğer bugün henüz oynamadıysan seriyi güncelle
if son_tarih != bugun:
    dunku_tarih = str(datetime.date.today() - datetime.timedelta(days=1))
    
    if son_tarih == dunku_tarih:
        durum["seri_gun"] += 1
    else:
        durum["seri_gun"] = 1 # Seri bozulmuş, yeniden başla
    
    durum["son_oynama_tarihi"] = bugun
    with open("durum.json", "w") as f:
        json.dump(durum, f)

print(f"Harika! {durum['seri_gun']}. günündesin. Serini koruyorsun!")

# 2. Veritabanını Yükle
with open("kelimeler.json", "r", encoding="utf-8") as f:
    kategoriler = json.load(f)

# 3. Kategori Seçimi
print("\n--- ZİNDANLAR ---")
for kat in kategoriler.keys():
    print("- " + kat)

secim = input("\nHangi kategoriye girmek istersin? ")

if secim in kategoriler:
    sozluk = kategoriler[secim]
    kalan_kelimeler = list(sozluk.items())
    can = 3
    hatali_kelimeler = {}

    print(f"\n{secim} zindanına girdin!")

    # 4. Oyun Döngüsü
    while can > 0 and len(kalan_kelimeler) > 0:
        rusca, turkce = random.choice(kalan_kelimeler)
        cevap = input(f"'{rusca}' nedir? ")
        
        if cevap.lower() == turkce:
            print("Doğru!")
            kalan_kelimeler.remove((rusca, turkce))
        else:
            can -= 1
            hatali_kelimeler[rusca] = turkce
            print(f"Yanlış! Canın azaldı: {can}")

    # 5. Bitiriş
    print(f"\nOyun bitti! Bugün {durum['seri_gun']}. günündesin.")
    if hatali_kelimeler:
        print("Tekrar etmen gerekenler:", hatali_kelimeler)
    else:
        print("Mükemmel! Hiç hata yapmadın.")
else:
    print("Böyle bir zindan bulunamadı!")