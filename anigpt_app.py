import streamlit as st
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from transformers import pipeline

# --- Google Sheets Auth ---
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Replace with your Google Sheet and tab/worksheet names
SHEET_NAME = "Ani_GPT_Testing"
TAB_NAME = "Mood"

try:
    sheet = client.open(SHEET_NAME).worksheet(TAB_NAME)
except Exception as e:
    st.error(f"Google Sheet access error: {e}")

# --- Huggingface AI Chat Model ---
@st.cache_resource  # caches model to avoid load repeat
def load_model():
    return pipeline("text-generation", model="tiiuae/falcon-7b-instruct")

chat_ai = load_model()

st.title("AniGPT V1 🚀 (Mood Tracker + AI Chat)")
st.markdown("**Google Sheet:** Ani_GPT_Testing &nbsp; &nbsp; **Tab:** Mood")

# --- Mood Tracker UI ---
st.header("Mood Tracker")
col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("Aaj ka Mood?", ["😊 Happy", "😢 Sad", "😐 Neutral", "😤 Angry"])
with col2:
    reason = st.text_input("Mood ka Reason")

user = st.text_input("User Name (ya nickname)", "testuser")

if st.button("Save Mood"):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    try:
        sheet.append_row([user, now, mood, reason])
        st.success("Mood saved! ✅")
    except Exception as e:
        st.error(f"Error saving mood: {e}")

st.markdown("---")

# --- AI Chatbot UI ---
st.header("AI Chatbot")
user_question = st.text_input("Tumhara Sawaal...")
if st.button("AI se Poocho"):
    with st.spinner("AI soch rahi hai..."):
        try:
            input_text = f"User: {user_question}\nAI:"
            output = chat_ai(input_text, max_length=100, temperature=0.7)
            reply = output[0]['generated_text'].split("AI:")[-1].strip()
            st.write("**AI:**", reply)
        except Exception as e:
            st.error(f"AI Model error: {e}")

st.markdown("---")
st.info("V1 Demo — Mood logs Google Sheet par jayegi, AI Chat Live hai!")

