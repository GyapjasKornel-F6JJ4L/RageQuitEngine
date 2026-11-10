# Indításhoz 'python -m streamlit run main.py'
import streamlit as st
from pipeline.engine2_sentiment import sentiment
from pipeline.engine3_llm import moderate_comment



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
# Elemzés indítása
if st.button("Elemzés indítása", type="primary"):
    if not comment_input.strip():
        st.warning("Kérlek, írj be egy kommentet!")
    else:
        with st.spinner("A modellek betöltése és az elemzés folyamatban..."):
            # Engine 2 - Sentiment
            sentiment_result = sentiment(comment_input.strip())
            # Engine 3 - LLM Moderáció
            moderation_result = moderate_comment(comment_input.strip())
        # Eredmények
        st.markdown("---")
        st.subheader("📊 Sentiment elemzés")
        st.write("Hangulat:", sentiment_result["mood"])
        st.write("Pontszám:", sentiment_result["score"])
        st.markdown("---")
        st.subheader("🤖 LLM moderáció")
        # Moderációs döntés
        decision = moderation_result["decision"]
        if decision == "DELETE":
            st.error("🚫 A komment törlésre javasolt!")
        elif decision == "ALLOW":
            st.success("✅ A komment engedélyezhető!")
        else:
            st.warning("⚠️ Ismeretlen moderációs döntés!")
        # Kategóriák
        st.write(
            "Személyes támadás:",
            moderation_result["personal_attack"]
        )
        st.write(
            "Sértés:",
            moderation_result["insult"]
        )
        st.write(
            "Gyűlöletbeszéd:",
            moderation_result["hate_speech"]
        )
        # Indoklás
        st.markdown("### 📝 Indoklás")
        st.write(moderation_result["reason"])