import re,datetime

def transfer_year(time_raw):
    '''transfer year from roc to ac'''
    roc_date = time_raw
    if (roc_year := int(roc_date.split('-')[0]) ) and roc_year < 1911 and abs( (roc_year + 1911) - datetime.date.today().year) <= 3:
        time_new = roc_date.replace(roc_date.split('-')[0],str(roc_year + 1911))
    else:
        time_new = roc_date   
    return time_new
 
def clean_date(time_raw,hosp_name,dtype='str'):
    '''tansfer date'''
    if (time_:= re.sub('[年,月]','-',time_raw.replace('日','')) ) and time_ != time_raw:
        time_new = transfer_year(time_)
    elif '/' in time_raw:
        if len(time_raw.split('/')) < 3:
            return time_raw
        else:
            time_new = transfer_year(time_raw.replace('/','-'))
    else:
        time_new =  transfer_year(time_raw)
    if (time_raw_checked := re.search('\d+[-,/,年]\d{1,2}[-,/,月]\d{1,2}',time_new) ) and dtype == 'datetime':
        return datetime.datetime.strptime(time_raw_checked.group(0),"%Y-%m-%d").date()
    elif (time_raw_checked := re.search('\d+[-,/,年]\d{1,2}[-,/,月]\d{1,2}',time_new) )  and dtype == 'str':
        return str(datetime.datetime.strptime(time_raw_checked.group(0),"%Y-%m-%d").date())
    else:
        print(hosp_name,'Error clear time data and time raw data is :',time_raw)
        return time_raw
