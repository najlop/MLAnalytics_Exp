import streamlit as st,os
import pandas as pd
from PIL import Image
import requests
from anthropic import Anthropic
from pypdf import PdfReader
# from streamlit.type_util import Key
# from streamlit_chromadb_connection.chromadb_connection import ChromadbConnection

logo = '/content/MLA.png'
img = Image.open(logo)

st.set_page_config(
    page_title='ArielGPT Home',
    page_icon=img
)

client = Anthropic(
    api_key=''
)
MODEL_NAME = 'claude-3-5-sonnet-20240620'

hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: center; color: black;'>ArielGPT Q&A</h3>", unsafe_allow_html=True)
st.sidebar.write("""
- Have a question on a research paper? Upload it and ask away!
""")
st.sidebar.write("---")
st.sidebar.markdown("<h3 style='text-align: center; color: black;'>ArielGPT Summarisation</h3>", unsafe_allow_html=True)
st.sidebar.write("""
- Submit a paper to get a technincal or non-technical summary from our model.
""")
st.sidebar.write("---")
st.sidebar.markdown("<h3 style='text-align: center; color: black;'>ArielGPT Knowledge Base</h3>", unsafe_allow_html=True)
st.sidebar.write("""
- Check out our knowledge base of research papers for the ESA Ariel mission.
""")
st.sidebar.write("---")
st.sidebar.markdown("<div style='text-align: center; color: blue;'>Copyrights © MLAnalytics 2024</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: blue;'>Powered By mark.hayden@students.opit.com</div>", unsafe_allow_html=True) 

st.markdown("<h2 style='text-align: center; color: gray;'>ArielGPT</h2>", unsafe_allow_html=True)

Q_A, summary, papers, about_us  = st.tabs(['Q&A','Summarise','Knowledge Base','About Us'])


def read_pdf(pdf_file):
  reader = PdfReader(pdf_file)
  content = ''.join(page.extract_text() for page in reader.pages)
  return content

def get_completion(_client, _prompt):
  return _client.messages.create(
      model=MODEL_NAME,
      max_tokens=2048,
      messages=[{
          "role": 'user', "content":  _prompt
      }]
  ).content[0].text

@st.cache_data(ttl=300) # 5 mins
def recommeded_papers(_client,_prompt):
  return _client.messages.create(
      model=MODEL_NAME,
      max_tokens=2048,
      messages=[{
          "role": 'user', "content":  _prompt
      }]
  ).content[0].text

with Q_A:

  # Intro Text
  st.markdown('# PDF summarization using Generative AI')
  st.header('''PDF size must be below 200MB. Only 1 PDF per time, time will vary depending on size''')

  input_file = st.file_uploader('Upload a PDF file', key='Q_A')

  # Save uploaded file
  if input_file:
    with open(os.path.join(input_file.name),'wb') as f:
          f.write(input_file.getbuffer())
    st.success('Saved File')

  st.markdown('# Summary')

  test = st.text_input("Question", "")

  if input_file and test:

    text = read_pdf(input_file)
    completion = get_completion(client,
      f"""Here is an academic paper: <paper>{text}</paper>

    Please do the following:
    Answer all questions asked about the aademic paper. The question is located here: <question>{test}</question>
    """
    )
    st.success('Summary ready!')
    st.text_area(label = '', value = completion, placeholder = 'The answer to your question will be shown here', height = 400)
    st.markdown('')

  else:
    st.text_area(label = '',value = 'The answer to your question will be shown here', placeholder = 'The answer to your question will be shown here', height = 400)

