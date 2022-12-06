import re

def findjobtype(job_type_clean):
    return re.search(r"[復,營,資,護,家,胸,皮,泌,眼,內,外,藥,麻,臨,急,病,兒,環]\w+[科,部,室,心,課]",job_type_clean).group(0)
