import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI PDF Chatbot", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.main {
    background-color: #0e1117;
}

h1, h2, h3 {
    color: white;
}

.stTextInput input {
    background-color: #1c1f26;
    color: white;
}

.stButton button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}

.chat-box {
    background-color: #1c1f26;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.user {
    color: #00bcd4;
    font-weight: bold;
}

.bot {
    color: #4caf50;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

# ---------------- HEADER ----------------
st.title("📄 AI PDF Chatbot")

# ---------------- UPLOAD ----------------
st.subheader("📤 Upload PDF")

uploaded_file = st.file_uploader("", type=["pdf"])

if uploaded_file:
    st.write(f"📁 {uploaded_file.name}")

    if st.button("Upload & Process"):
        with st.spinner("Processing..."):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),  # 🔥 FIXED
                        "application/pdf"
                    )
                }

                res = requests.post(f"{API_URL}/upload", files=files)

                if res.status_code == 200:
                    st.success("✅ PDF processed successfully!")
                    st.session_state.pdf_uploaded = True
                    st.session_state.chat_history = []
                else:
                    st.error("❌ Upload failed")

            except Exception as e:
                st.error(str(e))

# ---------------- CHAT ----------------
st.subheader("💬 Ask Questions")

if not st.session_state.pdf_uploaded:
    st.warning("Please upload a PDF first")
else:
    question = st.text_input("Type your question...")

    if st.button("Ask"):
        if question.strip() != "":
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(
                        f"{API_URL}/chat",
                        params={"question": question}
                    )

                    data = res.json()

                    if "answer" in data:
                        st.session_state.chat_history.append({
                            "q": question,
                            "a": data["answer"]
                        })
                    else:
                        st.error(data.get("error", "Error"))

                except Exception as e:
                    st.error(str(e))

# ---------------- CHAT HISTORY ----------------

for chat in reversed(st.session_state.chat_history):
    st.markdown(f"""
    <div class="chat-box">
        <div class="user">🧑 You:</div>
        <div>{chat['q']}</div>
        <br>
        <div class="bot">🤖 Bot:</div>
        <div>{chat['a']}</div>
    </div>
    """, unsafe_allow_html=True)