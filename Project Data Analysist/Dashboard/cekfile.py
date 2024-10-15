import os
import pandas as pd
import streamlit as st
# Check if the file exists before reading it
file_path = "Dashboard/all_data.csv"
if os.path.exists(file_path):
    all_df = pd.read_csv(file_path)
    print("its exist")
else:
    st.error(f"File not found: {file_path}")