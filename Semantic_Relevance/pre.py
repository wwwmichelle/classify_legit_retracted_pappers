import json
import re
import Semantic_Relevance.embedding
from tqdm import tqdm
import numpy as np

print("合法")
with open(r'..\merge_sentences\legit\legit_merge_sentence_record.txt', 'r', encoding='utf-8') as f:
    content = f.read()

pattern_1 = r'\{[^{}]*\[[^\]]*\][^{}]*\}'
match_1 = re.findall(pattern_1, content, flags=re.DOTALL)

pattern_2 = r'\{\s*"Evidence":\s*\d+\s*,\s*"Claim":\s*\d+\s*\}'
match_2 = re.findall(pattern_2, content, flags=re.DOTALL)

print(len(match_1))
print(match_1)
print(len(match_2))
print(match_2)


output = []
for i,j in zip(match_1,match_2):
    try:
        json_output = json.loads(i.replace(r"\xa0", ""))
        output.append(json_output)
    except Exception as e:
        print('出错',e,i)
print(len(output)) #268
print(output)

Claim_Evidence = []
Claim_no_Evidence = []
sims_mean = []
sims_max = []
sims_min = []
n = 0
for i in tqdm(output):
    relevant = []
    irrelevant = []
    sim_abs = []
    for x in i["Claim"]:
        for y in i["Evidence"]:
            sim = Semantic_Relevance.embedding.sentence_similarity(x,y)
            if sim > 0.8:
                n += 1
                relevant.append({"Claim":x, "Evidence":y})
                sim_abs.append(sim)
                print(n,sim)
        if not relevant:
            irrelevant.append({"Claim":x})
    Claim_Evidence.append(relevant)
    Claim_no_Evidence.append(irrelevant)
    if sim_abs:
        sims_mean.append(np.mean(sim_abs))
        sims_max.append(np.max(sim_abs))
        sims_min.append(np.min(sim_abs))
    else:
        sims_mean.append(0)
        sims_max.append(0)
        sims_min.append(0)

print(len(Claim_Evidence))
print(Claim_Evidence)
print(len(Claim_no_Evidence))
print(Claim_no_Evidence)
print(len(sims_mean))
print(sims_mean)
print(len(sims_max))
print(sims_max)
print(len(sims_min))
print(sims_min)