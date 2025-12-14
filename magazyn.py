import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="Magazyn z Kategoriami", page_icon="📦")

st.title("📦 System Zarządzania Magazynem")

# Definicja dostępnych kategorii
KATEGORIE = ["Spożywcze", "Elektronika", "Chemia", "Inne"]

# Inicjalizacja listy towarów (jeśli sesja jest nowa)
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = [
        {"nazwa": "Chleb", "kategoria": "Spożywcze", "ilosc": 10},
        {"nazwa": "Myszka", "kategoria": "Elektronika", "ilosc": 2}
    ]

# --- PANEL BOCZNY (FILTROWANIE) ---
st.sidebar.header("🔍 Filtrowanie")
filtr_kat = st.sidebar.multiselect(
    "Pokaż kategorie:",
    options=KATEGORIE,
    default=KATEGORIE
)

# --- SEKCJA 1: DODAWANIE TOWARU ---
with st.expander("➕ Dodaj nowy towar do listy"):
    with st.form("form_dodawania", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        n_nazwa = col1.text_input("Nazwa towaru")
        n_kat = col2.selectbox("Kategoria", KATEGORIE)
        n_ilosc = col3.number_input("Ilość", min_value=1, step=1)
        
        submit = st.form_submit_button("Dodaj produkt")
        
        if submit:
            if n_nazwa:
                nowy_produkt = {"nazwa": n_nazwa, "kategoria": n_kat, "ilosc": n_ilosc}
                st.session_state.magazyn.append(nowy_produkt)
                st.success(f"Dodano {n_nazwa} do kategorii {n_kat}")
                st.rerun()
            else:
                st.error("Nazwa nie może być pusta!")

st.divider()

# --- SEKCJA 2: LISTA TOWARÓW ---
st.subheader("📋 Aktualny stan magazynu")

if not st.session_state.magazyn:
    st.info("Magazyn jest obecnie pusty.")
else:
    # Filtrowanie danych do wyświetlenia
    widok_magazynu = [item for item in st.session_state.magazyn if item['kategoria'] in filtr_kat]
    
    if not widok_magazynu:
        st.warning("Brak produktów w wybranych kategoriach.")
    else:
        # Nagłówki tabeli
        h_col1, h_col2, h_col3, h_col4 = st.columns([3, 2, 1, 1])
        h_col1.markdown("**Nazwa**")
        h_col2.markdown("**Kategoria**")
        h_col3.markdown("**Ilość**")
        h_col4.markdown("**Akcja**")
        st.write("---")

        # Wyświetlanie wierszy (używamy oryginalnego indeksu do usuwania)
        for i, produkt in enumerate(st.session_state.magazyn):
            # Sprawdzamy czy produkt pasuje do filtra (aby go pokazać)
            if produkt['kategoria'] in filtr_kat:
                c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
                
                # Dynamiczna ikona w zależności od kategorii
                ikona = "🍎" if produkt['kategoria'] == "Spożywcze" else "💻" if produkt['kategoria'] == "Elektronika" else "🧼" if produkt['kategoria'] == "Chemia" else "📦"
                
                c1.write(f"{ikona} {produkt['nazwa']}")
                c2.info(produkt['kategoria'])
                c3.write(f"{produkt['ilosc']} szt.")
                
                if c4.button("Usuń", key=f"del_{i}"):
                    st.session_state.magazyn.pop(i)
                    st.rerun()

# --- SEKCJA 3: STATYSTYKI ---
if st.session_state.magazyn:
    st.divider()
    df = pd.DataFrame(st.session_state.magazyn)
    st.subheader("📊 Udział kategorii w magazynie")
    
    # Wykres kołowy pokazujący rozkład kategorii
    pie_data = df['kategoria'].value_counts()
    st.bar_chart(pie_data)
