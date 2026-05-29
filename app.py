import streamlit as st
import json
import os
import pandas as pd

# 2. Arayüz Ayarları (En başa aldık)
st.set_page_config(page_title="Rusça Zindan Oyunu", layout="centered")

# --- BAŞLATMA KISMI (Eksik olan buydu) ---
if "oyun_aktif" not in st.session_state:
    st.session_state["oyun_aktif"] = False
if "kelimeler" not in st.session_state:
    st.session_state["kelimeler"] = []
if "hatali_kelimeler" not in st.session_state:
    st.session_state["hatali_kelimeler"] = []
# ----------------------------------------

# 1. Seri Sistemini Yükle
def get_durum():
    if not os.path.exists("durum.json"):
        return {"seri_gun": 0}
    with open("durum.json", "r") as f:
        return json.load(f)

durum = get_durum()

st.title("🇷🇺 Rusça Zindan Oyunu")

st.sidebar.header("İstatistikler")
st.sidebar.metric("Seri Günü", f"{durum['seri_gun']} Gün")

# 3. Veritabanını Yükle
with open("kelimeler.json", "r", encoding="utf-8") as f:
    kategoriler = json.load(f)

# 4. Kategori Seçimi
kat = st.selectbox("Hangi zindana girmek istersin?", list(kategoriler.keys()))

if st.button("Zindana Gir"):
    st.session_state["oyun_aktif"] = True
    st.session_state["kelimeler"] = list(kategoriler[kat].items())
    st.session_state["hatali_kelimeler"] = []
    st.rerun()

# 5. Oyun Döngüsü
if st.session_state.get("oyun_aktif"):
    if st.session_state["kelimeler"]:
        rusca, turkce = st.session_state["kelimeler"][0]
        
        st.write("---")
        cevap = st.text_input(f"'{rusca}' kelimesinin Türkçe karşılığı nedir?", key="cevap_input")
        
        if st.button("Kontrol Et"):
            if cevap.lower() == turkce:
                st.success("Doğru!")
                st.session_state["kelimeler"].pop(0)
                st.rerun()
            else:
                st.error("Yanlış! Tekrar dene.")
                if (rusca, turkce) not in st.session_state["hatali_kelimeler"]:
                    st.session_state["hatali_kelimeler"].append((rusca, turkce))
    else:
        st.balloons()
        st.success("Tebrikler, tüm zindanı temizledin!")
        
        # Hatalı kelimeleri tablo olarak göster
        if st.session_state["hatali_kelimeler"]:
            st.warning("Tekrar etmen gereken kelimeler:")
            df = pd.DataFrame(st.session_state["hatali_kelimeler"], columns=["Rusça", "Türkçe"])
            st.table(df)
            
        if st.button("Yeni Oyun Başlat"):
            st.session_state["oyun_aktif"] = False
            st.rerun()
