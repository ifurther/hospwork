import sys,os
import pytest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.cych import Cych

@pytest.mark.skip(reason="ssl eror")
def test_cych():
    cych = Cych()
    assert cych.url_base == 'https://www.cych.gov.tw'
    assert isinstance(cych.work_table,pd.DataFrame)
    assert isinstance(cych.admit_table,pd.DataFrame)
