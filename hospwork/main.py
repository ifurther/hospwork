#!/usr/bin/env python
# coding: utf-8
import sys
from pathlib import Path
import pandas as pd

#sys.path.append(Path().cwd().parent.as_posix())
from . import Csmpt,Hch,Ylh,Ntuh,Cych,Vghks,Vghtpe


csmpt, hch, ylh, ntuh, cych, vghks, vghtpe = Csmpt(),Hch(),Ylh(),Ntuh(),Cych(),Vghks(),Vghtpe()



for cc in [csmpt, hch, ylh, ntuh, cych, vghks, vghtpe]:
    cc.get_full_work_table()


Full_work_table=[]
for cc in [csmpt, hch, ylh, ntuh, cych, vghks, vghtpe]:
    Full_work_table.append(cc.get_full_work_table())


Full_work_table=pd.concat(Full_work_table)


Full_work_table[Full_work_table['召聘職稱'].isin(['醫學物理師'])]


g=Full_work_table[Full_work_table['召聘職稱'].str.match(r'\S+(醫學物理師|放射師)')==True]


print(g)

