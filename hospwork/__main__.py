
from .hch import Hch
from .ylh import Ylh

import pandas as pd

if __name__ == '__main__':
    hch = Hch()
    hch.get_full_work_table()
    ylh = Ylh()
    ylh.get_full_work_table()
    print('Call it locally')
    print(pd.merge(hch.full_work_table,ylh.full_work_table))
