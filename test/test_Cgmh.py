import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.cgmh import Cgmh

def test_cgmh():
    cgmh = Cgmh()
    assert isinstance(cgmh.work_table,pd.DataFrame)
