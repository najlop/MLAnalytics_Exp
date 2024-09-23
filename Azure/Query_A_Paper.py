import streamlit as st
import requests, os
from anthropic import Anthropic
from pypdf import PdfReader

st.set_page_config(
    page_title='ArielGPT Query A Paper'
)

client = Anthropic(
    api_key=''
)
MODEL_NAME = 'claude-3-5-sonnet-20240620'

# Intro Text
st.markdown('# PDF summarization using Generative AI')
st.header('''PDF size must be below 200MB. Only 1 PDF per time, time will vary depending on size''')

input_file = st.file_uploader('Upload a PDF file')

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