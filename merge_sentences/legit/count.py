import re
import json
import numpy as np

with open('legit_merge_sentence_record.txt', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = '\{.*?\}'
result = re.findall(pattern, content, flags=re.DOTALL)
print(result)
print(len(result))


all_output = []
for i in result:
    try:
        output = json.loads(i.replace("'Evidence'", '"Evidence"').replace("'Claim'", '"Claim"'))
        all_output.append(output)
    except Exception as e:
        print(e)
        print(i)


Claim_number_list = []
Evidence_number_list = []
for i in all_output:
    Claim_number = 0
    Evidence_number = 0
    for j in i:
        if j == "Claim":
            Claim_number += i["Claim"]
        if j == "Evidence":
            Evidence_number += i["Evidence"]
    Evidence_number_list.append(Evidence_number)
    Claim_number_list.append(Claim_number)

#合法平均数、中位数、最大值、最小值
Evidence_min = min(Evidence_number_list)
Evidence_max = max(Evidence_number_list)
Evidence_mean = np.mean(Evidence_number_list)
Evidence_median = np.median(Evidence_number_list)
print(Evidence_median, Evidence_mean, Evidence_min, Evidence_max)
#3.0 2.903703703703704 1 14

Claim_min = min(Claim_number_list)
Claim_max = max(Claim_number_list)
Claim_mean = np.mean(Claim_number_list)
Claim_median = np.median(Claim_number_list)
print(Claim_median, Claim_mean, Claim_min, Claim_max)
#2.0 1.6851851851851851 0 5


with open(r"C:\Users\21347\PycharmProjects\chatgpt_api\merge_sentences\fraud\fraud_merge_sentence_record.txt", 'r', encoding='utf-8') as file:
    content_else = file.read()

pattern_else = '\{.*?\}'
result_else = re.findall(pattern_else, content_else, flags=re.DOTALL)
print(result_else)
print(len(result_else))

all_output_else = []
for i in result_else:
    try:
        output_else = json.loads(i.replace("'Evidence'", '"Evidence"').replace("'Claim'", '"Claim"'))
        all_output_else.append(output_else)
    except Exception as e:
        print(e)
        print(i)
print(len(all_output_else))
print(all_output_else)

Claim_number_list_else = []
Evidence_number_list_else = []
for i in all_output_else:
    Claim_number_else = 0
    Evidence_number_else = 0
    for x in i:
        if x == "Claim":
            Claim_number_else += i["Claim"]
        elif x == "Evidence":
            Evidence_number_else += i["Evidence"]
        else:
            print(x)
    Evidence_number_list_else.append(Evidence_number_else)
    Claim_number_list_else.append(Claim_number_else)

#非法平均数、中位数、最大值、最小值
Evidence_min_else = min(Evidence_number_list_else)
Evidence_max_else = max(Evidence_number_list_else)
Evidence_mean_else = np.mean(Evidence_number_list_else)
Evidence_median_else = np.median(Evidence_number_list_else)
print(Evidence_median_else, Evidence_mean_else, Evidence_min_else, Evidence_max_else)
#2.0 2.350835322195704 0 8

Claim_min_else = min(Claim_number_list_else)
Claim_max_else = max(Claim_number_list_else)
Claim_mean_else = np.mean(Claim_number_list_else)
Claim_median_else = np.median(Claim_number_list_else)
print(Claim_median_else, Claim_mean_else, Claim_min_else, Claim_max_else)
#1.0 1.422434367541766 0 5

