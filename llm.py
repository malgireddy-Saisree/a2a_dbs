# llm/azure_openai.py

import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-12-01-preview"
)

def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # your deployment name (IMPORTANT)
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content


# -------------------------------
# MAIN FUNCTION (TEST LLM)
# -------------------------------
def main():
    print("🔍 Testing Azure OpenAI...\n")

    try:
        question = "What is the capital of India?"
        print("🧠 Question:", question)

        answer = call_llm(question)

        print("\n✅ Response from LLM:")
        print(answer)

    except Exception as e:
        print("\n❌ Error connecting to Azure OpenAI:")
        print(e)


# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()