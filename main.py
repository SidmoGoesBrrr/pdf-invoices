import openai
from pdfminer.high_level import extract_text
import streamlit as st
#make dark theme default

openai.api_key = st.secrets['OpenAI']

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def get_invoices(resume_path):
    pdf_text = extract_text_from_pdf(resume_path)

    messages = [
        {"role": "system", "content": "You are a helpful assistant who reads pdf files and gives information. You are typically given data and asked to give supplier name, date, invoice amount, vat amount  total amount from the data. For example, "+"""Emt is supplier
statement/invoice- this is statement
invoice amount is 489.32/1.2
vat amount is: 489.32/1.2 - 489.32
total amoint is those two added together which is 489.32
most suppliers have the above already broken down for you"""},
        {"role": "user", "content": "Give the supplier name, date, invoice amount, vat amount,total amount as a python readable list from the data."},
        {"role": "assistant", "content": "['Star Pharamacy', '2021-03-01', '1000', '100', '1100']"},
        {"role": "user", "content": f"Give the supplier name, date, invoice amount, vat amount, total amount as a python readable list from the data.\n{pdf_text}"},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response, messages

st.title("PDF Invoice Reader")
#allow this to input multiple files

files = st.file_uploader("Upload your files here", type=["pdf"], accept_multiple_files=True)
#if multiple files are there do this for every file

for file_path in files:
    response = get_invoices(file_path)
    st.success(f"File uploaded successfully!")
    st.text("Request sent: ")
    st.write(response[1])
    st.text("Response: ")
    st.write(response[0].choices[0])

