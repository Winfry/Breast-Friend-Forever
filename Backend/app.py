# backend/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma

app = FastAPI()
emb = OpenAIEmbeddings()
vectordb = Chroma(persist_directory="../chroma_store", embedding_function=emb)
retriever = vectordb.as_retriever(search_kwargs={"k":3})
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Query):
    result = qa_chain.run(q.question)
    return {"answer": result}
