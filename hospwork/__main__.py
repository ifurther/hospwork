#!/usr/bin/env python

import pandas as pd
import numpy as np
from tabulate import tabulate
import concurrent.futures
#sys.path.append(Path().cwd().parent.as_posix())
from . import Csmpt,Ylh,Ntuh,Cych,Vghks,Vghtpe,Hch,Ntucc,Vghtc,Cgmh,Vhcy
from .io.sqlite import to_sqlite

def main():
    csmpt, ylh, ntuh, vghks, hch, ntucc, vghtc, cgmh = Csmpt(), Ylh(), Ntuh(), Vghks(), Hch(), Ntucc(), Vghtc(), Cgmh()


    Full_work_table=[]
    Full_exam_table=[]
    Full_admit_table=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for cc in [csmpt, ylh, ntuh, hch, ntucc, vghks, vghtc, cgmh]:
            executor.map(cc.get_full_work_table())
            Full_work_table.append(cc.get_full_work_table())

            if hasattr(cc, 'exam_table') and len(cc.exam_table) > 0:
                Full_exam_table.append(cc.get_full_exam_table())
            else:
                print(cc.name,' don\'t have exam table')
            if hasattr(cc, 'admit_table') and len(cc.admit_table) > 0:
                Full_admit_table.append(cc.get_full_admit_table())
            else:
                print(cc.name,' don\'t have admit table')


    Full_work_table=pd.concat(Full_work_table, ignore_index=True).convert_dtypes()
    Full_exam_table=pd.concat(Full_exam_table, ignore_index=True).convert_dtypes()    
    Full_admit_table=pd.concat(Full_admit_table, ignore_index=True).convert_dtypes()
    Full_work_table['期限'] = Full_work_table['期限'].astype('str')
    Full_admit_table['期限'] = Full_admit_table['期限'].astype('str')
    Full_work_table[Full_work_table['召聘職稱'].isin(['醫學物理師'])]


    g=Full_work_table[Full_work_table['召聘職稱'].str.match(r'\S+(醫學物理師|放射師)')==True]
    print(Full_work_table)
    #print(g)
    print(tabulate(g, headers='keys', tablefmt="pretty"))
    to_sqlite(Full_work_table)
    to_sqlite(Full_exam_table,table_name = 'exam_table')
    to_sqlite(Full_admit_table,table_name = 'admit_table')
    #g.to_csv('test.csv')

if __name__ == '__main__':
    main()
