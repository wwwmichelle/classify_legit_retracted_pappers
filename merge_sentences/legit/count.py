import re
import json
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'SimSun' #中文使用宋体
plt.rcParams['mathtext.fontset'] = 'stix' #数学公式字体

with open('legit_merge_sentence_record.txt', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = '\{\s*"Evidence"\s*:\s*\d+\s*,\s*"Claim"\s*:\s*\d+\s*\}'
result = re.findall(pattern, content, flags=re.DOTALL)
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
print(Evidence_mean, Evidence_median, Evidence_min, Evidence_max)
#2.587121212121212 2.0 1 16

Claim_min = min(Claim_number_list)
Claim_max = max(Claim_number_list)
Claim_mean = np.mean(Claim_number_list)
Claim_median = np.median(Claim_number_list)
print(Claim_mean, Claim_median, Claim_min, Claim_max)
#1.678030303030303 2.0 0 5


with open(r"..\fraud\fraud_merge_sentence_record.txt", 'r', encoding='utf-8') as file:
    content_else = file.read()

pattern_else = '\{\s*"Evidence"\s*:\s*\d+\s*,\s*"Claim"\s*:\s*\d+\s*\}'
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
print(Evidence_mean_else, Evidence_median_else, Evidence_min_else, Evidence_max_else)
#1.9782082324455206 2.0 0 6

Claim_min_else = min(Claim_number_list_else)
Claim_max_else = max(Claim_number_list_else)
Claim_mean_else = np.mean(Claim_number_list_else)
Claim_median_else = np.median(Claim_number_list_else)
print(Claim_mean_else, Claim_median_else, Claim_min_else, Claim_max_else)
#1.414043583535109 1.0 0 5

#绘图
plt.figure(figsize=(6,4),dpi=150)
plt.title('论据数对比')
plt.violinplot([Evidence_number_list, Evidence_number_list_else],
            showmeans=True
)
plt.show()

plt.figure(figsize=(6,4),dpi=150)
plt.title('论点数对比')
plt.violinplot([Claim_number_list, Claim_number_list_else],
            showmeans=True
)
plt.show()