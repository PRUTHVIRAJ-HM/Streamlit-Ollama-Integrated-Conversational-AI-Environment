import streamlit as st
import ollama
import time
import re
# Set page configuration
st.set_page_config(
    page_title="DeepSeek-R1 Chatbot",
    page_icon="🤖",
    layout="wide"
)

# App title and description
st.title("🤖 DeepSeek-R1 Chatbot")
st.markdown("Chat with the DeepSeek-R1 model running locally on Ollama")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize model name in session state
if "model_name" not in st.session_state:
    st.session_state.model_name = "deepseek-r1:1.5b"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to check available models using proper parsing
def check_model_availability():
    try:
        model_list = ollama.list()

        if not model_list or not hasattr(model_list, 'models'):
            return False

        model_names = [m.model for m in model_list.models]



        for name in model_names:
            if name.startswith("deepseek-r1"):
                st.session_state.model_name = name
                return True

        return False
    except Exception as e:
        with st.sidebar:
            with st.expander("Debug Information"):
                st.error(f"Error checking model availability: {str(e)}")
        return False

# Function to generate response from Ollama

import re

import re

def generate_response(prompt):
    try:
        if not check_model_availability():
            return "❌ Error: DeepSeek-R1 model is not available."

        st.sidebar.success(f"Model selected: {st.session_state.model_name}")

        # Create a placeholder for assistant message
        with st.chat_message("assistant"):
            think_box = st.empty()
            response_box = st.empty()

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
                    time.sleep(0.01)

            # Extract think content
            think_match = re.search(r"<think>(.*?)</think>", full_response, re.DOTALL)
            think_content = think_match.group(1).strip() if think_match else None
            if not think_content:
                think_content = None  # Normalize empty think

            # Clean final response
            response_text = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL).strip()

            # Render think content if exists
            if think_content:
                with think_box.expander("🧠 What the assistant is thinking..."):
                    st.markdown(think_content)
            else:
                think_box.empty()

            # Render response
            if response_text:
                response_box.markdown(response_text)
            else:
                response_box.info("🤖 No direct response was generated.")

        return full_response

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return f"❌ Error: {str(e)}"


# Chat input
if prompt := st.chat_input("Ask something..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate and display assistant response
    response = generate_response(prompt)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot uses:
    - **DeepSeek-R1 (1.5B)** - A powerful open-source language model
    - **Ollama** - For running the model locally
    - **Streamlit** - For the web interface
    """)

    # Show the actual model being used
    st.subheader("Model Being Used")
    if check_model_availability():
        st.success(f"Using model: **{st.session_state.model_name}**")
        st.markdown(f"""
        You can run this model directly with:
        ```
        ollama run {st.session_state.model_name}
        ```
        """)
    else:
        st.error("No DeepSeek-R1 model found")
        st.markdown("""
        Please pull the model with:
        ```
        ollama pull deepseek-r1:1.5b
        ```
        """)

    
with st.sidebar:
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