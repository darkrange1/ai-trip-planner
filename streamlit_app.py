import streamlit as st
import requests
import datetime
import json
import ast

import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Ajan Tabanlı Seyahat Planlayıcı",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Main Background and Text */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Title Styling */
    h1 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: #4DB6AC; /* Teal color */
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Header Styling */
    h2, h3 {
        color: #80CBC4;
        font-weight: 600;
    }
    
    /* Input Box Styling */
    .stTextInput > div > div > input {
        background-color: #263238;
        color: #ffffff;
        border: 1px solid #37474F;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #00897B;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #00695C;
        transform: scale(1.02);
    }
    
    /* Card/Container Styling for Results */
    .result-card {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-top: 2rem;
        border: 1px solid #333;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #263238;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=80)
    st.title("Menü")
    st.markdown("---")
    st.markdown("### 🛠️ Nasıl Kullanılır")
    st.info(
        """
        1. Gideceğiniz yeri yazın.
        2. Süreyi belirtin (örn. 5 gün).
        3. İlgi alanlarınızı ekleyin (tarih, yemek vb.).
        4. **Seyahatimi Planla** butonuna basın!
        """
    )

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("<h1>✈️ Ajan Tabanlı Seyahat Planlayıcı</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem; margin-bottom: 2rem;'>Mükemmel seyahat planları oluşturmak için yapay zeka destekli yardımcınız.</p>", 
        unsafe_allow_html=True
    )

    with st.form(key="query_form", clear_on_submit=False):
        user_input = st.text_input(
            "Nereye gitmek istersiniz?", 
            placeholder="Örn. Sanat müzelerine odaklanan 5 günlük Paris gezisi planla...",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button("✨ Seyahatimi Planla")

    if submit_button and user_input.strip():
        try:
            with st.spinner("🤖 Yapay Zeka planınızı hazırlıyor... lütfen bekleyin..."):
                payload = {"question": user_input}
                response = requests.post(f"{BASE_URL}/query", json=payload)

            if response.status_code == 200:
                answer = response.json().get("answer", "Yanıt alınamadı.")
                
                cleaned_answer = answer
                
                if isinstance(answer, list) and len(answer) > 0:
                    for item in answer:
                        if isinstance(item, dict):
                            if 'text' in item:
                                cleaned_answer = item['text']
                                break
                            elif 'content' in item:
                                cleaned_answer = item['content']
                                break
                    if cleaned_answer == answer: 
                         cleaned_answer = str(answer[0])

                elif isinstance(answer, dict):
                    if 'text' in answer:
                        cleaned_answer = answer['text']
                    elif 'content' in answer:
                        cleaned_answer = answer['content']
                
                   
                elif isinstance(answer, str):
                    clean_str = answer.strip()
                    if clean_str.startswith("[") or clean_str.startswith("{"):
                        try:
                            parsed = json.loads(clean_str)
                        except:
                            try:
                                parsed = ast.literal_eval(clean_str)
                            except:
                                parsed = None
                        
                        if parsed:
                             if isinstance(parsed, list) and len(parsed) > 0:
                                for item in parsed:
                                    if isinstance(item, dict):
                                        if 'text' in item:
                                            cleaned_answer = item['text']
                                            break
                                        elif 'content' in item:
                                            cleaned_answer = item['content']
                                            break
                             elif isinstance(parsed, dict):
                                if 'text' in parsed:
                                    cleaned_answer = parsed['text']
                                elif 'content' in parsed:
                                    cleaned_answer = parsed['content']

                if not isinstance(cleaned_answer, str):
                    cleaned_answer = str(cleaned_answer)
                
                answer = cleaned_answer.replace("\\n", "\n")

                st.markdown(f"""
                <div class="result-card">
                    <h2>🗺️ {user_input} Seyahatiniz</h2>
                     <p style='color: #888; font-size: 0.9rem;'>Oluşturulma Tarihi: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
                    <hr style="border-top: 1px solid #444;">
                    <div style="font-family: sans-serif; line-height: 1.6;">
                        {answer}
                    </div>
                    <hr style="border-top: 1px solid #444;">
                    <p style="font-size: 0.8rem; color: #666; text-align: center;">
                        *Bu plan yapay zeka tarafından oluşturulmuştur. Lütfen rezervasyonları ve uygunluk durumlarını kontrol edin.*
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.error(f"❌ Hata: {response.text}")

        except Exception as e:
            st.error(f"❌ Bağlantı Hatası: {str(e)}")