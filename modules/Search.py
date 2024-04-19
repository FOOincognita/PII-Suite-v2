from modules.StudentDatabase import StudentDatabase, _STUDENTS
import streamlit as st
import pandas as pd
import threading
import os

#! Users should be able to search regardless of PIILinker's status
#!! Users need to be able to search using 1 SID for students with 2 SIDs

#!!! Add support for archives

class InvalidCSVPath(Exception): pass


class PIISearch:
    
    def __init__(self) -> None:
        #!! Wayyyyy too many variables here...
            self.dataBase: StudentDatabase = StudentDatabase() #? Use if not using PIILinker data
            self.df: pd.DataFrame = pd.DataFrame() #? Use if using PIILinker data
            self.fDF: pd.DataFrame = pd.DataFrame() #? Filtered
            self.size: int = 0
            
    @st.cache_data
    def loadCSV(self, path):
        self.dataBase.loadCSV(path)
        self.size = len(self.dataBase.df)
    
    def filter(self, searchStr: str) -> None:
        pd.DataFrame(stuData, columns=["UIN", "name", "SID", "section", "email"])
        if searchStr:
            self.fDF = df[
                df['SID'].apply(
                    lambda x: any(sid.strip().startswith(searchStr) for sid in str(x).split(','))
                )
            ]
       
        return self.fDF.style.format(formatter={('UIN'): lambda x: f'{x}'})

        
    
    
_SEARCH = PIISearch()