with summary:
  
  # Intro Text
  st.markdown('# PDF summarization using Generative AI')
  st.header('''PDF size must be below 200MB. Only 1 PDF per time, time will vary depending on size''')

  input_file = st.file_uploader('Upload a PDF file',key='summary')
  counter = 0

  options = st.radio(
      'What type of summary would you like?',
      ['High-Level','Technical'],
      captions=[
        'A summary that leaves out any technical terms for a simpler summary',
        'A detailed summary that includes the technical aspects of the paper',
      ],
      index=None
  )

  # Save uploaded file
  if input_file:
    with open(os.path.join(input_file.name),'wb') as f:
          f.write(input_file.getbuffer())
    st.success('Saved File')

  st.markdown('# Summary')

  if input_file and options == 'High-Level':
    counter = 1

    text = read_pdf(input_file)
    completion = get_completion(client,
      f"""Here is an academic paper: <paper>{text}</paper>

    Please do the following:
    Provide a high-level overview of the research paper in such a way that the reader won't need to read the whole paper.
    """
    )
    st.success('Summary ready!')
    st.text_area(label = '', value = completion, placeholder = 'Please upload a PDF to summarise', height = 400)
    st.markdown('')

  elif input_file and options == 'Technical':
    counter = 2

    text = read_pdf(input_file)
    completion = get_completion(client,
      f"""Here is an academic paper: <paper>{text}</paper>

    Please do the following:
    Provide a detailed technical summary of the research paper in such a way that the reader won't need to read the whole paper.
    """
    )
    st.success('Summary ready!')
    st.text_area(label = '', value = completion, placeholder = 'Please upload a PDF to summarise', height = 400)
    st.markdown('')

  else:
    st.text_area(label = '',value = 'Please upload a PDF to summarise', placeholder = 'Please upload a PDF to summarise', height = 400)

  if counter != 0:
    text = read_pdf(input_file)
    similar_papers = st.number_input(
      'Would you like to see similar papers?', value=None, placeholder='How many papers would you like?'
    )
    if similar_papers:
      similarity = recommeded_papers(client,
      f"""Please do the following:
        Assume you are an academic who wants to find more research papers similar to this academic paper: <paper>{text}</paper>.
        Return a list of research papers that are similar to this paper. Sort the list in descending order from most relevant to least relevant.
        The number of papers in the list must be the same as this number: <number>{similar_papers}</number>.
        """
      )
      st.success('Summary ready!')
      st.text_area(label = '', value = similarity, placeholder = 'Please upload a PDF to summarise', height = 400)
      st.markdown('')

with papers:
  st.markdown('Placeholder until Azure DB is running')
  first_paper = 'Operational_range_bounding_of_spectroscopy_models_with_anomaly_detection_draft.pdf'
  second_paper = 'Human_Activity_Recognition_from_Accelerometer_Data_Using_a_Wearable_Device.pdf'
  papers = [first_paper, second_paper]
  subjects = ['anomaly detection algorithms to set operational range boundaries for spectroscopy models','human activity recognition using accelerometer data from a wearable device']
  df = pd.DataFrame(subjects, columns=['Paper Name'])
  st.dataframe(df, hide_index=True)

with about_us:
  st.markdown('Under Development')


























# counter = 2
# st.title('Under development')

# first_paper = 'Operational_range_bounding_of_spectroscopy_models_with_anomaly_detection_draft.pdf'
# second_paper = 'Human_Activity_Recognition_from_Accelerometer_Data_Using_a_Wearable_Device.pdf'
# papers = [first_paper, second_paper]
# subjects = ['anomaly detection algorithms to set operational range boundaries for spectroscopy models','human activity recognition using accelerometer data from a wearable device']

# configuration = {
#     "client": "PersistentClient",
#     "path": "/content/"
# }

# embedding_function_name = "DefaultEmbeddingFunction"
# embedding_config={}

# if 'a' not in st.session_state:
#   st.session_state.a = 1

# collection_name = "documents_collection"
# conn = st.connection("chromadb",
#                      type=ChromadbConnection,
#                      **configuration)

# input_file = st.file_uploader('Upload a PDF file')
# if input_file:
#   counter = counter + 1
#   conn.upload_documents(collection_name=collection_name,
#                         documents=papers,
#                         metadatas=[{"genre": g} for g in subjects],
#                         embedding_function_name=embedding_function_name,
#                         embedding_config={},
#                         ids=[f"{i}" for i in range(len(papers))])
#   documents_collection_df  = conn.get_collection_data(collection_name=collection_name,
#                           attributes= ["documents", "embeddings"])
#   st.dataframe(documents_collection_df['documents'],hide_index=True,use_container_width=True)                   
# if st.session_state['a'] == 1:
#   st.write('delete and create')
#   st.session_state.a = 2
#   conn.delete_collection(collection_name=collection_name)
#   conn.create_collection(collection_name=collection_name,
#                         embedding_function_name=embedding_function_name,
#                         embedding_config={},
#                         metadata = {"hnsw:space": "cosine"})



#   conn.upload_documents(collection_name=collection_name,
#                         documents=papers,
#                         metadatas=[{"genre": g} for g in subjects],
#                         embedding_function_name=embedding_function_name,
#                         embedding_config={},
#                         ids=[f"{i}" for i in range(len(papers))])
#   documents_collection_df  = conn.get_collection_data(collection_name=collection_name,
#                           attributes= ["documents", "embeddings"])
#   st.dataframe(documents_collection_df['documents'],hide_index=True,use_container_width=True)
# elif st.session_state['a'] != 1:
#   st.write('maintain')
#   documents_collection_df  = conn.get_collection_data(collection_name=collection_name,
#                           attributes= ["documents", "embeddings"])
#   st.dataframe(documents_collection_df['documents'],hide_index=True,use_container_width=True)
#   pass  