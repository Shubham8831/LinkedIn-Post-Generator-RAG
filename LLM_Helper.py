from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
import os

llm = ChatGroq(groq_api_key = os.getenv("GROQ_API_KEY"), model_name = "llama-3.3-70b-versatile")



if __name__ == "__main__":
    result = llm.invoke("how to make a samosa")
    print(result.content)