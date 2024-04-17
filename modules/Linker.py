from os import getcwd, chdir, path, listdir, mkdir
from .StudentDatabase import _STUDENTS
from datetime import datetime as dt
import streamlit as st
import sys


#* Submission ID & PII Handler
class PIILinker:
    
    def __init__(self) -> None:
        self.FERPAMode:   bool      = 1      #? FERPA Mode Toggle
        
        self.csvDir        : str = ""        #? CSV Directory
        self.rootDir       : str = getcwd()  #? Directory of Main Execution
        self.outputDir     : str = getcwd()  #? Output Directory
        self.starterDir    : str = ""        #? Hold path to starter
        self.submissionDir : str = ""        #? Submissions Directory
        
        self.starterCode  : str       = ""   #? Holds combined starter code
        self.starterFiles : list[str] = []   #? List of .cpp/.h File Names in Starter Directory
        
        #* Redemption
        self.redemptionMode    : bool = 0    #? Redemption Mode
        self.redemptionSubsDir : str  = ""   #? Redemption submissions Directory
        self.redemptionCSVDir  : str  = ""   #? Redemption CSV Directory
    
    
    def setup(self) -> None:
        """ Grabs Starter-Code """
        self.starterFiles = [
            file for file in listdir(self.starterDir) 
                if file.endswith(".cpp") or file.endswith(".h")
        ]
        
        if not len(self.starterFiles): 
            print("[ERROR] Starter-Code Directory Contains 0 .h/.cpp File(s)", file=sys.__stderr__) #!! FIXME: Pipe to streamlit
            exit() #!! FATAL ERROR
        
        chdir(self.starterDir)
        NL2 = "\n\n"
        
        for i, sFile in enumerate(self.starterFiles, 0):
            with open(sFile, mode='r', encoding='utf-8', errors='ignore') as rFile:
                self.starterCode += f"{(NL2 if i else '')}/* ----- {sFile} | STARTER CODE ----- */\n\n{rFile.read()}"    
                
        chdir(self.rootDir)
        
    
    def link(self) -> None:
        """ Extracts Submissions for PII-linking """
        SUBMISSIONS = self.submissionDir if not self.redemptionMode else self.redemptionSubsDir
        REDEMPTION_HEADER = \
            f"{('\n'*6)}/* {('-'*15)} [REDEMPTION] {('-'*15)} */{('\n'*2)}" if self.redemptionMode else ""
        
        chdir(SUBMISSIONS) 
        for folder in listdir():
            STUDENT = _STUDENTS[SID := folder.strip().split('_')[-1]]
            chdir(path.join(SUBMISSIONS, folder)) 
            for file in self.starterFiles:       
                if file not in listdir(): 
                    #!!!! REDIRECT TO STREAMLIT
                    ## NOTE: Non-fatal
                    print(f"[WARNING] Missing {file} for:\n\t{repr(STUDENT)}", file=sys.__stderr__) 
                    continue
        
                with open(file, mode='r', encoding='utf-8', errors='ignore') as fileCode:
                    STUDENT.code += f"{REDEMPTION_HEADER}/* ----- {file} | " \
                                  + f"{(SID if self.FERPAMode else repr(STUDENT))} ----- */\n\n{fileCode.read()}"
                                  
            chdir(SUBMISSIONS) 
        chdir(self.rootDir) 
        
        
    def generate(self) -> None:
        """ Generates Folder PII-linked Code """
        PIISTAT = "FERPA" if self.FERPAMode else "Linked"
        fileID = f"{(T := dt.now()).month}-{T.year}_{T.second}"
        mkdir(EXPDIR := path.join(self.outputDir, f"{PIISTAT}_{fileID}")) 
        chdir(EXPDIR) 

        with open(file="0_STARTER.cpp", mode='w', encoding='utf-8', errors="ignore") as wFile: 
            wFile.write(self.starterCode)
                    
        for _, student in _STUDENTS.students.values():
            if not path.exists(STUDIR := path.join(EXPDIR, (FERPA := (f"{'_'.join(student.SID)}" if self.FERPAMode else '_'.join(student.name.split()))))):
                mkdir(STUDIR)     
            chdir(STUDIR) 
    
            with open(file=f"{FERPA}.cpp", mode='w', encoding='utf-8', errors="ignore") as wFile: 
                wFile.write(student.code)
                        
            chdir(EXPDIR) 
        chdir(self.rootDir) 
        

    def _run(self, _redMode: bool) -> bool:
        st.title(f"Linker::__run() Called. _redMode: {_redMode}")
        
    def hvhfjhgf(self, _redMode: bool) -> bool:
        
        """ Logic flow control for PII-Linker 
            !! TODO: Add "grey out" to "run" button if redemption check box
            !!       is selected, but no/invalid path was specified
        """
        try:
            self.setup()
            self.link(self.submissionDir)
            
            if self._redMode:
                self.link(self.redemptionSubsDir)
                
            self.generate()
        except:
            return 0 #!!! SWAP FOR RAISE TO PASS TO STREAMLIT
        return 1
    

#* Singleton; import into needed files
_LINKER = PIILinker()