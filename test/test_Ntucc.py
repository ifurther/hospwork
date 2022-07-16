import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.ntucc import Ntucc

def test_ntucc():
    ntucc = Ntucc()
    assert ntucc.url_base == 'https://www.ntucc.gov.tw/ntucc/'
    assert isinstance(ntucc.work_table,pd.DataFrame)
    #assert isinstance(ntucc.admit_table,pd.DataFrame)
