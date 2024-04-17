import streamlit as st
from modules.Explorer import Explorer, FileType #? Select files/folder for path
from modules.Linker import _LINKER #? Handles Linking; call PIILinker::__run()


def link() -> None: ## TODO: ADD STUDENT & PIILinker CLASSES
    ## TODO redemption; archive support
    ## Maybe add stepper-bar?
    
    setState = lambda key, val: setattr(st.session_state, key, val)
    getState = lambda key:      st.session_state.get(key)
    
    st.title('Linker v2-β', anchor=False)
    
    #? Init redemption mode session state attr for global use
    if "redemptionToggle" not in st.session_state:
        setState("redemptionToggle", False)
    if "FERPAToggle" not in st.session_state:
        setState("FERPAToggle", True)
    
    #* Mode Selection   
    st.write(""); st.subheader("Mode Selection", anchor=False)
    with st.container(border=1):  
        FERPA = st.toggle("FERPA Mode", value=True, help="Names linked files using SubmissionID(s) rather than student names", )
        setState("FERPAToggle", FERPA)
        
        REDEMPTION = st.toggle("Redemption Mode", value=False, help="Enables redemption-submission linking given valid paths")
        setState("redemptionToggle", REDEMPTION)
    
    #> Init Explorers
    #! [FIXME]: It's possible allocating a session state variable may not be necessary
    #!! Maybe I need to write each of these to .json just to be sure?
    def _initExplorer(__name: str, __msg: str, __type: FileType):
        setState(__name, Explorer(__name, __msg, __type))
        
        match __type:
            case FileType.FOLDER: getState(__name).selectFolder()
            case FileType.FILE:   getState(__name).selectFile()
            case _:               st.exception(RuntimeError("[ERROR]: Default Reached in initExplorer()"))
    
    
    #* Original Submissions
    st.write(""); st.subheader("Original Submissions", anchor=False)
    with st.container(border=1):
        _initExplorer("starterDir",    "Select Starter Code Directory", FileType.FOLDER )
        _initExplorer("outputDir",      "Select Output Directory",       FileType.FOLDER)
        _initExplorer("submissionsDir", "Select Submissions Directory",  FileType.FOLDER)
        _initExplorer("originalCSV",    "Select CSV File",               FileType.FILE  )

    #* Redemption Submissions
    if REDEMPTION:
        st.write(''); st.subheader("Redemption Submissions", anchor=False) 
        with st.container(border=1):  
            _initExplorer("redemptionSubsDir", "Select Redemption Submissions", FileType.FOLDER)
            _initExplorer("redemptionCSV",     "Select Redemption CSV",         FileType.FILE)

    #* Run Button        
    RT:     bool = REDEMPTION #?? Just so it's shorter...
    VALID:  bool = all(getState(key).valid for key in ["starterDir", "outputDir", "submissionsDir", "originalCSV"])
    RVALID: bool = False
    
    if RT:
        RVALID = all((getState(key).valid for key in ["redemptionCSV", "redemptionSubsDir"]))
        
    RUNNABLE = not (all([not RT, VALID]) or all([RT, VALID, RVALID]))
      
    st.write("")
    st.button(
        label               = "Link Submissions",
        help                = "Run PII-Linker for selected files; all visable fields must contain valid paths",
        disabled            = not (all([not RT, VALID]) or all([RT, VALID, RVALID])), #> ~((~P ^ Q) v (P ^ Q ^ R))
        on_click            = lambda: _LINKER._run(),
        use_container_width = True
    )

    
    #* Use toast to show complete
    #* Add loading bar