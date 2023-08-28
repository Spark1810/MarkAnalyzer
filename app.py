from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from pandasai import PandasAI
import matplotlib

#list of free LLMs that support PandasAI (more coming in future):
from pandasai.llm.starcoder import Starcoder
# from pandasai.llm.open_assistant import OpenAssistant
# from pandasai.llm.falcon import Falcon

matplotlib.use('TkAgg')

load_dotenv()

API_KEY = os.getenv('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')

llm = Starcoder(api_token='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')
# llm = OpenAssistant(api_token=API_KEY)
# llm = Falcon(api_token=API_KEY)
pandas_ai =PandasAI(llm)


st.title('Dr Grader : Unleash the Power of Data to Decode Your Academic Destiny')

uploaded_file=st.file_uploader('Upload your file', type=['xlsx'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="latin-1")
    st.write(df.head(3))

    prompt = st.text_input('Enter your prompt')

    if st.button('Generate'):
        if prompt:
            with st.spinner("Generating response..."):
                st.write(pandas_ai.run(df,prompt=prompt))
        else:
            st.warning("Please enter your prompt.")
