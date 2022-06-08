#!/usr/bin/env python
# coding: utf-8
import sys
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
import numpy as np

#sys.path.append(Path().cwd().parent.as_posix())
from . import Csmpt,Ylh,Ntuh,Cych,Vghks,Vghtpe

def main():
    csmpt, ylh, ntuh, cych, vghks, vghtpe = Csmpt(),Ylh(),Ntuh(),Cych(),Vghks(),Vghtpe()


    Full_work_table=[]
    for cc in [csmpt, ylh, ntuh, cych, vghks, vghtpe]:
        cc.get_full_work_table()
        Full_work_table.append(cc.get_full_work_table())


    Full_work_table=pd.concat(Full_work_table, ignore_index=True).convert_dtypes()


    Full_work_table[Full_work_table['召聘職稱'].isin(['醫學物理師'])]


    g=Full_work_table[Full_work_table['召聘職稱'].str.match(r'\S+(醫學物理師|放射師)')==True]
    print(Full_work_table)
    print(g)

    database = r"sqlite:///hospwork.db"

    # create a database connection
    db = create_engine(database)
    with db.connect() as conn:
        #Full_work_table = Full_work_table.fillna(value=np.nan, inplace=True)
        Full_work_table.to_sql('work_table', conn, if_exists='append', index=False)
    


