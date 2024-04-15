from .StudentDatabase import _STUDENTS 
import pandas as pd
import threading
import os

#! Users should be able to search regardless of PIILinker's status
#!! Users need to be able to search using 1 SID for students with 2 SIDs


class InvalidCSVPath(Exception): pass

class PIISearch:
    
    def __init__(self, path: str) -> None:
            self.PATH: str = path
            self.data: pd.DataFrame = pd.DataFrame() #? Use if not using PIILinker data
            
            
    def load_csv(self):
        pass