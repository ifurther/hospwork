import re

def clean_unused_str(job_text,name)->str:
    '''clean the unused text'''
    clean_job_text = job_text.replace('：','').replace("-","")
    clean_job_text = clean_job_text.replace('【徵才公告】','').replace("【徵的就是你/妳】","")
    clean_job_text = clean_job_text.replace(name,'').replace('【徵才】','').replace("】","")
    clean_job_text = clean_job_text.replace("【","").replace('，請查照。','').replace("，請 查照。","")
    return clean_job_text
def findjobtype(job_type)-> str:
    '''find the job type'''
    try:
        return re.search(r"\B[科,短,社,契,牙,秘,醫,部,室,門,招,募,誠](.*)[員,理,工,師,生]",job_type).group(0).replace("招募","").replace('募','').replace("聘","")
    except AttributeError:
        print("Error find job type:",job_type)
        return job_type
def findjoboriginzation(job_type):
    '''find the job originzation'''
    try:
        return re.search(r"([運,腎,心,生,婦,神,5,管,新,教,影,癌,血,牙,腦,骨,巨,工,傳,耳,放,復,營,資,護,家,胸,皮,泌,眼,外,藥,麻,臨,急,病,兒,環,健](\w+||)[科,部,室,心,課,處,房,局,組])|([內,中](\w+||)[科,局])",job_type).group(0)
    except AttributeError:
        print("Error find originzation: {}".format(job_type))
        return job_type
    except re.error as Re:
        print("Error find originzation: {}, its error: {}".format(job_type,Re))
        return job_type    
