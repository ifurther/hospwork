#!/usr/bin/env python

import pandas as pd
import numpy as np
from tabulate import tabulate

#sys.path.append(Path().cwd().parent.as_posix())
from . import Csmpt,Ylh,Ntuh,Cych,Vghks,Vghtpe,Hch,Ntucc,Vghtc,Cgmh,Vhcy
from .io.sqlite import to_sqlite

def main():
    csmpt, ylh, ntuh, vghks, vghtpe, hch, ntucc, vghtc, cgmh, vhcy = Csmpt(), Ylh(), Ntuh(), Vghks(), Vghtpe(), Hch(), Ntucc(), Vghtc(), Cgmh(), Vhcy()


    Full_work_table=[]
    Full_admit_table=[]
    for cc in [csmpt, ylh, ntuh, hch, ntucc, vghks, vghtpe, vghtc, vhcy, cgmh]:
        cc.get_full_work_table()
        Full_work_table.append(cc.get_full_work_table())
        if len(cc.admit_table) > 0:
            Full_admit_table.append(cc.get_full_admit_table())


    Full_work_table=pd.concat(Full_work_table, ignore_index=True).convert_dtypes()
    Full_admit_table=pd.concat(Full_admit_table, ignore_index=True).convert_dtypes()


    Full_work_table[Full_work_table['召聘職稱'].isin(['醫學物理師'])]


    g=Full_work_table[Full_work_table['召聘職稱'].str.match(r'\S+(醫學物理師|放射師)')==True]
    print(Full_work_table)
    #print(g)
    print(tabulate(g, headers='keys', tablefmt="pretty")) 
    to_sqlite(Full_work_table)
    to_sqlite(Full_admit_table,table_name = 'admit_table')
    #g.to_csv('test.csv')

if __name__ == '__main__':
    main()
