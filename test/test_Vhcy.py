import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.vhcy import Vhcy

def test_vhcy():
    vhcy = Vhcy()
    assert isinstance(vhcy.work_table,pd.DataFrame)
