import streamlit as st
from enum import Enum
import subprocess
import sys
import os


class FileType(Enum):
    FILE   = 1
    FOLDER = 2


class FileExplorer:
    
    def __init__(self, _buttonName: str, _buttonMsg: str, _type: FileType):
        tmp       = f"{_buttonName}_{('folder' if _type == FileType.FOLDER else 'file')}_"
        self.NAME = f"{tmp}path"
        self.MSG  = _buttonMsg
        self.type = _type
        self.KEY  = f"{tmp}key"
        
        if self.NAME not in st.session_state:
            st.session_state[self.NAME] = '' 


    def select_file(self):
        file_col1, file_col2 = st.columns([0.2, 0.8])  
        with file_col1:
            if st.button("Select File", key=self.KEY): 
                result = subprocess.run([
                        sys.executable, 
                        os.path.join('modules', 'scripts', 'file_selector.py')
                    ], 
                    capture_output=True, 
                    text=True
                )
                st.session_state[self.NAME] = result.stdout.strip() 
        with file_col2:
            st.write(PATH if (PATH := st.session_state[self.NAME]) else "") 


    def select_folder(self):
        folder_col1, folder_col2 = st.columns([0.2, 0.8])
        with folder_col1:
            if st.button("Select Directory", key=self.KEY): 
                result = subprocess.run([
                        sys.executable, 
                        os.path.join('modules', 'scripts', 'folder_selector.py')
                    ], 
                    capture_output=True, 
                    text=True
                )
                st.session_state[self.NAME] = result.stdout.strip()
        with folder_col2:
            st.write(PATH if (PATH := st.session_state[self.NAME]) else "")

