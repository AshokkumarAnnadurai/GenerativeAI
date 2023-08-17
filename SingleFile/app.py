from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

def main():
    load_dotenv()
    st.set_page_config(page_title="Signa G-AI")
    st.header("Ask you PDF ")

    #upload the file
    pdf = st.file_uploader("Upload your PDF" , type="pdf")

    #extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text=""
        for page in pdf_reader.pages:
            text += page.extract_text()

        #split the file
        text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = text_splitter.split_text(text)

        #create Embedding
        embeddings = OpenAIEmbeddings()
        Knowledge_base = FAISS.from_texts(chunks, embeddings)

        #show user input
        user_question = st.text_input('Ask a Question about your Pdf:')
        if user_question:
            docs = Knowledge_base.similarity_search(user_question)
            
            llm = OpenAI()
            chain = load_qa_chain(llm,chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs , question=user_question)
                print(cb)
            
            st.write(response)

if __name__ == '__main__':
    main()