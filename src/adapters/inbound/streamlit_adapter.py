import streamlit as st
from urllib.parse import urlparse
from infrastructure.dependencies import build_ingest_service, build_chat_service
from src.domain.entities.website import WebsiteInput

@st.cache_resource
def get_ingest_service():
    return build_ingest_service()

@st.cache_resource
def get_chat_service():
    return build_chat_service()

def run():
    st.set_page_config(page_title="Chatbot Generator", page_icon="🤖", layout="centered")

    if "website_id" not in st.session_state:
        st.session_state.website_id = None
    if "company_name" not in st.session_state:
        st.session_state.company_name = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot_ready" not in st.session_state:
        st.session_state.chatbot_ready = False

    if not st.session_state.chatbot_ready:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🤖 Instant Website Chatbot Generator")
        st.markdown("Enter any company website URL and get a working chatbot — instantly.")
        st.markdown("---")

        url = st.text_input("Website URL", placeholder="https://example.com", label_visibility="collapsed")

        if st.button("⚡ Generate Chatbot", use_container_width=True, type="primary"):
            if not url.strip():
                st.error("Please enter a URL first.")
            else:
                try:
                    with st.status("Building your chatbot...", expanded=True) as status:
                        st.write("🌐 Scanning website pages...")
                        session = get_ingest_service().ingest(WebsiteInput(url=url))
                        st.write(f"📄 Indexed {session.chunks_indexed} chunks")
                        st.write("🧠 Building knowledge base...")
                        st.write("✅ Done!")
                        status.update(label="Chatbot ready!", state="complete")

                    st.session_state.website_id = session.website_id
                    st.session_state.company_name = session.company_name
                    st.session_state.chatbot_ready = True
                    st.session_state.messages = []
                    st.rerun()
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    else:
        company = st.session_state.company_name
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"## 💬 {company} Assistant")
            st.caption(f"Answers based on content from {company}")
        with col2:
            if st.button("🔄 New"):
                st.session_state.chatbot_ready = False
                st.session_state.website_id = None
                st.session_state.messages = []
                st.rerun()

        st.markdown("---")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg.get("sources"):
                    with st.expander("📎 Sources"):
                        for s in msg["sources"]:
                            st.caption(s)

        if question := st.chat_input(f"Ask anything about {company}..."):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        result = get_chat_service().chat(st.session_state.website_id, question)
                        st.write(result["answer"])
                        if result["sources"]:
                            with st.expander("📎 Sources"):
                                for s in result["sources"]:
                                    st.caption(s)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result["answer"],
                            "sources": result["sources"]
                        })
                    except Exception as e:
                        st.error(f"Error: {e}")

run()