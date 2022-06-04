class Hospital_work():
    def __init__(self):
        self.url_full = self.url()
    def url(self):
        return self.url_base+self.url_work
    def get_wrok_table(self):
        pass
    def get_full_work_table(self):
        full_work_table = self.work_table
        full_work_table['source'] = self.name
        self.full_work_table = full_work_table
        return self.full_work_table
