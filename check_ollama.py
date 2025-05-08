import ollama
import sys

def check_ollama_installation():
    """Check if Ollama is running and the DeepSeek-R1 model is available."""
    print("Checking Ollama installation...")

    try:
        # List available models
        models = ollama.list()
        print(f"Ollama is running. Available models:")

        # Check if DeepSeek-R1 is in the list
        deepseek_available = False
        for model in models.get('models', []):
            model_name = model.get('name', '')
            print(f"- {model_name}")
            if 'deepseek-r1' in model_name:
                deepseek_available = True

        if not deepseek_available:
            print("\nDeepSeek-R1 model not found. You need to pull it:")
            print("Run: ollama pull deepseek-r1:1.5b")
            return False

        # Test a simple query to make sure the model works
        print("\nTesting DeepSeek-R1 model with a simple query...")
        response = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=[{"role": "user", "content": "Say hello in one short sentence."}]
        )

        print(f"\nModel response: {response['message']['content']}")
        print("\nOllama and DeepSeek-R1 are working correctly!")
        return True

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Ollama is installed and running")
        print("2. Check if you've pulled the DeepSeek-R1 model with: ollama pull deepseek-r1:1.5b")
        print("3. Verify that the Ollama service is accessible at http://localhost:11434")
        return False

if __name__ == "__main__":
    success = check_ollama_installation()
    if not success:
        sys.exit(1)
