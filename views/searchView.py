import streamlit as st
from st_keyup import st_keyup as keyup
import pandas as pd

from modules.Search import _SEARCH




#!!! ADD PULLDOWN FOR CSV FILES
#!!! ADD ARCHIVE SUPPORT
#!!! RENAME /logs/ to /databases/; implement naming scheme
def search() -> None:
    st.title("Search v2-β")
    st.write("")
    with st.container(border=1):
        _SEARCH.loadCSV("logs/studentDatabase.csv") #!! ONLY USE HARD PATH IF USING LINK DATA

        # Text input for SID search
        searchStr = keyup("Enter Submission ID to search")
        
        st.write(""); 
        
        st.dataframe(
            _SEARCH.filter(searchStr), 
            use_container_width=True,
            hide_index=True
        )
        
        # !!!!!!!!!!!!!! [REMOVE] !!!!!!!!!!!!!! #
        if searchStr:
            filtered_df = df[
                df['SID'].apply(
                    lambda x: any(sid.strip().startswith(searchStr) for sid in str(x).split(','))
                )
            ]
            # Remove default formatting for numbers in the dataframe (like commas in thousands)
            st.dataframe(
                filtered_df.style.format(formatter={('UIN'): lambda x: f'{x}'}),
                use_container_width=True,
                hide_index=True
            )
        else:
            # Remove default formatting for the full dataframe as well
            st.dataframe(
                df.style.format(formatter={('UIN'): lambda x: f'{x}'}),
                use_container_width=True, 
                hide_index=True
            )
        # !!!!!!!!!!!!!! [REMOVE] !!!!!!!!!!!!!! #
        
        st.markdown(f"{_SEARCH.size} Students Found")