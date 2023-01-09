#!/usr/bin/env python
# coding: utf-8
import sys
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
import numpy as np

#sys.path.append(Path().cwd().parent.as_posix())
from . import Csmpt,Ylh,Ntuh,Cych,Vghks,Vghtpe,Cgmh
from .io.sqlite import to_sqlite

def main():
    csmpt, ylh, ntuh, cych, vghks, vghtpe, cgmh = Csmpt(),Ylh(),Ntuh(),Cych(),Vghks(),Vghtpe(),Cgmh()


    Full_work_table=[]
    for cc in [csmpt, ylh, ntuh, cych, vghks, vghtpe, cgmh]:
        cc.get_full_work_table()
        Full_work_table.append(cc.get_full_work_table())


    Full_work_table=pd.concat(Full_work_table, ignore_index=True).convert_dtypes()


    Full_work_table[Full_work_table['召聘職稱'].isin(['醫學物理師'])]


    g=Full_work_table[Full_work_table['召聘職稱'].str.match(r'\S+(醫學物理師|放射師)')==True]
    to_sqlite(g)
    print(Full_work_table)
    print(g)


