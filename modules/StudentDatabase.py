from __future__ import annotations
import pandas as pd

class TypeMismatchError(Exception): pass #? Use when isinstance(obj, type) is False

class Student:
    
    def __init__(self, _first="NA", _last="NA", _UIN="NA", _email="NA", _section="", _SID="NA", _code=""):
        self.name:    str = f"{_first} {_last}"
        self.UIN:     str = _UIN
        self.email:   str = _email
        self.section: str = _section if _section else "NA"
        self.SID:     list[str] = [_SID]
        self.code:    str = _code
        
    def __eq__(self, rhs: Student) -> bool:
            """ Compare only NAME, UIN, and EMAIL """
            if not isinstance(rhs, Student):
                raise TypeMismatchError(f"Student::__eq__\n\tExpected type(rhs) -> Student\n\tActual type(rhs) -> {type(rhs)}")
            return (self.name, self.UIN, self.email, self.section) == (rhs.name, rhs.UIN, rhs.email, rhs.section)

    def __repr__(self) -> str:
        """ Custom representation including conditional section display """
        return f"{self.name} | UIN{self.UIN} | {self.section} | SID{self.SID}"



class StudentDatabase:
    
    def __init__(self) -> None:
        self.df:       pd.DataFrame       = pd.DataFrame()
        self.students: dict[str, Student] = {}    #* {uin, Student}
    
    def __getitem__(self, SID: str) -> Student | None:
        """ Returns student given submissionID """
        for _, student in self.students.items():
            if SID in student.SID:
                return student
        return None
            
            
    def __setitem__(self, SID: str, student: Student) -> None:
            """ Adds student to database """
            self.students[SID] = student
            
  
    def loadCSV(self, PATH: str="") -> None:
        """ Builds student database using CSV """
        _DF = pd.read_csv(
            PATH, 
            usecols=[
                "First Name",
                "Last Name",
                "SID",
                "Email",
                "Sections",
                "Submission ID",
                "Status"
            ]
        )
        
        # Rename columns for clarity and direct mapping
        _DF.rename(
            columns={
                'SID'           : 'UIN', 
                'Submission ID' : 'SID',
                'Sections'      : 'section',
                'Email'         : 'email',
                'First Name'    : 'first',
                'Last Name'     : 'last'
            },
            inplace=True
        )
        
        #* Filter rows where Status is "Graded"
        _DF = _DF[_DF['Status'] == 'Graded']
        
        # Iterate over the DataFrame rows and create Student instances
        for _, row in _DF.iterrows():
            
            if row['UIN'] in self.students: #? Handles redemption
                self.students[row['UIN']].SID += [row['SID']]
            else:
                self.students[row['UIN']] = Student(
                    first   = row['first'],
                    last    = row['last'],
                    SID     = row['SID'],
                    UIN     = row['UIN'],
                    email   = row['email'],
                    section = row['section']
                )
            
        #*
        self.df = pd.concat([self.df, _DF], ignore_index=True) if self.df else _DF


#! Import into files which handle students; only 1 should ever exist
_STUDENTS = StudentDatabase()