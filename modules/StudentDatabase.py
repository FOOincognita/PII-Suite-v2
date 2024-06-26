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
            if not isinstance(rhs, Student): #!! CHANGE EXCEPTION NAME
                raise TypeMismatchError(f"Student::__eq__\n\tExpected type(rhs) -> Student\n\tActual type(rhs) -> {type(rhs)}")
            return (self.name, self.UIN, self.email, self.section) == (rhs.name, rhs.UIN, rhs.email, rhs.section)

    def __repr__(self) -> str:
        """ Custom representation including conditional section display """
        return f"{self.name} | UIN{self.UIN} | {self.section} | SID{self.SID}"



class StudentDatabase:
    
    def __init__(self) -> None:
        self.df:       pd.DataFrame       = pd.DataFrame()
        self.students: dict[str, Student] = {}    #* {uin, Student}
    
    def get(self, SID: str, _default=None) -> Student | None:
        """ Returns Student given 1 of each Student's submissionIDs (each student can have up to 2 submission IDs) """
        for student in self.students.values():
            if SID in student.SID:
                return student
        return _default 
    
    def __getitem__(self, SID: str) -> Student:
        """ Returns Student given 1 of each Student's submissionIDs (each student can have up to 2 submission IDs) """
        for student in self.students.values():
            if SID in student.SID:
                return student
        raise KeyError(f"StudentDatabase::__getitem__\n\tSID -> {SID}\n\tStudentDatabase -> {self}")
            
            
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
        
        #* Rename columns for clarity and direct mapping
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
            
        #* Convert UIN and SID to int strings (truncate decimal)
        _DF['UIN'] = _DF['UIN'].astype(int).astype(str).str.replace(',', '')
        _DF['SID'] = _DF['SID'].astype(int).astype(str)
        
        #* Replace empty entries in 'section' with "NA"
        _DF['section'].fillna("NA", inplace=True)
    
        
        # Iterate over the DataFrame rows and create Student instances
        for _, row in _DF.iterrows():
            
            if row['UIN'] in self.students: #? Handles redemption
                self.students[row['UIN']].SID += [row['SID']]
            else:
                self.students[row['UIN']] = Student(
                    _first   = row['first'],
                    _last    = row['last'],
                    _SID     = row['SID'],
                    _UIN     = row['UIN'],
                    _email   = row['email'],
                    _section = row['section']
                )
            
        #* Concatenate DataFrame to existing DataFrame or replace empty DataFrame
        self.df = _DF if self.df.empty else pd.concat([self.df, _DF], ignore_index=True)


    def writeLogs(self, PATH: str="") -> None:
        """ Writes student database to CSV """
        stuData = []
        
        for uin, student in self.students.items():
            SIDstr = ', '.join(student.SID)  # Join SID list into a single string separated by comma
    
            stuData.append([
                uin,
                student.name,
                SIDstr,
                student.section,
                student.email
            ])
        
        pd.DataFrame(stuData, columns=["UIN", "name", "SID", "section", "email"]).to_csv(PATH, index=False)

#! Import into files which handle students; only 1 should ever exist
_STUDENTS = StudentDatabase()