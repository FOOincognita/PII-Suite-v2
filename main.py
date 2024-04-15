import os
import pandas as pd

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer as dfExplorer

from modules.FileExplorer import FileExplorer, FileType #? Select files/folder for path
from modules.Linker import _LINKER #? Handles Linking; call PIILinker::__run()



    #* ---------- WORK IN PROGRESS ---------- *
        # Add prog bars, toast, etc.
        #? Add persistent memory maybe?? idk
        # Add streamlit-on-Hover-tabs
        #> Add st.file_uploader for C50 runs


#* --------------- GLOBAL CONFIG --------------- *#
st.set_page_config(
    page_title = "PII-Suite", 
    page_icon  = "assets/favicon.png",
    layout     = "centered", #> wide
    menu_items = {             
        'Get Help'     : 'https://github.com/FOOincognita/UI/', #! ADD LINK
        'Report a bug' : "https://github.com/FOOincognita/UI/", #! ADD LINK
        'About'        : "Texas A&M University Department of Computer Science & Engineerimg"                  #! ADD INFO
    }
)


def main() -> None:
    with st.sidebar:
        tab = option_menu(
            default_index = 0,
            menu_title    = "PII-Suite",
            menu_icon     = "capsule", #! FIXME:
            options       = ["Link", "Search", "Compare50", "Settings"] , #! FIXME
            icons         = ["robot", "database", "kanban", "gear"], #! FIXME
        )
    
    match tab:
        case 'Link':     link() #? Should Link & Search be on same view, sub-menu, or seperate views?
        case 'Search':   search()
        case 'Compare50': compare()
        case 'Settings': settings()
        case _:
            st.exception(RuntimeError("[ERROR]: Default Case Reached in main()"))
    

#* --------------- DATA FRAME --------------- *#
def link() -> None: ## TODO: ADD STUDENT & PIILinker CLASSES
    ## TODO redemption; archive support
    ## Maybe add stepper-bar?
    st.title('Linker')
    
    #* Global Starter 
    STARTER = FileExplorer("starterCode", "Select Directory", FileType.FOLDER).select_folder()
    
    #* Global Output
    OUTPUT = FileExplorer("output", "Select Output Dir", FileType.FOLDER).select_folder()
    
    
    ## Main submissions
    #* CSV Selection
    st.markdown("Select CSV")
    CSV = FileExplorer("CSV", "Select CSV", FileType.FILE).select_file()
        
    #* Submissions 
    SUBMISSIONS = FileExplorer("submissions", "Select Submissions Dir", FileType.FOLDER).select_folder()

        
    ## Redemption 
    
    if 'toggle_state' not in st.session_state:
        st.session_state['toggle_state'] = False  # Default state is OFF
    
    st.subheader('Redemption', divider='gray')
    #* CHECK-BOX: Redemption Mode
    # Update the toggle state in session state
    st.session_state['TOGGLE_R'] = st.toggle('Redemption Mode')

    if st.session_state['TOGGLE_R']:
        # When toggled on, execute these lines
        CSV_R = FileExplorer("CSV_R", "Select CSV", FileType.FILE).select_file()
        SUBMISSIONS_R = FileExplorer("submissions_R", "Select Submissions", FileType.FOLDER).select_folder()
        st.session_state['CSV_R'] = CSV_R  # Optionally, store the results in session state for further use
        st.session_state['SUBMISSIONS_R'] = SUBMISSIONS_R
    else:
        # Optional: Provide feedback or alternative content when toggled off
        st.write("Redemption is Disabled")
    
    
    #! Send paths to PIILinker 
    #! Check for exceptions & grey outs for errors
    # __run()
    
    #> Use toast to show complete
    


#* --------------- Sub-menu example (horizontal) --------------- *#
def search() -> None:
    # TODO: Add Search GUI
    st.title("Search")
    
    ## Either use streamlit-searchbox or streamlit-keyup
    #! Don't forgor to add to requirements.txt
    

#* --------------- SETTINGS --------------- *#
def compare() -> None:
    # TODO: Add Compare50 GUI
    st.title('Compare50')
    sub_tab = option_menu(
        None,
        options       = ["A", "B"],
        icons         = ['prescription2', 'cash-stack'],
        default_index = 0,
        orientation   = "horizontal", 
    )

    match sub_tab:
        case 'A': subTab1()
        case 'B': subTab2()
        case _:
            st.exception(RuntimeError("[ERROR]: Default Case Reached in compare()"))

def subTab1():
    st.subheader("1")
    
def subTab2():
    st.subheader("2")


#* --------------- SETTINGS --------------- *#
def settings() -> None:
    st.title('Settings')

    

    

if __name__ == "__main__":
    main()
