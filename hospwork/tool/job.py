import re

def clean_unused_str(job_text,name)->str:
    '''clean the unused text'''
    clean_job_text = job_text.replace('：','').replace("-","").replace(" ","")
    clean_job_text = clean_job_text.replace('【徵才公告】','').replace("【徵的就是你/妳】","")
    clean_job_text = clean_job_text.replace(name,'').replace('【徵才】','').replace("】","")
    clean_job_text = clean_job_text.replace("【","").replace('，請查照。','').replace("，請 查照。","")
    clean_job_text = clean_job_text.replace("\xa0","").replace('\n',"").replace("\u3000","")
    return clean_job_text
def findjobtype(job_type,name)-> str:
    '''find the job type'''
    if '研究助理' in job_type:
        return '研究助理'
    elif '工讀生' in job_type:
        return '工讀生'
    try:
        return re.search(r"\B[處,行,課,科,短,社,契,牙,秘,醫,部,室,門,招,募,誠,聘](.*)[員,理,工,師,生,廚,士]",job_type).group(0).replace("招募","").replace('募','').replace("聘","")
    except AttributeError:
        print("{} Error find job type: {}".format(name, job_type))
        return job_type
def findjoboriginzation(job_type,name):
    '''find the job originzation'''
    try:
        return re.search(r"([胃,實,失,醫,秘,核,運,腎,心,生,婦,神,5,管,新,教,影,癌,血,牙,腦,骨,巨,工,傳,耳,放,復,營,資,護,家,胸,皮,泌,眼,外,藥,麻,臨,人,急,主,病,兒,環,健,社](\w+||)[科,部,室,心,課,處,房,局,組,庫])|([內,中](\w+||)[科,局])",job_type.replace(name,"")).group(0)
    except AttributeError:
        print("{} Error find originzation: {}".format(name, job_type))
        return job_type
    except re.error as Re:
        print("{} Error find originzation: {}, its error: {}".format(name, job_type,Re))
        return job_type    
