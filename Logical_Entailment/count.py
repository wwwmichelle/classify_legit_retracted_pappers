import re
import json
import numpy as np

#合法
with open('score0.85/legit_logical_entailment_record.txt', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'Support\s*Score\b[^\d]*(\d+\.\d)'
result = re.findall(pattern, content, flags=re.DOTALL)
print(result)
print(len(result))

all_output = []
for i in result:
    try:
        i = float(i)
        all_output.append(i)
    except Exception as e:
        print(e)
        print(i)

print(len(all_output))
print(all_output)

#合法平均数、中位数、最大值、最小值
score_min = min(all_output)
score_max = max(all_output)
score_mean = np.mean(all_output)
score_median = np.median(all_output)
print(score_median, score_mean, score_min, score_max)
#合法：570组Claim_Evidence
#0.5 0.5133333333333334 0.0 1.0
#合法：254组Claim_Evidence
#0.6 0.5307086614173228 0.0 1.0


#非法
with open('score0.85/fraud_logical_entailment_record.txt', 'r', encoding='utf-8') as file:
    content_f = file.read()

pattern = r'Support\s*Score\b[^\d]*(\d+\.\d)'
result_f = re.findall(pattern, content_f, flags=re.DOTALL)
print(result_f)
print(len(result_f))

all_output_f = []
for i in result_f:
    try:
        i = float(i)
        all_output_f.append(i)
    except Exception as e:
        print(e)
        print(i)

print(len(all_output_f))
print(all_output_f)

#非法平均数、中位数、最大值、最小值
score_min_f = min(all_output_f)
score_max_f = max(all_output_f)
score_mean_f = np.mean(all_output_f)
score_median_f = np.median(all_output_f)
print(score_median_f, score_mean_f, score_min_f, score_max_f)
#合法：798组Claim_Evidence
#0.7 0.6355889724310776 0.0 1.0
#合法：589组Claim_Evidence
#0.7 0.6732993197278911 0.0 1.0
