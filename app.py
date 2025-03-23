from flask import Flask, render_template, jsonify, request
from Medical_Assistant.components.data_preproceesing import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from Medical_Assistant.components.prompt import system_prompt

app = Flask(__name__)

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embeddings = download_embeddings()

index_name = "medbot-index"

doc_search = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
    text_key="text")

retriever = doc_search.as_retriever(search_kwargs={"k": 3}, search_type="similarity")

llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, api_key=GOOGLE_API_KEY, max_tokens=1000)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])  # Changed from "/get"
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        response = rag_chain.invoke({"input": user_message})
        return jsonify({"reply": response["answer"]})  # Changed from "output_text"
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"reply": "Sorry, I'm having trouble answering that right now."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug=True)
