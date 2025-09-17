import re
import json

with open(r"C:\Users\21347\PycharmProjects\chatgpt_api\component_extract\legit\component_extract_record.txt", encoding="utf-8") as f:
    content = f.read()

content = content.replace('\\', '')

"""提取并解析标签列表，返回清洗后的列表"""
raw = re.findall(r'"answer"\s*:\s*\[(.*?)\]', content, flags=re.DOTALL)
preds = re.findall(r'### Final Output.*?\[(.*?)\]', content, flags=re.DOTALL)
print(len(raw))
print(len(preds))

result = []
outputs_all = []
for a, p in zip(raw, preds):
    labels = json.loads("[" + a.replace('"null"', "null") + "]")
    outputs = json.loads("[" + p.replace('"null"', "null").replace(' Evidence', ' "Evidence"').replace(' Claim', ' "Claim"') + "]")
    labels = [x if x in ["Claim", "Evidence"] else None for x in labels]
    outputs = [x if x in ["Claim", "Evidence"] else None for x in outputs]
    result.append((labels, outputs))
    outputs_all.append(outputs)

print(result)
print(len(result))
print(outputs_all)
print(len(outputs_all))

Evidence_TP = 0
Evidence_FP = 0
Evidence_FN = 0
Claim_TP = 0
Claim_FP = 0
Claim_FN = 0
for i in result:
    for x, y in zip(i[0], i[1]):
        if x == "Evidence" and y == "Evidence":
            Evidence_TP += 1
        if (x == "Claim" or x is None) and y == "Evidence":
            Evidence_FP += 1
        if x == "Evidence" and (y == "Claim" or y is None):
            Evidence_FN += 1
        if x == "Claim" and y == "Claim":
            Claim_TP += 1
        if (x == "Evidence" or x is None) and y == "Claim":
            Claim_FP += 1
        if x == "Claim" and (y == "Evidence" or y is None):
            Claim_FN += 1


Evidence_R = Evidence_TP / (Evidence_TP + Evidence_FN)
Evidence_P = Evidence_TP / (Evidence_TP + Evidence_FP)
Evidence_F1 = 2 * Evidence_R * Evidence_P / (Evidence_R + Evidence_P)

Claim_R = Claim_TP / (Claim_TP + Claim_FN)
Claim_P = Claim_TP / (Claim_TP + Claim_FP)
Claim_F1 = 2 * Claim_R * Claim_P / (Claim_R + Claim_P)

Average_F1 = (Evidence_F1 + Claim_F1) / 2

print(Evidence_F1, Evidence_P, Evidence_R, Claim_F1, Claim_P, Claim_R, Average_F1)




