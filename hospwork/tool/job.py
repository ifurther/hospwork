import re

def clean_unused_str(job_text,name)->str:
    '''clean the unused text'''
    return job_text.replace('：','').replace("-","").replace('【徵才公告】','').replace("【徵的就是你/妳】","").replace(name,'').replace('【徵才】','')
def findjobtype(job_type_clean)-> str:
    '''find the job originzation'''
    return re.search(r"[放,復,營,資,護,家,胸,皮,泌,眼,內,外,藥,麻,臨,急,病,兒,環,健]\w+[科,部,室,心,課]",job_type_clean).group(0)
