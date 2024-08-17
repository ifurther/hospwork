import pandas as pd

class Hospitalwork():
    '''main class'''
    def __init__(self):
        self.name: str
        self.url_base: str
        self.url_work: str
        self.url_exam: str
        self.url_admit: str
        self.work_table: pd.DataFrame
        self.exam_table: pd.DataFrame
        self.admit_table: pd.DataFrame
        self.url_full = self.url()
        self.url_full_exam = self.get_url_full_exam()
        self.url_full_admit = self.get_url_full_admit()
    def url(self) -> str:
        '''return work url'''
        return self.url_base+self.url_work
    def get_url_full_exam(self) -> str:
        '''return exam url'''
        return self.url_base+self.url_exam
    def get_url_full_admit(self) -> str:
        '''return admit url'''
        return self.url_base+self.url_admit
    def get_wrok_table(self):
        pass
    def get_full_work_table(self):
        full_work_table = self.work_table
        full_work_table['source'] = self.name
        self.full_work_table = full_work_table
        return self.full_work_table
    def get_full_exam_table(self):
        full_exam_table = self.exam_table
        full_exam_table['source'] = self.name
        self.full_exam_table = full_exam_table
        return self.full_exam_table
    def get_full_admit_table(self):
        full_admit_table = self.admit_table
        full_admit_table['source'] = self.name
        self.full_admit_table = full_admit_table
        return self.full_admit_table

