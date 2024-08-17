import sys,os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.hospital_work import Hospitalwork

def test_url():
   class Hosp(Hospitalwork):
       def __init__(self):
            self.url_base = 'test'
            self.url_work = 'test'
            self.url_full = super().url()
   hosp = Hosp()
   assert hosp.url_full == 'testtest'
