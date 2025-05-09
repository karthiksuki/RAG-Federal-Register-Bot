import streamlit as st
import pymysql
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def fetch_documents():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='federal_register'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, title, publication_date, agency, url,pdf FROM documents_fedral")
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    return documents

def create_faiss_index(documents):
    embeddings = [model.encode([doc['title'] + " " + doc['agency']])[0] for doc in documents]
    embeddings = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings

documents = fetch_documents()
index, embeddings = create_faiss_index(documents)

st.set_page_config(page_title="Federal Register Chat Agent", layout="centered")
st.title("Federal Register Chat Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask something about federal documents")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Processing the query"):
        query_embedding = model.encode([query]).astype('float32')
        k = 5
        distances, indices = index.search(query_embedding, k)

        if distances[0][0] < 0.5:
            relevant_docs = [documents[idx] for idx in indices[0]]
            docs_str = "\n".join(
                f"- {doc['title']} ({doc['publication_date']}, {doc['agency']}) [{doc['url']}, {doc['pdf']}]"
                for doc in relevant_docs
            )
            response = f"Based on the documents retrieval:\n{docs_str}"
        else:
            response = "No relevant federal documents were found in the database for your query."

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
