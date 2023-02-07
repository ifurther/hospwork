import re,datetime

def clean_date(time_raw,dtype='str'):
    '''tansfer date'''

    if (roc_date:= re.sub('[年,月]','-',time_raw.replace('日','')) ) and roc_date != time_raw and (roc_year := roc_date.split('-')[0]+1911) and abs(roc_year - datetime.date.today().year) <= 3:
        time_new = time_raw.replace(roc_date.split('-')[0],roc_year)
    elif '/' in time_raw:
        time_new = time_raw.replace('/','-')
    else:
        time_new = time_raw
    if (time_raw_checked := re.search('\d+[-,/,年]\d{1,2}[-,/,月]\d{1,2}',time_new) ) and dtype == 'datetime':
        return datetime.datetime.strptime(time_raw_checked.group(0),"%Y-%m-%d").date()
    elif  (time_raw_checked := re.search('\d+[-,/,年]\d{1,2}[-,/,月]\d{1,2}',time_new) )  and dtype == 'str':
        return str(datetime.datetime.strptime(time_raw_checked.group(0),"%Y-%m-%d").date())
    else:
        print('Error:',time_raw)
        return time_raw
