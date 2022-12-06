import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.vghtpe import Vghtpe

def test_vghtpe():
    vghtpe = Vghtpe()
    assert vghtpe.url_base == 'https://www1.vghtpe.gov.tw/conscribe/'
    assert isinstance(vghtpe.work_table,pd.DataFrame)
    assert isinstance(vghtpe.admit_table,pd.DataFrame)
