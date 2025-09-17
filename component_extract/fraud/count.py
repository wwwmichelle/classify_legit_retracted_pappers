import re
import json
import numpy as np
from component_extract.legit.count_F1 import outputs_all

with open(r'C:\Users\21347\PycharmProjects\chatgpt_api\component_extract\fraud\fraud_component_extract_record.txt', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = '\[[^\]]*(?:Evidence|Claim|null)[^\]]*\]'

result = re.findall(pattern, content,flags=re.DOTALL)
print(result)
print(len(result))

all_output = []
n = 0
for i in result:
    n += 1
    try:
        format_content = i.replace("'null'", "null").replace("'Evidence'", '"Evidence"').replace("'Claim'", '"Claim"').replace('"null"', "null").replace(" Evidence", '"Evidence"').replace(" Claim", '"Claim"')
        output = json.loads(format_content)
        all_output.append(output)
    except Exception as e:
        print(n, e)
print(all_output)
print(len(all_output))

Claim_number_list = []
Evidence_number_list = []
for i in all_output:
    Claim_number = 0
    Evidence_number = 0
    for j in i:
        if j == "Claim":
            Claim_number += 1
        if j == "Evidence":
            Evidence_number += 1
    Evidence_number_list.append(Evidence_number)
    Claim_number_list.append(Claim_number)

#非法平均数、中位数、最大值、最小值
Evidence_min = min(Evidence_number_list)
Evidence_max = max(Evidence_number_list)
Evidence_mean = np.mean(Evidence_number_list)
Evidence_median = np.median(Evidence_number_list)
print(Evidence_median, Evidence_mean, Evidence_min, Evidence_max)
#4.0 4.71462829736211 0 16

Claim_min = min(Claim_number_list)
Claim_max = max(Claim_number_list)
Claim_mean = np.mean(Claim_number_list)
Claim_median = np.median(Claim_number_list)
print(Claim_median, Claim_mean, Claim_min, Claim_max)
#1.0 1.5947242206235013 0 7

Claim_number_list_else = []
Evidence_number_list_else = []
for i in outputs_all:
    Claim_number_else = 0
    Evidence_number_else = 0
    for x in i:
        if x == 'Claim':
            Claim_number_else += 1
        if x == 'Evidence':
            Evidence_number_else += 1
    Evidence_number_list_else.append(Evidence_number_else)
    Claim_number_list_else.append(Claim_number_else)

#合法平均数、中位数、最大值、最小值
Evidence_min_else = min(Evidence_number_list_else)
Evidence_max_else = max(Evidence_number_list_else)
Evidence_mean_else = np.mean(Evidence_number_list_else)
Evidence_median_else = np.median(Evidence_number_list_else)
print(Evidence_median_else, Evidence_mean_else, Evidence_min_else, Evidence_max_else)
#6.0 6.323420074349443 1 24

Claim_min_else = min(Claim_number_list_else)
Claim_max_else = max(Claim_number_list_else)
Claim_mean_else = np.mean(Claim_number_list_else)
Claim_median_else = np.median(Claim_number_list_else)
print(Claim_median_else, Claim_mean_else, Claim_min_else, Claim_max_else)
#2.0 1.788104089219331 0 7