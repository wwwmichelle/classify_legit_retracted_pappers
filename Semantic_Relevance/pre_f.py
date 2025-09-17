import json
import re
import Semantic_Relevance.embedding
from tqdm import tqdm
import numpy as np

print("非法")
with open(r'C:\Users\21347\PycharmProjects\chatgpt_api\merge_sentences\fraud\fraud_merge_sentence_record.txt', 'r', encoding='utf-8') as file:
    content_f = file.read()

pattern = r'\{[^{}]*\[[^\]]*\][^{}]*\}'
match_f = re.findall(pattern, content_f, flags=re.DOTALL)

print(len(match_f))
print(match_f)

output_f = []
for i in match_f:
    try:
        json_output_f = json.loads(i.replace(r"\xa0", ""))
        output_f.append(json_output_f)
    except Exception as e:
        print('出错',e,i)
print(len(output_f)) #416
print(output_f)


Claim_Evidence_f = []
Claim_no_Evidence_f = []
sims_mean_f = []
sims_max_f = []
sims_min_f = []
n = 0
for i in tqdm(output_f):
    relevant_f = []
    irrelevant_f = []
    sim_abs_f = []
    for x in i["Claim"]:
        for y in i["Evidence"]:
            sim = Semantic_Relevance.embedding.sentence_similarity(x,y)
            if sim > 0.8:
                n += 1
                relevant_f.append({"Claim":x, "Evidence":y})
                sim_abs_f.append(sim)
                print(n,sim)
        if not relevant_f:
            irrelevant_f.append({"Claim":x})
    Claim_Evidence_f.append(relevant_f)
    Claim_no_Evidence_f.append(irrelevant_f)
    if sim_abs_f:
        sims_mean_f.append(np.mean(sim_abs_f))
        sims_max_f.append(np.max(sim_abs_f))
        sims_min_f.append(np.min(sim_abs_f))
    else:
        sims_mean_f.append(0)
        sims_max_f.append(0)
        sims_min_f.append(0)

print(len(Claim_Evidence_f))
print(Claim_Evidence_f)
print(len(Claim_no_Evidence_f))
print(Claim_no_Evidence_f)
print(len(sims_mean_f))
print(sims_mean_f)
print(len(sims_max_f))
print(sims_max_f)
print(len(sims_min_f))
print(sims_min_f)