import sys,os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.hospital_work import Hospital_work

def test_url():
   class Hosp(Hospital_work):
       def __init__(self):
            self.url_base = 'test'
            self.url_work = 'test'
            self.url_full = super().url()
   hosp = Hosp()
   assert hosp.url_full == 'testtest'
