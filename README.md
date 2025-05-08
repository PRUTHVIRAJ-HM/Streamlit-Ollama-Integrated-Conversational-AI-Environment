# DeepSeek-R1 Streamlit Chatbot

A simple chatbot interface for the DeepSeek-R1 model running locally with Ollama.

## Prerequisites

- Python 3.8+
- Ollama installed and running
- DeepSeek-R1 model pulled in Ollama

## Setup

1. Clone this repository or download the files.

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running and the DeepSeek-R1 model is available:

```bash
# Pull the model if you haven't already
ollama pull deepseek-r1:1.5b

# Or you can run it directly (it will pull if not available)
ollama run deepseek-r1:1.5b
```

## Running the Chatbot

1. Start the Streamlit app:

```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501).

3. Start chatting with the DeepSeek-R1 model!

## Features

- Clean, user-friendly interface
- Real-time streaming responses
- Chat history maintained during the session
- Error handling for Ollama connection issues

## Customization

You can modify the `app.py` file to:

- Change the model (replace "deepseek-r1:1.5b" with another model available in your Ollama installation)
- Adjust the UI layout and styling
- Add additional parameters to the Ollama API calls

## Troubleshooting

- If you encounter connection errors, make sure Ollama is running in another terminal window
- If the model is not found, make sure you've pulled it with `ollama pull deepseek-r1:1.5b`
- For other issues, check the Ollama logs for details
