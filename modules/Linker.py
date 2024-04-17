from os import getcwd, chdir, path, listdir, mkdir
from .StudentDatabase import _STUDENTS
from datetime import datetime as dt
import streamlit as st
from enum import Enum
import sys

class InvalidStarterCode(RuntimeError): pass
class SIDNotFound(RuntimeError): pass #? When searching for a student by SID, no result was found


class LinkType(Enum):
    ORIGINAL   = 0
    REDEMPTION = 1


#* Submission ID & PII Handler
class PIILinker:
    
    def __init__(self) -> None:
        self.FERPAMode: bool = 1             #? FERPA Mode Toggle
        
        self.csvDir        : str = ""        #? CSV Directory
        self.rootDir       : str = getcwd()  #? Directory of Main Execution
        self.outputDir     : str = ""        #? Output Directory
        self.starterDir    : str = ""        #? Hold path to starter
        self.submissionDir : str = ""        #? Submissions Directory
        
        self.starterCode  : str       = ""   #? Holds combined starter code
        self.starterFiles : list[str] = []   #? List of .cpp/.h File Names in Starter Directory
        
        ## Redemption
        self.redemptionMode    : bool = 0    #? Redemption Mode
        self.redemptionCSVDir  : str  = ""   #? Redemption CSV Directory
        self.redemptionSubsDir : str  = ""   #? Redemption submissions Directory
    
    
    def setup(self) -> None:
        """ Grabs Starter-Code

            raises:
                InvalidStarterCode: If starter-code directory does not contain any .h/.cpp files
        """
        self.starterFiles = [
            file for file in listdir(self.starterDir) 
                if file.endswith(".cpp") or file.endswith(".h")
        ]
        
        ## Starter Code Exception
        if not len(self.starterFiles): 
            raise InvalidStarterCode(f"{self.starterDir}")
        
        ## Read Starter Code
        chdir(self.starterDir)
        NL2 = "\n\n"
        
        for i, sFile in enumerate(self.starterFiles, 0):
            with open(sFile, mode='r', encoding='utf-8', errors='ignore') as rFile:
                self.starterCode += f"{(NL2 if i else '')}/* ----- {sFile} | STARTER CODE ----- */\n\n{rFile.read()}"    
                
        chdir(self.rootDir)
        
        ## Load CSV(s)
        _STUDENTS.loadCSV(self.csvDir)
        if self.redemptionMode:
            _STUDENTS.loadCSV(self.redemptionCSVDir)
        
        _STUDENTS.writeLogs(path.join("logs", "studentDatabase.csv")) #!! FOR DEBUG ONLY
        
    
    def link(self, __type: LinkType) -> None:
        """ Extracts Submissions for PII-linking
            raises:
                SIDNotFound: If SID is not found in StudentDatabase (_STUDENTS)
        
        """
        SUBMISSIONS = self.redemptionSubsDir if __type.value else self.submissionDir 
        REDEMPTION_HEADER = \
            f"{('\n'*6)}/* {('-'*15)} [REDEMPTION] {('-'*15)} */{('\n'*2)}" if __type.value else ""
        
        chdir(SUBMISSIONS) 
        for folder in listdir():
            if not path.isdir(folder): continue #? Prevents exceptions when the yml is present
            try:
                STUDENT = _STUDENTS[SID := folder.strip().split('_')[-1]]
            except KeyError:
                raise SIDNotFound(f"{SID}")
                
            chdir(path.join(SUBMISSIONS, folder)) 
            for file in self.starterFiles:       
                if file not in listdir(): 
                    ## NOTE: Non-fatal
                    print(f"[WARNING] Missing {file} for:\n\t{repr(STUDENT)}", file=sys.__stderr__) 
                    continue
        
                with open(file, mode='r', encoding='utf-8', errors='ignore') as fileCode:
                    STUDENT.code += f"{REDEMPTION_HEADER}/* ----- {file} | " \
                                  + f"{('_'.join(SID) if self.FERPAMode else repr(STUDENT))} ----- */\n\n{fileCode.read()}"
                                  
            chdir(SUBMISSIONS) 
        chdir(self.rootDir) 
        
        
    def generate(self) -> None:
        """ Generates Folder PII-linked Code """
        PIISTAT = "FERPA" if self.FERPAMode else "Linked"
        PIISTAT += "_REDEMPTION_" if self.redemptionMode else ""
        fileID = f"{(T := dt.now()).month}-{T.year}_{T.second}"
        mkdir(EXPDIR := path.join(self.outputDir, f"{PIISTAT}_{fileID}")) 
        chdir(EXPDIR) 

        with open(file="0_STARTER.cpp", mode='w', encoding='utf-8', errors="ignore") as wFile: 
            wFile.write(self.starterCode)
                    
        for student in _STUDENTS.students.values():
            if not path.exists(STUDIR := path.join(EXPDIR, (FERPA := (f"{'_'.join(student.SID)}" if self.FERPAMode else '_'.join(student.name.split()))))):
                mkdir(STUDIR)     
            chdir(STUDIR) 
    
            with open(file=f"{FERPA}.cpp", mode='w', encoding='utf-8', errors="ignore") as wFile: 
                wFile.write(student.code)
                        
            chdir(EXPDIR) 
        chdir(self.rootDir) 
        
        
    def _update(self) -> None:
        #!! [FIXME]: WRITE SETTINGS TO JSON
        getState = lambda key: st.session_state.get(key)
        getPath  = lambda key: st.session_state.get(f"{key}_path")
        
        #* Mode Settings
        self.redemptionMode = getState("RedemptionToggle")
        self.FERPAMode      = getState("FERPAToggle")
        
        #* Original Paths
        self.submissionDir  = getPath("submissionsDir")
        self.starterDir     = getPath("starterDir")
        self.outputDir      = getPath("outputDir")
        self.csvDir         = getPath("originalCSV")
        
        #* Redemption Paths
        self.redemptionCSVDir  = getPath("redemptionCSV")
        self.redemptionSubsDir = getPath("redemptionSubsDir")
    
        
    def _run(self) -> None:
        """ Logic for PII-Linker """
        #* Update all variables
        self._update()
        
        #* Status Bar
        with st.status("Linking Submissions...", expanded=True) as status:
            ## Setup
            st.write("Running Setup...")
            try: 
                self.setup()
            except InvalidStarterCode as e: 
                status.update(label="Oospie Daisies...", state="error")
                st.exception(InvalidStarterCode(f"[FATAL] Starter-Code Directory Contains 0 .h/.cpp File(s)\n\tDirectory: {e}"))
                
            ## Link Submissions
            st.write("Linking Original Submissions...")
            try: 
                self.link(LinkType.ORIGINAL)
            except SIDNotFound as e:
                status.update(label="Oospie Daisies...", state="error")
                st.exception(SIDNotFound(f"[FATAL] SID {e} Not Found in Linker::link()"))
                
            ## Link Redemption Submissions
            if self.redemptionMode:
                st.write("Linking Redemption Submissions...")
                try:
                    self.link(LinkType.REDEMPTION)
                except SIDNotFound as e:
                    status.update(label="Oospie Daisies...", state="error")
                    st.exception(SIDNotFound(f"[FATAL] SID {e} Not Found in Linker::link(REDEMPTION)"))
            
            st.write("Writing Linked Submissions to Output...")   
            try:
                self.generate()
            except Exception as e:
                status.update(label="Oospie Daisies...", state="error")
                st.exception(Exception(f"[FATAL] Unknown Exception raised in Linker::generate()\n\tDetails: {e}"))
                
            status.update(label="Submissions Successfully Linked!", state="complete", expanded=False)

#* Singleton; import into needed files
_LINKER = PIILinker()