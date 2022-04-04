class Hospital_work:
    def __init__(self, name, url_base, url_work, work_table):
        self.name = name
        self.work = work_table
        self.url_base = url_base
        self.url_work = url_work
    def url(self):
        return self.url_base+self.url_work
    def get_wrok_table(self):
        pass
