import streamlit as st
import requests
st.set_page_config(
    page_title="EaseMyLearn",
    page_icon="📚",
    layout="centered"
)
st.markdown("""
<style>
    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    h1 {
        text-align: center;
        font-size: 42px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 40px;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
st.title("EaseMyLearn")

st.markdown(
    '<p class="subtitle">Learn anything from your documents with AI</p>',
    unsafe_allow_html=True
)

file = st.file_uploader(
    "Upload your document",
    type=["pdf", "docx"]
)

if file:
    if st.button("Upload"):

        files = {
            "file": (file.name, file.getvalue(), file.type)
        }

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        if response.status_code == 200:
            data = response.json()

            st.success("Document uploaded successfully")

            st.write("Filename:", data["filename"])
            st.write("Characters:", data["characters"])
            st.write("Chunks:", data["number_of_chunks"])

            st.session_state.document_id = data["document_id"]

        else:
            st.error(response.text)
if "document_id" in st.session_state:

    st.divider()

    st.subheader("Ask about your document")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask a question about your document")

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={
                "question": question,
                "document_id": st.session_state.document_id
            }
        )

        if response.status_code == 200:

            data = response.json()
            answer = data["answer"]

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.rerun()

        else:
            st.error(response.text)