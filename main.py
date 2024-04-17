import streamlit as st

from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer as dfExplorer

from views.linkView import link
from views.C50View import compare
from views.searchView import search
from views.settingsView import settings



#* ---------- WORK IN PROGRESS ---------- *
    #? Add persistent memory maybe?? idk
    #> Add streamlit-on-Hover-tabs
    ## Add st.file_uploader for C50 runs
    ## Add Archive Support


#* --------------- GLOBAL CONFIG --------------- *#
st.set_page_config(
    page_title = "PII-Suite v2-β", 
    page_icon  = "assets/favicon.png",
    layout     = "centered", #> wide
    menu_items = {             
        "Get help" : 'https://github.com/FOOincognita/PII-Suite-v2', 
        'Report a bug'  : "https://github.com/FOOincognita/UI/", #! ADD LINK
        'About'         : "Texas A&M University Department of Computer Science & Engineering" #! ADD INFO
    }
)

def main() -> None:
    with st.sidebar:
        tab = option_menu(
            default_index = 0,
            menu_title    = "PII-Suite v2-β",
            menu_icon     = "code-slash", 
            options       = ["Link", "Search", "Compare50", "Settings"] , 
            icons         = ["link-45deg", "person-bounding-box", "person-vcard", "sliders"],
        )
    
    match tab:
        case 'Link':      link() #? Should Link & Search be on same view, sub-menu, or seperate views?
        case 'Search':    search()
        case 'Compare50': compare()
        case 'Settings':  settings()
        case _:
            st.exception(RuntimeError("[ERROR]: Default Case Reached in main()"))


if __name__ == "__main__":
    main()
