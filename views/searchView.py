import streamlit as st
from st_keyup import st_keyup as keyup
import pandas as pd


@st.cache_data
def load_csv_data(path):
    data = pd.read_csv(path)
    data['UIN'] = data['UIN'].astype(str).str.replace(',', '')
    return data


#!!! ADD PULLDOWN FOR CSV FILES
#!!! RENAME /logs/ to /databases/; implement naming scheme
def search() -> None:

    st.title("Search v2-β")
    st.write("")
    with st.container(border=1):
        df = load_csv_data("logs/studentDatabase.csv") #!! ONLY USE HARD PATH IF USING LINK DATA
        LENGTH = len(df)

        # Text input for SID search
        searchStr = keyup("Enter Submission ID to search")
        
        st.write("")    
        if searchStr:
            filtered_df = df[df['SID'].apply(lambda x: any(sid.strip().startswith(searchStr) for sid in str(x).split(',')))]
            LENGTH = len(filtered_df)
            # Remove default formatting for numbers in the dataframe (like commas in thousands)
            st.dataframe(filtered_df.style.format(formatter={('UIN'): lambda x: f'{x}'}),use_container_width=True, hide_index=True)
        else:
            # Remove default formatting for the full dataframe as well
            st.dataframe(df.style.format(formatter={('UIN'): lambda x: f'{x}'}),use_container_width=True, hide_index=True)
            
        st.markdown(f"{LENGTH} Students Found")