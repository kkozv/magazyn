import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Prosty Magazyn", page_icon="📦")

st.title("📦 System Zarządzania Magazynem")
st.info("Uwaga: Dane są przechowywane tylko w pamięci podręcznej sesji bieżącej karty. Odświeżenie strony zresetuje listę.")

# Inicjalizacja listy towarów (tylko jeśli nie istnieje w danej sesji)
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = ["Chleb", "Mleko", "Cukier"]

# Sekcja 1: Dodawanie towaru
st.subheader("➕ Dodaj nowy towar")
nowy_towar = st.text_input("Nazwa towaru", placeholder="Wpisz nazwę...")

if st.button("Dodaj do listy"):
    if nowy_towar:
        if nowy_towar not in st.session_state.magazyn:
            st.session_state.magazyn.append(nowy_towar)
            st.success(f"Dodano: {nowy_towar}")
        else:
            st.warning("Ten towar już jest na liście.")
    else:
        st.error("Pole nazwy nie może być puste.")

st.divider()

# Sekcja 2: Wyświetlanie i Usuwanie
st.subheader("📋 Aktualny stan magazynu")

if not st.session_state.magazyn:
    st.write("Magazyn jest pusty.")
else:
    # Wyświetlenie listy z przyciskami do usuwania
    for index, towar in enumerate(st.session_state.magazyn):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{index + 1}. {towar}")
        with col2:
            if st.button(f"Usuń", key=f"btn_{index}"):
                st.session_state.magazyn.pop(index)
                st.rerun() # Odświeżenie aplikacji po usunięciu

# Stopka
st.sidebar.markdown("### O aplikacji")
st.sidebar.write("Prosty prototyp magazynu wykonany w Streamlit.")
