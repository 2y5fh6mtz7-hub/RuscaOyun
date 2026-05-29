import streamlit as st
import json
import os
import datetime
import random
import pandas as pd

# 1. Seri Sistemi ve Veri Yükleme
def get_durum():
    if not os.path.exists("durum.json"):
        return {"seri_gun": 0, "son_oynama_tarihi": ""}
    with open("durum.json", "r") as f:
        return json.load(f)

def save_durum(durum):
    with open("durum.json", "w") as f:
        json.dump(durum, f)

# Oturum yönetimi
if "oyun_basladi" not in st.session_state:
    st.session_state.oyun_basladi = False

st.title("🇷🇺 Rusça Zindan Oyunu")

durum = get_durum()
bugun = str(datetime.date.today())
son_tarih = durum.get("son_oynama_tarihi", "")

# Seri kontrolü
if son_tarih != bugun:
    dunku_tarih = str(datetime.date.today() - datetime.timedelta(days=1))
    if son_tarih == dunku_tarih:
        durum["seri_gun"] += 1
    else:
        durum["seri_gun"] = 1
    durum["son_oynama_tarihi"] = bugun
    save_durum(durum)

st.sidebar.metric("Seri Günü", f"{durum['seri_gun']}")

# 2. Kategoriler
with open("kelimeler.json", "r", encoding="utf-8") as f:
    kategoriler = json.load(f)

# 3. Kategori Seçimi
kat = st.selectbox("Hangi zindana girmek istersin?", list(kategoriler.keys()))

if st.button("Zindana Gir"):
    st.session_state.oyun_basladi = True
    st.session_state.kalan_kelimeler = list(kategoriler[kat].items())
    st.session_state.hatali_kelimeler = {}
    st.session_state.can = 3
    st.rerun()

# 4. Oyun Döngüsü
if st.session_state.oyun_basladi:
    if st.session_state.can > 0 and len(st.session_state.kalan_kelimeler) > 0:
        rusca, turkce = random.choice(st.session_state.kalan_kelimeler)
        st.write(f"### Kalan Can: {st.session_state.can}")
        cevap = st.text_input(f"'{rusca}' nedir?", key="cevap_input")
        
        if st.button("Kontrol Et"):
            if cevap.lower() == turkce:
                st.success("Doğru!")
                st.session_state.kalan_kelimeler.remove((rusca, turkce))
                st.rerun()
            else:
                st.session_state.can -= 1
                st.session_state.hatali_kelimeler[rusca] = turkce
                st.error(f"Yanlış! Kalan can: {st.session_state.can}")
                if st.session_state.can <= 0:
                    st.rerun()
    else:
        st.write("---")
        st.write("Oyun Bitti!")
        if st.session_state.hatali_kelimeler:
            st.write("Tekrar etmen gerekenler:", st.session_state.hatali_kelimeler)
        else:
            st.success("Mükemmel! Hiç hata yapmadın.")
        if st.button("Yeniden Başla"):
            st.session_state.oyun_basladi = False
            st.rerun()
