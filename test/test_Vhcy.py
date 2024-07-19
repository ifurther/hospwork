import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.vhcy import Vhcy

def test_vhcy():
    vhcy = Vhcy()
    assert isinstance(vhcy.work_table,pd.DataFrame)
    assert isinstance(vhcy.exam_table,pd.DataFrame)
    assert isinstance(vhcy.admit_table,pd.DataFrame)
    #assert not vhcy.work_table.empty, "work_table is null"
    #assert not vhcy.exam_table.empty, "exam_table is null"
    #assert not vhcy.admit_table.empty, "admit_table is null"
