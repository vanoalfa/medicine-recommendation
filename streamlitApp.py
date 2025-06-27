import streamlit as st
from VSMModel import VSMModel

st.title("🔍 Sistem Rekomendasi Obat")
st.write("Masukkan nama obat atau gejala, sistem akan menampilkan obat yang relevan berdasarkan deskripsi dan kemiripan makna.")

query = st.text_input("Masukkan kata kunci pencarian:")

if query:
    with st.spinner("Mencari rekomendasi..."):
        hasil = VSMModel(query)
        st.text_area("Hasil:", hasil, height=400)
