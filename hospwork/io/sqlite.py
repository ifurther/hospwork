#!/usr/bin/env python
# coding: utf-8
import sys
from sqlalchemy import create_engine
from sqlalchemy.types import JSON
from pathlib import Path
import pandas as pd
import numpy as np


def to_sqlite(Full_work_table,table_name = 'work_table', database = "sqlite:///hospwork.db"):

    # create a database connection
    db = create_engine(database)
    Full_work_table.to_sql(table_name, db, if_exists='replace', index=False, dtype={'name_of_json_column_in_source_table': JSON})
    print('success')


