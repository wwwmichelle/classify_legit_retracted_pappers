import json
from component_extract.legit.count_F1 import outputs_all

with open('legit/AbstRCT_test.json') as f:
    data = json.load(f)
abstracts = []
for i in data:
    abstracts.append(data[i]["sentences"])
print(len(abstracts))

Evidence_all = []
Claim_all = []
n = 0
for x, y in zip(abstracts, outputs_all):
    n += 1
    if len(x) == len(y):
        Evidence = []
        Claim = []
        for j in range(len(y)):
            if y[j] == 'Evidence':
                Evidence.append(x[j])
            if y[j] == 'Claim':
                Claim.append(x[j])
        Evidence_all.append(Evidence)
        Claim_all.append(Claim)
    else:
        print("出错",n,len(x),len(y))

print(len(Evidence_all))
print(len(Claim_all))

data_all = []
for i in range(len(Claim_all)):
    content = f"Evidence:{Evidence_all[i]}\nClaim:{Claim_all[i]}"
    data_all.append(content)

print(data_all)
print(len(data_all))

'''
出错 35 14 13
出错 57 9 8
出错 58 15 14
出错 59 13 12
出错 63 9 8
出错 65 12 11
出错 67 12 11
出错 69 13 12
出错 71 16 15
出错 78 12 11
出错 81 13 12
出错 142 18 19
出错 154 18 19
出错 219 7 8
出错 266 17 16
出错 313 9 8
出错 391 18 17
出错 395 14 15
出错 402 22 23
出错 409 21 20
出错 415 8 6
396
'''