import streamlit as st;
import tabula as tb;
from fastembed import TextEmbedding
from typing import List
import numpy as np
from langchain_community.document_loaders import PyPDFLoader
import os

embedding_model = TextEmbedding()
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
        print(pages)

chat=st.chat_input("what's on your mind");

testWord="hey";
if chat:
    embedding_generator=embedding_model.embed(chat);
    vectorData=list(embedding_generator);

    embedding_generator2=embedding_model.embed(testWord);
    testVectorData=list(embedding_generator2)
    # checking the logic to match two words
    result=np.dot(vectorData[0],testVectorData[0]);
    print(result)
    testVectorData=np.array(testVectorData);
    # print(testVectorData[0].shape)

# print(vectorData);
