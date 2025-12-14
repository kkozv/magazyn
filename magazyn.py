import streamlit as st
import pandas as pd

st.set_page_config(page_title="Magazyn z Kategoriami", page_icon="📦")

st.title("📦 System Zarządzania Magazynem")

KATEGORIE = ["Spożywcze", "Elektronika", "Chemia", "Inne"]

# Zmieniamy nazwę klucza na 'magazyn_v2', aby uniknąć konfliktu ze starymi danymi
if 'magazyn_v2' not in st.session_state:
    st.session_state.magazyn_v2 = [
        {"nazwa": "Chleb", "kategoria": "Spożywcze", "ilosc": 10},
        {"nazwa": "Myszka", "kategoria": "Elektronika", "ilosc": 2}
    ]

# --- PANEL BOCZNY ---
st.sidebar.header("🔍 Filtrowanie")
filtr_kat = st.sidebar.multiselect(
    "Pokaż kategorie:",
    options=KATEGORIE,
    default=KATEGORIE
)

# --- DODAWANIE TOWARU ---
with st.expander("➕ Dodaj nowy towar do listy"):
    with st.form("form_dodawania", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        n_nazwa = col1.text_input("Nazwa towaru")
        n_kat = col2.selectbox("Kategoria", KATEGORIE)
        n_ilosc = col3.number_input("Ilość", min_value=1, step=1)
        
        if st.form_submit_button("Dodaj produkt"):
            if n_nazwa:
                st.session_state.magazyn_v2.append({
                    "nazwa": n_nazwa, 
                    "kategoria": n_kat, 
                    "ilosc": n_ilosc
                })
                st.rerun()

st.divider()

# --- LISTA TOWARÓW ---
st.subheader("📋 Aktualny stan magazynu")

# Filtrowanie bezpieczne (sprawdza czy element jest słownikiem)
widok_magazynu = [
    item for item in st.session_state.magazyn_v2 
    if isinstance(item, dict) and item.get('kategoria') in filtr_kat
]

if not widok_magazynu:
    st.info("Brak produktów do wyświetlenia.")
else:
    for i, produkt in enumerate(st.session_state.magazyn_v2):
        # Wyświetlamy tylko te, które pasują do filtra
        if isinstance(produkt, dict) and produkt.get('kategoria') in filtr_kat:
            c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
            c1.write(f"📦 {produkt['nazwa']}")
            c2.caption(produkt['kategoria'])
            c3.write(f"{produkt['ilosc']} szt.")
            
            if c4.button("Usuń", key=f"del_{i}"):
                st.session_state.magazyn_v2.pop(i)
                st.rerun()

# --- WYKRES ---
if widok_magazynu:
    st.divider()
    df = pd.DataFrame(widok_magazynu)
    st.bar_chart(df.groupby('kategoria')['ilosc'].sum())
