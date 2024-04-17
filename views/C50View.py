import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer as dfExplorer



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