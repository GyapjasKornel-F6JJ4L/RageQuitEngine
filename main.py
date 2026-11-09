# Indításhoz 'python -m streamlit run main.py'
import streamlit as st
from pipeline.engine2_sentiment import sentiment


st.markdown(
    """
    <style>
    [data-testid="stHeader"] { 
        display: none !important; 
    }
    [data-testid="stStatusWidget"] { 
        visibility: hidden !important; 
    }
    .stMain h1 {
        text-align: center;
        width: 100%;
    }
    .stMain h3 {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="RageQuitEngine",
    page_icon="🤬"
)



st.title("🤬 RageQuitEngine")
st.markdown("### Automatikus Kommentmoderációs Pipeline")
st.html("<br>")
comment_input = st.text_area("Írd be a kommentet amelyet tesztelni szeretnél:",
             placeholder="pl. Ez egy ostoba videó volt! Sajnálom, hogy elvett fél órát az életemből")
if st.button("Elemzés indítása", type="primary"):
    with st.spinner("A modell betöltése és az elemzés folyamatban..."):
        sentiment_result = sentiment(comment_input.strip())
    st.write(sentiment_result)
