import re

def clean_unused_str(job_text,name)->str:
    '''clean the unused text'''
    return job_text.replace('：','').replace("-","").replace('【徵才公告】','').replace("【徵的就是你/妳】","").replace(name,'').replace('【徵才】','')
def findjobtype(job_type)-> str:
    '''find the job type'''
    try:
        return re.search(r"\B[科,短,社,契,牙,秘,醫,部,室](.*)[員,理,工,師,生]",job_type).group(0)
    except AttributeError:
        print("ERROR:",job_type)
        return job_type
def findjoboriginzation(job_type):
    '''find the job originzation'''
    return re.search(r"[放,復,營,資,護,家,胸,皮,泌,眼,內,外,藥,麻,臨,急,病,兒,環,健]\w+[科,部,室,心,課]",job_type).group(0)
