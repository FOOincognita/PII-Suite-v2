import streamlit as st
from enum import Enum
import subprocess
import sys
import os

# Function to read the CSS file
def loadCSS():
    with open('styles/buttons.css', "r") as file:
        return file.read()

# Load your CSS file
buttonCSS = loadCSS()
resetCSS = """
button {
    max-width: initial !important;
    height: auto !important;
    margin-top: 0px !important; 
}
"""

CSS = lambda _css: st.markdown(f"<style>{_css}</style>", unsafe_allow_html=True)


class FileType(Enum):
    FILE   = 1
    FOLDER = 2


class Explorer:
    
    def __init__(self, _buttonName: str, _buttonMsg: str, _type: FileType):
        tmp = f"{_buttonName}_{('folder' if _type == FileType.FOLDER else 'file')}_"
        self.NAME:  str      = f"{tmp}path"
        self.MSG:   str      = _buttonMsg
        self.type:  FileType = _type
        self.KEY:   str      = f"{tmp}key"
        self.valid: bool     = 0
        
        if self.NAME not in st.session_state:
            st.session_state[self.NAME] = '' 


    def selectFile(self):
        CSS(buttonCSS)
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
            st.code(PATH if (PATH := st.session_state[self.NAME]) else self.MSG) 
            self.valid = bool(PATH)




    def selectFolder(self):
        CSS(buttonCSS)
        folder_col1, folder_col2 = st.columns([0.2, 0.8])
        with folder_col1:
            if st.button("Select Folder", key=self.KEY): 
                result = subprocess.run([
                        sys.executable, 
                        os.path.join('modules', 'scripts', 'folder_selector.py')
                    ], 
                    capture_output=True, 
                    text=True
                )
                st.session_state[self.NAME] = result.stdout.strip()
        with folder_col2:
            st.code(PATH if (PATH := st.session_state[self.NAME]) else self.MSG)
            self.valid = bool(PATH)

