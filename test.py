import streamlit as st;
from langchain_community.document_loaders import PyPDFLoader
from fastembed import TextEmbedding
import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams,PointStruct
from openai import OpenAI
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()
print("om")
# file_in_session=False


db = QdrantClient(
    url="https://149e4918-9505-4d8d-bf3c-fb96c39318aa.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key=os.getenv("qdrant_key"),
)

# define model
 # ollama pull phi3:3.8b-instruct
# SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful assistant."}
MODEL = "llama3-8b-8192" 
client = OpenAI(
    base_url="https://api.groq.com/openai/v1/",  # ollama endpoint
    api_key=os.getenv("key"),
)

# if 'file_processed' not in st.session_state:
#     st.session_state.file_processed = False


db.recreate_collection(
    collection_name="books",
    vectors_config=VectorParams(size=384,distance="Cosine")
)
def save_uploads(upload):
    try:
        with open(os.path.join("./"+upload.name), "wb") as f:
            f.write(upload.getbuffer());
            st.success("saved sucessfully :"+(upload.name));
            book=PyPDFLoader(os.path.join("./"+upload.name))
            return book
    except:
        st.error("file could not be saved properly")
        return 0;

def push_vector_db(book):
    pages=book.load_and_split();
    id=0
    try:
        for page in pages:
            page2vector=embeding_model.embed(page.page_content);
            page2vector=list(page2vector)
            point=PointStruct(id=id, vector=page2vector[0],payload={"content":page.page_content, "metadata":page.metadata})
            db.upsert(collection_name="books",points=[point])
            print("iteration:",id)
            id+=1
        # st.session_state.file_processed = True        
        
    except:
        st.error("lol error in saving book")

embeding_model=TextEmbedding();
st.write("This is an attempt to recreate the project from scratch")


upload=st.file_uploader("Upload your file",type="pdf",key="uploaded_file")




chat=st.chat_input("write your message here")


if upload:
    book = save_uploads(upload)
    if book:
        push_vector_db(book)

if chat:
    chat2vector=list(embeding_model.embed(chat))
    search_results=db.search(
        collection_name="books",
        query_vector=chat2vector[0],
        limit=5
    )
    output=[result.payload["content"] for result in search_results ]
    # st.write(output)
    # apparently every single content needs a role
    prompt = [
            {
                "role": "system",
                "content": chat +" and also answer the following question using the context below"
            },
            
        ]
    for message in output:
        prompt.append({
            "role":"user",
            "content":message
        })
    print(prompt)
    reply_stream=client.chat.completions.create(
        model=MODEL,
        # this message does not take dict but list of dictionary 
        messages= prompt,
        stream=True
    )
    st.write(reply_stream)




    




