#!/usr/bin/env python

import pandas as pd
import numpy as np

#sys.path.append(Path().cwd().parent.as_posix())
from . import Csmpt,Ylh,Ntuh,Cych,Vghks,Vghtpe,Hch,Ntucc,Vghtc
from .io.sqlite import to_sqlite

def main():
    csmpt, ylh, ntuh, cych, vghks, vghtpe, hch, ntucc, vghtc= Csmpt(),Ylh(),Ntuh(),Cych(),Vghks(),Vghtpe(), Hch(), Ntucc(), Vghtc()


    Full_work_table=[]
    for cc in [csmpt, ylh, ntuh, cych, vghks, vghtpe, hch, ntucc, vghtc]:
        cc.get_full_work_table()
        Full_work_table.append(cc.get_full_work_table())


    Full_work_table=pd.concat(Full_work_table, ignore_index=True).convert_dtypes()


    Full_work_table[Full_work_table['召聘職稱'].isin(['醫學物理師'])]


    g=Full_work_table[Full_work_table['召聘職稱'].str.match(r'\S+(醫學物理師|放射師)')==True]
    print(Full_work_table)
    print(g)

    to_sqlite(Full_work_table)
    #g.to_csv('test.csv')

if __name__ == '__main__':
    main()
