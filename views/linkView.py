import streamlit as st
from modules.Explorer import Explorer, FileType #? Select files/folder for path
from modules.Linker import _LINKER #? Handles Linking; call PIILinker::__run()


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
    
    #? Check for runnable status & update runToggle state if either condition(s) met
    RT:     bool = getState("redemptionToggle")
    VALID:  bool = all(getState(key).valid for key in ["starterCode", "outputDir", "submissionsDir", "originalCSV"])
    RVALID: bool = False
    
    if getState("redemptionToggle"):
        RVALID = all((getState(key).valid for key in ["redemptionCSV", "redemptionSubsDir"]))
        
    #!! setState(runKey, 1) #!!!(all([not RT, VALID]) or all([RT, VALID, RVALID])))
    
    #? Workaround for custom CSS; to allow this specific button to have default CSS values   
    st.write("")
    st.button(
        label               = "Link Submissions",
        disabled            = not (all([not RT, VALID]) or all([RT, VALID, RVALID])), #> ~((~P ^ Q) v (P ^ Q ^ R))
        on_click            = lambda: _LINKER._run(getState("redemptionToggle")),
        use_container_width = True
    )

    #! Send paths to PIILinker 
    #! Check for exceptions & grey outs for errors
    
    #> Use toast to show complete