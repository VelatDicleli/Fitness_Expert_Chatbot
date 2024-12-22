
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore


def chatbot(message):
    
    pc = Pinecone(api_key="")

    index = pc.Index("sport")
    

    vectorstore = PineconeVectorStore(index=index,embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))



    retriever = vectorstore.as_retriever(index=index)

    prompt = PromptTemplate(
        input_variables=["question", "context"],
        template="""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. You are a sport expert and keep the answer concise.

    Question: {input}

    Context: {context}

    Answer:"""
    )


    llm = ChatGroq(model="mixtral-8x7b-32768",api_key="")

    document_chain = create_stuff_documents_chain(llm,prompt)
    retriever_chain = create_retrieval_chain(retriever,document_chain)

    result = retriever_chain.invoke({"input":message})

    return result["answer"]









