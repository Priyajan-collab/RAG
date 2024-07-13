import streamlit as st;
import tabula as tb;
from fastembed import TextEmbedding

import numpy as np
from langchain_community.document_loaders import PyPDFLoader
import os
from qdrant_client import QdrantClient;
from qdrant_client.http.models import VectorParams, PointStruct
from openai import OpenAI

key="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"
# define model
 # ollama pull phi3:3.8b-instruct
# SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful assistant."}
client = OpenAI(
    base_url="https://api.groq.com/openai/v1/",  # ollama endpoint
    api_key=key,
)



# init client

qClient=QdrantClient(":memory:");
# collection_name
collection_name = "Operator_Overloading"
# review this code below
qClient.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance="Cosine")
)

embedding_model = TextEmbedding()
# this is a function to save file locally
def save_uploadedfile(uploadedfile):
    try:
            with open(os.path.join("./",uploadedfile.name),"wb") as f:
                f.write(uploadedfile.getbuffer())
                st.success("Saved File:{} to tempDir".format(uploadedfile.name))
            return uploadedfile.name
    except:
        return 0;

st.write("this is test");
# this either returns single file or none, if accept multiple file is true then it returns list or none
uploadFile= st.file_uploader("upload your book here",type="pdf",key="uploaded")

# uploaded file
if uploadFile:
    fileName=save_uploadedfile(uploadFile)
    if fileName:
        book=PyPDFLoader("./"+fileName)
        # print(book)
        pages=book.load_and_split();
        i=0;
        for page in pages:
            # Generate embedding for the page content
            embedding = embedding_model.embed(page.page_content)
            vector_data = list(embedding)
            # review this code below
            # Create a point structure with the document and metadata
            
            point = PointStruct(id=i, vector=vector_data[0], payload={"content": page.page_content, "metadata": page.metadata})
            
            # Add point to the collection
            qClient.upsert(collection_name=collection_name, points=[point])
            
            print("iteration:", i)
            i += 1
        # print(pages[1].page_content)

chat=st.chat_input("what's on your mind");

# testWord="what is a function overloading?";
if chat:
    embedding_generator=embedding_model.embed(chat);
    vectorData=list(embedding_generator);
    # print(vectorData[0])

    # embedding_generator2=embedding_model.embed(testWord);
    # testVectorData=list(embedding_generator2)

    search_result=qClient.search(
         collection_name="Operator_Overloading",
        #  query_text=chat,
         query_vector=vectorData[0],
         limit=5
    )
    
    output=[result.payload['content'] for result in search_result]
    st.write(output)
    
    
    # print(test[0])
    # checking the logic to match two words
    # result=np.dot(vectorData[0],testVectorData[0]);
    # print(result)
    # testVectorData=np.array(testVectorData);
    # print(testVectorData[0].shape)

# print(vectorData);
