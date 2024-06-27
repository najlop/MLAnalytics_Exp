import streamlit as st
import os
from transformers import BartForConditionalGeneration, BartTokenizer
from io import StringIO
import pandas as pd
import pymupdf
from datetime import datetime

# Intro Text
st.markdown('# PDF summarization using Pegasus')
st.header('''PDF size must be below 200MB. Only 1 PDF per time, time will vary depending on size''')

input_file = st.file_uploader('Upload a PDF file')

# Save uploaded file
if input_file:
  with open(os.path.join(input_file.name),'wb') as f:
        f.write(input_file.getbuffer())
  st.success('Saved File')

st.markdown('# Summary')

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
# Load tokeniser
tokenizer = BartTokenizer.from_pretrained(model_name)

def pdf_to_dataframe(input_file):
  metadata = []
  pdf = pymupdf.open(input_file)
  # Get page content as dict and blocks of data
  for page in pdf:
    pages = page.get_text('dict')
    blocks = pages['blocks']
    # Extract metadata from blocks and filter for text, font size and font name
    for block in blocks:
      if 'lines' in block.keys():
        spans = block['lines']
        for span in spans:
          data = span['spans']
          for x in data:
            metadata.append((x['text'], x['size'], x['font']))
  pdf.close()
  output = pd.DataFrame(metadata,columns = ['text','size','font'])
  return output

if input_file:
  start = datetime.now()
  st.spinner(text='Please wait...')
  page_wise_text = []
  # Kp-Regular holds actual text so filter for that
  df = pdf_to_dataframe(input_file)
  df = df.loc[df['font'] == 'Kp-Regular']
  corpus = ' '.join(df['text'])

  # Tokenise text
  tokens = tokenizer.encode(corpus, truncation=True, padding='longest', return_tensors='pt',max_length=1024)

  # Summarise text
  summary = model.generate(tokens,max_length=1024, min_length=50, length_penalty=0.0, num_beams=4, early_stopping=True)

  # Decode tokens and add to list
  decoded_output = tokenizer.decode(summary[0],skip_special_tokens=True)
  page_wise_text.append(decoded_output)

  # Show Summary
  st.success('Summary ready!')
  st.text_area(label ="",value=page_wise_text, placeholder="Please upload a PDF to get it's summary", height = 100)
  st.markdown('')
  end = datetime.now() - start

  st.header(end)
