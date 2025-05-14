import streamlit as st
import tempfile
import xml.etree.ElementTree as ET

# Import the processing function from feed_processor
from feed_processor import process_feed

st.set_page_config(page_title="GMC Feed Refurbished", layout="wide")
st.title("Shoper XML → Google Merchant Center (refurbished)")

st.write("Prześlij plik XML z Shoper, aby wszystkie produkty oznaczyć jako refurbished i dodać <g:identifier_exists>no</g:identifier_exists>.")

uploaded_file = st.file_uploader("Wybierz plik XML", type=["xml"] )

if uploaded_file is not None:
    # Zapisujemy do pliku tymczasowego
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as in_tmp:
        in_tmp.write(uploaded_file.read())
        in_path = in_tmp.name

    # Przygotowujemy ścieżkę wyjściową
    out_path = in_path.replace(".xml", "_refurbished.xml")

    # Przetwarzamy
    process_feed(in_path, out_path)

    # Udostępniamy do pobrania
    with open(out_path, "rb") as f:
        st.download_button(
            label="Pobierz zmodyfikowany feed",
            data=f,
            file_name="feed_refurbished.xml",
            mime="application/xml"
        )
