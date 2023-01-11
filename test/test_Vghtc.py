import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.vghtc import Vghtc

def test_vghtc():
    vghtc = Vghtc()
    assert vghtc.url_base == 'https://www.vghtc.gov.tw'
    assert isinstance(vghtc.work_table,pd.DataFrame)
    assert not vghtc.work_table.empty, "work_table is null"
    assert isinstance(vghtc.admit_table,pd.DataFrame)
    assert not vghtc.admit_table.empty, "admit_table is null"
