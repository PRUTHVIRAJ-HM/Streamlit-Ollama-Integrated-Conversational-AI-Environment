import streamlit as st
import ollama
import time
import re

# Page config
st.set_page_config(page_title="LLaMA3 Chatbot", page_icon="🦙", layout="wide")

# Title
st.title("🦙 LLaMA3 Chatbot")
st.markdown("Chat with the LLaMA3 model running locally on Ollama")

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model_name" not in st.session_state:
    st.session_state.model_name = "llama3:latest"

# === Function: Check for available model ===
def check_model_availability():
    try:
        model_list = ollama.list()
        if not model_list or not hasattr(model_list, 'models'):
            return False

        model_names = [m.model for m in model_list.models]
        for name in model_names:
            if name.startswith("llama3"):
                st.session_state.model_name = name
                return True
        return False
    except Exception as e:
        with st.sidebar:
            with st.expander("Debug Information"):
                st.error(f"Error checking model availability: {str(e)}")
        return False

# === Function: Generate and parse response ===
def generate_response(prompt, think_placeholder=None):
    try:
        if not check_model_availability():
            return "❌ Error: LLaMA3 model is not available.", None

        st.sidebar.success(f"Model selected: {st.session_state.model_name}")

        full_response = ""
        current_think = ""
        response_stream = ollama.chat(
            model=st.session_state.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        for chunk in response_stream:
            content = chunk.get("message", {}).get("content", "")
            if content:
                full_response += content

                # Extract current <think> content
                think_match = re.search(r"<think>(.*?)</think>", full_response, re.DOTALL)
                new_think = think_match.group(1).strip() if think_match and think_match.group(1).strip() else ""
                if new_think != current_think:
                    current_think = new_think
                    if think_placeholder is not None:
                        with think_placeholder.expander("🧠 What the assistant is thinking..."):
                            st.markdown(current_think)
                time.sleep(0.01)

        # Remove <think> from final response
        response_text = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()
        return response_text, current_think

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return f"❌ Error: {str(e)}", None

# === Display chat history ===
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            if message.get("think"):
                with st.expander("🧠 What the chat-bot thought..."):
                    st.markdown(message["think"])
                st.markdown(message["response"])
            else:
                st.markdown(message["response"])
        else:
            st.markdown(message["content"])

# === Chat input box ===
if prompt := st.chat_input("Ask something..."):
    # Reformat last assistant message if needed
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        last_msg = st.session_state.messages[-1]
        if "<think>" in last_msg["response"]:
            think_match = re.search(r"<think>(.*?)</think>", last_msg["response"], re.DOTALL)
            think_content = think_match.group(1).strip() if think_match else ""
            response_text = re.sub(r"<think>.*?</think>", "", last_msg["response"], flags=re.DOTALL).strip()
            st.session_state.messages[-1] = {
                "role": "assistant",
                "response": response_text,
                "think": think_content
            }

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Stream and display the assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response_stream = ollama.chat(
            model=st.session_state.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        for chunk in response_stream:
            content = chunk.get("message", {}).get("content", "")
            if content:
                full_response += content
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)
        message_placeholder.markdown(full_response if full_response else "🤖 No response generated.")

    st.session_state.messages.append({
        "role": "assistant",
        "response": full_response
    })

# === Sidebar Info ===
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot uses:
    - **LLaMA3 (latest)** - A high-performance open-source language model
    - **Ollama** - For running the model locally
    - **Streamlit** - For the web interface
    """)

    st.subheader("Model Being Used")
    if check_model_availability():
        st.success(f"Using model: **{st.session_state.model_name}**")
        st.markdown(f"""
        You can run this model directly with:
        ```bash
        ollama run {st.session_state.model_name}
        ```
        """)
    else:
        st.error("No LLaMA3 model found")
        st.markdown("""
        Please pull the model with:
        ```bash
        ollama pull llama3:latest
        ```
        """)

    st.subheader("Model Information")
    try:
        model_info = ollama.show(st.session_state.model_name)
        model_list = ollama.list()
        model_names = [m.model for m in model_list.models]
        st.markdown(f"**Model:** {model_names[0]}")
        st.markdown(f"**Modified At:** {model_info.get('modified_at', 'N/A')}")

        details = model_info.get('details', {})
        if details:
            st.markdown(f"**Format:** {details.get('format', 'N/A')}")
            st.markdown(f"**Family:** {details.get('family', 'N/A')}")
            parameters = details.get('parameter_size') or model_info.get('parameters') or 'N/A'
            st.markdown(f"**Parameters:** {parameters}")
            quantization = details.get('quantization_level') or 'Not quantized'
            st.markdown(f"**Quantization:** {quantization}")
        else:
            st.warning("No detailed information available for this model.")
    except Exception as e:
        st.warning(f"⚠️ Could not retrieve model info. Error: {str(e)}")
