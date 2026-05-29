import streamlit as st
import json
import os
import random

# Veri yükleme
def get_kelimeler():
    with open("kelimeler.json", "r", encoding="utf-8") as f:
        return json.load(f)

st.title("🇷🇺 Rusça Zindan Oyunu")

# Oturum başlatma
if "oyun_basladi" not in st.session_state:
    st.session_state.oyun_basladi = False

kategoriler = get_kelimeler()

# Kategori seçimi
kat = st.selectbox("Hangi zindana girmek istersin?", list(kategoriler.keys()))

if st.button("Zindana Gir"):
    st.session_state.oyun_basladi = True
    st.session_state.kelimeler_listesi = list(kategoriler[kat].items())
    st.session_state.hatali_liste = []
    st.session_state.dogru_sayisi = 0
    st.rerun()

# Oyun akışı
if st.session_state.oyun_basladi:
    if st.session_state.kelimeler_listesi:
        # Rastgele kelime seç (Listeden ilkini alıp sürekli güncelleme mantığı)
        rusca, turkce = st.session_state.kelimeler_listesi[0]
        
        st.subheader(f"Kelime: {rusca}")
        cevap = st.text_input("Türkçe karşılığı nedir?", key="cevap_input")
        
        if st.button("Kontrol Et"):
            if cevap.strip().lower() == turkce.lower():
                st.success("Doğru!")
                st.session_state.kelimeler_listesi.pop(0) # Doğru bildiyse listeden at
                st.rerun()
            else:
                st.error("Yanlış! Tekrar dene.")
                st.session_state.hatali_liste.append(f"{rusca} = {turkce}")
                # Hatalı olanı sona atalım ki tekrar sorulsun
                kelime = st.session_state.kelimeler_listesi.pop(0)
                st.session_state.kelimeler_listesi.append(kelime)
                st.rerun()
    else:
        st.balloons()
        st.success("Tebrikler, tüm zindanı temizledin!")
        st.write("Hata listesi:", st.session_state.hatali_liste)
        if st.button("Yeni Oyun"):
            st.session_state.oyun_basladi = False
            st.rerun()
