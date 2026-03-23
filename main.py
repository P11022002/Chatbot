import requests
import os
from dotenv import load_dotenv

# 1. Load variables from the .env file
load_dotenv()

# 2. Fetch the App ID securely from environment variables
PUTER_APP_ID = os.getenv("PUTER_APP_ID")

def chat_with_puter_grok(user_query, chat_history):
    if not PUTER_APP_ID:
        return "Error: PUTER_APP_ID not found in .env file."

    url = "https://puter.com/app/grok-chatbot"
    headers = {
        "Authorization": f"Bearer {PUTER_APP_ID}",
        "Content-Type": "application/json"
    }
    
    # We include the history so the bot 'remembers' context
    data = {
        "model": "x-ai/grok-4.1-fast", 
        "messages": chat_history + [{"role": "user", "content": user_query}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection Failed: {str(e)}"

def start_chatbot():
    print("🚀 Puter-Grok Chatbot (Secure Mode) Active")
    print("Type 'exit' to stop.")
    
    history = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        answer = chat_with_puter_grok(user_input, history)
        print(f"\nGrok: {answer}")
        
        # Update history for context-aware conversation
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    start_chatbot()