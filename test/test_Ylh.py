import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.ylh import Ylh

def test_ylh():
    ylh = Ylh()
    assert ylh.url_base == 'https://www.ylh.gov.tw'
    assert isinstance(ylh.work_table,pd.DataFrame)
