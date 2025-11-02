import streamlit as st
import requests
from datetime import datetime

st.title("Financial Records RAG System")
API_URL = "http://localhost:8000/query"

def query_api(query):
    response = requests.post(API_URL, json={"prompt": query})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error querying API")
        return None

user_query = st.text_input("Enter your financial query:")
if st.button("Submit", key="ask_query"):
    if user_query:
        result = query_api(user_query)
        if result:
            st.subheader("Response:")
            st.write(result['response'])
            if 'source_documents' in result and result['source_documents']:
                st.subheader("Source Documents:")
                for doc in result['source_documents']:
                    st.write(doc)
    else:
        st.warning("Please enter a query.")
 
        
def add_documents_api(documents):
    ADD_DOCS_API_URL = "http://localhost:8000/add_docs"
    response = requests.post(ADD_DOCS_API_URL, json={"documents": documents})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error adding documents")
        return None 
    
    
st.subheader("Add Financial Documents")
doc_files = st.file_uploader(
    "Upload txt file", accept_multiple_files=True, type=["txt"])


if st.button("Submit", key="add_docs"):
    for doc_file in doc_files:
        if doc_file is not None:
            upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_content = doc_file.read().decode("utf-8")
            document = [{"id": doc_file.name + "_" + upload_time, "content": file_content}]
            add_result = add_documents_api(document)
            if add_result:
                st.success(f"Added {document[0]['id']} documents successfully.")
