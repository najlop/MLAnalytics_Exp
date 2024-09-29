import streamlit as st
from streamlit.type_util import Key
from streamlit_chromadb_connection.chromadb_connection import ChromadbConnection

st.set_page_config(
    page_title='ArielGPT Home'
)

st.title('Under development')

configuration = {
    "client": "PersistentClient",
    "path": "/content/"
}

if 'a' not in st.session_state:
  st.session_state.a = 1

collection_name = "documents_collection"
conn = st.connection("chromadb",
                     type=ChromadbConnection,
                     **configuration)
                     
if st.session_state['a'] == 1:
  st.write('delete and create')
  st.session_state.a = 2
  conn.delete_collection(collection_name=collection_name)
  embedding_function_name = "DefaultEmbeddingFunction"
  conn.create_collection(collection_name=collection_name,
                        embedding_function_name=embedding_function_name,
                        embedding_config={},
                        metadata = {"hnsw:space": "cosine"})

  first_paper = 'Operational_range_bounding_of_spectroscopy_models_with_anomaly_detection_draft.pdf'
  second_paper = 'Human_Activity_Recognition_from_Accelerometer_Data_Using_a_Wearable_Device.pdf'
  papers = [first_paper, second_paper]
  subjects = ['anomaly detection algorithms to set operational range boundaries for spectroscopy models','human activity recognition using accelerometer data from a wearable device']

  conn.upload_documents(collection_name=collection_name,
                        documents=papers,
                        metadatas=[{"genre": g} for g in subjects],
                        embedding_function_name=embedding_function_name,
                        embedding_config={},
                        ids=[f"id{i}" for i in range(len(papers))])
  documents_collection_df  = conn.get_collection_data(collection_name=collection_name,
                          attributes= ["documents", "embeddings"])
  st.dataframe(documents_collection_df['documents'],hide_index=True,use_container_width=True)
elif st.session_state['a'] != 1:
  st.write('maintain')
  documents_collection_df  = conn.get_collection_data(collection_name=collection_name,
                          attributes= ["documents", "embeddings"])
  st.dataframe(documents_collection_df['documents'],hide_index=True,use_container_width=True)
  pass  