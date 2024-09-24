import streamlit as st
import requests, os
from anthropic import Anthropic
from pypdf import PdfReader

st.set_page_config(
    page_title='ArielGPT Summary'
)

client = Anthropic(
    api_key=''
)
MODEL_NAME = 'claude-3-5-sonnet-20240620'

# Intro Text
st.markdown('# PDF summarization using Generative AI')
st.header('''PDF size must be below 200MB. Only 1 PDF per time, time will vary depending on size''')

input_file = st.file_uploader('Upload a PDF file')
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

if input_file and options == 'High-Level':
  counter = 1
  st.success('Summary ready!')
  st.text_area(label = '', value = 'Please upload a PDF to summarise', placeholder = 'Please upload a PDF to summarise', height = 400)
  st.markdown('')

elif input_file and options == 'Technical':
  counter = 2
  st.success('Summary ready!')
  st.text_area(label = '', value = "Please upload a PDF to summarise", placeholder = 'Please upload a PDF to summarise', height = 400)
  st.markdown('')

else:
  st.text_area(label = '',value = 'Please upload a PDF to summarise', placeholder = 'Please upload a PDF to summarise', height = 400)

if counter != 0:
  text = read_pdf(input_file)
  similar_papers = st.number_input(
    'Would you like to see similar papers?', value=None, placeholder='How many papers would you like?'
  )
  if similar_papers:
    st.success('Answer Ready!')
    st.text_area(label = '', value = similarity, placeholder = 'Please upload a PDF to summarise', height = 400)
    st.markdown('')
