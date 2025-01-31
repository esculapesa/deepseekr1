
import os
import tempfile
import time
import streamlit as st
from streamlit_chat import message
from rag import ChatPDF
from profile_manager import ProfileManager

st.set_page_config(page_title="RAG with Local DeepSeek R1")

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "assistant" not in st.session_state:
        st.session_state["assistant"] = ChatPDF()
    if "profile_manager" not in st.session_state:
        st.session_state["profile_manager"] = ProfileManager()

def display_messages():
    """Display the chat history."""
    st.subheader("Chat History")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def process_input():
    """Process the user input and generate an assistant response."""
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner("Thinking..."):
            try:
                agent_text = st.session_state["assistant"].ask(
                    user_text,
                    k=st.session_state["retrieval_k"],
                    score_threshold=st.session_state["retrieval_threshold"],
                )
            except ValueError as e:
                agent_text = str(e)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))

def read_and_save_file():
    """Handle file upload and ingestion."""
    if not st.session_state["current_profile"]:
        st.error("Please select or create a profile first")
        return

    st.session_state["assistant"].clear()
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}..."):
            t0 = time.time()
            st.session_state["assistant"].ingest(file_path)
            # Save to profile
            st.session_state["profile_manager"].add_pdf_to_profile(
                st.session_state["current_profile"],
                file_path,
                file.name
            )
            t1 = time.time()

        st.session_state["messages"].append(
            (f"Ingested {file.name} in {t1 - t0:.2f} seconds", False)
        )
        os.remove(file_path)

def load_profile_pdfs():
    """Load PDFs from the selected profile."""
    if st.session_state["current_profile"]:
        st.session_state["assistant"].clear()
        st.session_state["messages"] = []
        pdf_paths = st.session_state["profile_manager"].load_profile_pdfs(
            st.session_state["current_profile"]
        )
        if pdf_paths:
            for pdf_path in pdf_paths:
                with st.spinner(f"Loading {os.path.basename(pdf_path)}..."):
                    try:
                        st.session_state["assistant"].ingest(pdf_path)
                        st.success(f"Loaded {os.path.basename(pdf_path)}")
                    except Exception as e:
                        st.error(f"Failed to load {os.path.basename(pdf_path)}: {str(e)}")
        else:
            st.info(f"No PDFs found in profile {st.session_state['current_profile']}")

def page():
    """Main app page layout."""
    initialize_session_state()

    st.header("RAG with Local DeepSeek R1")

    # Profile Management
    st.subheader("Profile Management")
    col1, col2 = st.columns(2)
    
    with col1:
        new_profile = st.text_input("Create New Profile")
        if st.button("Create Profile") and new_profile:
            st.session_state["profile_manager"].create_profile(new_profile)
            st.success(f"Created profile: {new_profile}")

    with col2:
        profiles = st.session_state["profile_manager"].get_all_profiles()
        st.session_state["current_profile"] = st.selectbox(
            "Select Profile",
            [""] + profiles,
            on_change=load_profile_pdfs
        )

    st.subheader("Upload a Document")
    st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.session_state["ingestion_spinner"] = st.empty()

    # Retrieval settings
    st.subheader("Settings")
    st.session_state["retrieval_k"] = st.slider(
        "Number of Retrieved Results (k)", min_value=1, max_value=10, value=5
    )
    st.session_state["retrieval_threshold"] = st.slider(
        "Similarity Score Threshold", min_value=0.0, max_value=1.0, value=0.2, step=0.05
    )

    # Display messages and text input
    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)

    # Clear chat
    if st.button("Clear Chat"):
        st.session_state["messages"] = []
        st.session_state["assistant"].clear()

if __name__ == "__main__":
    page()
