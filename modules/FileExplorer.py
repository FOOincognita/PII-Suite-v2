import streamlit as st
import subprocess
import sys
import os

#! [FIXME]: ADD ERROR HANDLING
#!! ADD to UI; 1 instance per button
class FileExplorer:
    def __init__(self):
        # Initialize session state for file and folder paths if they don't already exist
        if 'file_path' not in st.session_state:
            st.session_state['file_path'] = '' #! [FIXME]: keys will need to be button label dependent
        if 'folder_path' not in st.session_state:
            st.session_state['folder_path'] = '' #! [FIXME]: keys will need to be button label dependent

    def select_file(self):
        # File selection button and label
        file_col1, file_col2 = st.columns([1, 3])  # Adjust the ratio as needed
        with file_col1:
            if st.button('Open File Selector'): ## TODO: Add variable to store button label
                result = subprocess.run(
                    [sys.executable, os.path.join('modules', 'scripts', 'file_selector.py')], 
                    capture_output=True, 
                    text=True
                )
                st.session_state['file_path'] = result.stdout.strip() #! [FIXME]: keys will need to be button label dependent
        with file_col2:
            if st.session_state['file_path']: #! [FIXME]: keys will need to be button label dependent
                st.write(f'Selected file: {st.session_state["file_path"]}')
            else:
                st.write("")  # Keeps the layout consistent

    def select_folder(self):
        # Folder selection button and label
        folder_col1, folder_col2 = st.columns([1, 3])  # Adjust the ratio as needed
        with folder_col1:
            if st.button('Open Folder Selector'): ## TODO: Add variable to store button label
                result = subprocess.run(
                    [sys.executable, os.path.join('modules', 'scripts', 'folder_selector.py')], 
                    capture_output=True, 
                    text=True
                )
                st.session_state['folder_path'] = result.stdout.strip() #! [FIXME]: keys will need to be button label dependent
        with folder_col2:
            if st.session_state['folder_path']: #! [FIXME]: keys will need to be button label dependent
                st.write(f'Selected folder: {st.session_state["folder_path"]}') #! [FIXME]: keys will need to be button label dependent
            else:
                st.write("")  # Keeps the layout consistent

