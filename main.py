import os
import pandas as pd

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer as dfExplorer

from modules.Explorer import Explorer, FileType #? Select files/folder for path
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
    
    setState = lambda key, val: setattr(st.session_state, key, val)
    getState = lambda key:      st.session_state.get(key)
    
    st.title('PII-Linker v2-Beta', anchor=False)
    
    #? Init redemption mode session state attr
    if "redemptionToggle" not in st.session_state:
        setState("redemptionToggle", False)
    if "FERPAToggle" not in st.session_state:
        setState("FERPAToggle", True)
    
    ## Mode Selection
    st.write(""); st.subheader("Mode Selection", anchor=False)
    with st.container(border=1):  
        setState("FERPAToggle", 
            st.toggle(
                label = 'FERPA Mode', 
                help  = "Toggle for FERPA compliance.\n\t0: Submissions linked using PII\n\t1: Submissions linked using Submission IDs", 
                value = getState("FERPAToggle")
            )
        )
        setState(
            "redemptionToggle",
            st.toggle(
                label = "Redemption Mode",
                help  = "Toggle for redemption mode.\n\t", ## TODO
                value = getState("redemptionToggle")
            )
        )
    
    ## Init Explorers
    def _initExplorer(__name: str, __msg: str, __type: FileType):
        setState(__name, Explorer(__name, __msg, __type))
        
        match __type:
            case FileType.FOLDER: getState(__name).selectFolder()
            case FileType.FILE:   getState(__name).selectFile()
            case _:               st.exception(RuntimeError("[ERROR]: Default Reached in initExplorer()"))
    
    
    ## Original Submissions
    st.write(""); st.subheader("Original Submissions", anchor=False)
    with st.container(border=1):
        _initExplorer("starterCode",    "Select Starter Code Directory", FileType.FOLDER)
        _initExplorer("outputDir",      "Select Output Directory",       FileType.FOLDER)
        _initExplorer("submissionsDir", "Select Submissions Directory",  FileType.FOLDER)
        _initExplorer("originalCSV",    "Select CSV File",               FileType.FILE  )

    ## Redemption Submissions
    if getState("redemptionToggle"):
        st.write(''); st.subheader("Redemption Submissions", anchor=False) 
        with st.container(border=1):  
            _initExplorer("redemptionSubsDir", "Select Redemption Submissions", FileType.FOLDER)
            _initExplorer("redemptionCSV",     "Select Redemption CSV",         FileType.FILE)

    ## Run Button        
    if (runKey := "runToggle") not in st.session_state:
        setState(runKey, False)
        
    #? Workaround for custom CSS; to allow this specific button to have default CSS values   
    st.write("")
    with st.form("NULLForm", border=False):
        st.form_submit_button(
            label               = "Link Submissions",
            disabled            = (not getState(runKey)),
            on_click            = lambda: _LINKER.__run(getState("redemptionToggle")),
            use_container_width = True
        )
    
    #? Check for runnable status & update runToggle state if either condition(s) met
    RT:     bool = getState("redemptionToggle")
    VALID:  bool = all(getState(key).valid for key in ["starterCode", "outputDir", "submissionsDir", "originalCSV"])
    RVALID: bool = False
    
    if getState("redemptionToggle"):
        RVALID = all((getState(key).valid for key in ["redemptionCSV", "redemptionSubsDir"]))
        
    setState(runKey, (all([not RT, VALID]) or all([RT, VALID, RVALID])))
 
    #* (~P ^ Q) v (P ^ Q ^ R)
            
            
    #! Send paths to PIILinker 
    #! Check for exceptions & grey outs for errors
    
    #> Use toast to show complete



#* --------------- Sub-menu example (horizontal) --------------- *#
def search() -> None:
    # TODO: Add Search GUI
    st.title("PII-Search v2-Beta [WiP]")
    
    ## Either use streamlit-searchbox or streamlit-keyup
    #! Don't forgor to add to requirements.txt
    

#* --------------- SETTINGS --------------- *#
def compare() -> None:
    # TODO: Add Compare50 GUI
    st.title('Compare50 [WiP]')
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
