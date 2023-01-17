class Hospital_work():
    def __init__(self):
        self.url_full = self.url()
        self.url_full_admit = self.url_admit()
    def url(self):
        return self.url_base+self.url_work
    def url_admit(self):
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
        return self.full_admit_table
    def get_full_admit_table(self):
        full_admit_table = self.admit_table
        full_admit_table['source'] = self.name
        self.full_admit_table = full_admit_table
        return self.full_admit_table

