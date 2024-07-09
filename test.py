import streamlit as st;
import tabula as tb;
from fastembed import TextEmbedding
from typing import List
import numpy as np

embedding_model = TextEmbedding()

st.write("this is test");
# this either returns single file or none, if accept multiple file is true then it returns list or none
uploadFile= st.file_uploader("upload your book here",type="pdf",key="uploaded")

# uploaded file
if uploadFile:
    book=tb.read_pdf(uploadFile);
    print(book);




chat=st.chat_input("what's on your mind");

testWord="car";
if chat:
    embedding_generator=embedding_model.embed(chat);
    vectorData=list(embedding_generator);

    embedding_generator2=embedding_model.embed(testWord);
    testVectorData=list(embedding_generator2)
    # checking the logic to match two words
    result=np.dot(vectorData[0],testVectorData[0]);
    print(result)
    testVectorData=np.array(testVectorData);
    # print(testVectorData[0])

# print(vectorData);
