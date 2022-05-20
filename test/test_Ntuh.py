import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.ntuh import Ntuh

def test_ntuh():
    ntuh = Ntuh()
    assert ntuh.url_base == 'https://www.ntuh.gov.tw/'
    assert isinstance(ntuh.work_table,pd.DataFrame)
