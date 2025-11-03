import streamlit as st
import requests
from datetime import datetime
from PIL import Image
import numpy as np

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
                
                
def ocr_kvp_api(image_path):
    OCR_KVP_API_URL = "http://localhost:8000/ocr_kvp_add_docs"
    response = requests.post(OCR_KVP_API_URL, json={"image_path": image_path})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error extracting KVP from OCR")
        return None

uploaded_files = st.file_uploader("Choose an image...", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
if uploaded_files is not None:
    kvp_results = []
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        image_path = f"./temp/temp_{uploaded_file.name}"
        image.save(image_path)
        st.image(img_array, caption='Uploaded Image.', use_column_width=True)
        kvp_results.append(ocr_kvp_api(image_path))
    if kvp_results:
        st.subheader("Extracted Key-Value Pairs:")
        st.json(kvp_results)

        # if st.button("Extract KVP and Add Docs",key="add_kvp_docs_"+uploaded_file.name):
            # kvp_results.append(ocr_kvp_api(image_path))
            # if kvp_results:
            #     st.subheader("Extracted Key-Value Pairs:")
            #     st.json(kvp_results)

# def ocr_kvp_api(image_path):
#     OCR_KVP_API_URL = "http://localhost:8000/ocr_kvp"
#     response = requests.post(OCR_KVP_API_URL, json={"image_path": image_path})
#     if response.status_code == 200:
#         return response.json()
#     else:
#         st.error("Error extracting KVP from OCR")
#         return None

# uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     img_array = np.array(image)
#     image_path = f"./temp/temp_{uploaded_file.name}"
#     image.save(image_path)
#     st.image(img_array, caption='Uploaded Image.', use_column_width=True)

#     if st.button("Extract KVP"):
#         kvp_result = ocr_kvp_api(image_path)
#         if kvp_result:
#             st.subheader("Extracted Key-Value Pairs:")
#             st.json(kvp_result)