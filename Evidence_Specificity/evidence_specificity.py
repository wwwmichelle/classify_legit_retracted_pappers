import json
from tqdm import tqdm
from openai import OpenAI
from Semantic_Relevance.pre_f import Claim_Evidence_f
import re
import numpy as np

client = OpenAI(
    api_key="sk-xxxx",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def evidence_specificity(text):
    prompt = """
You are an expert in scientific discourse analysis and natural language processing.  

You are given two pieces of text:  
- One is classified as 'Claim'  
- The other is classified as 'Evidence'  

Your task is to evaluate and score the **specificity and reliability** of the Evidence, i.e., whether it provides concrete experimental data, statistical results, or merely vague/general statements. More specific evidence (e.g., quantitative results, p-values, numerical comparisons) is considered stronger and more credible, while vague or generic statements are considered weaker.  

Instructions:  

1. Reasoning  
- Analyze the Evidence to identify whether it contains **specific details** such as numerical values, statistical results, experimental data, or precise comparisons.  
- If the Evidence only makes general, qualitative, or vague claims, note that it is less specific.  
- Explain your reasoning in **2–4 sentences**, referencing explicit elements of the Evidence to justify your evaluation.  
- Avoid assumptions—focus solely on what is written in the Evidence.  

2. Specificity Score (0 to 1, increments of 0.1)  
Use the following scale to rate the specificity of the Evidence:  
- **0 = Completely Vague**: No specific details, purely general statement.  
- **0.1 = Virtually Vague**: Very minimal specificity, only broad assertions.  
- **0.2 = Very Slightly Specific**: Contains extremely limited concrete detail.  
- **0.3 = Slightly Specific**: Provides a small concrete element but still mostly general.  
- **0.4 = Somewhat Specific**: Some detail, but incomplete or imprecise.  
- **0.5 = Moderately Specific**: Provides moderate details but lacks strong concreteness.  
- **0.6 = Fairly Specific**: Contains relevant detail but not comprehensive.  
- **0.7 = Specific**: Clearly includes concrete information, though not extensive.  
- **0.8 = Very Specific**: Strong, detailed evidence such as quantitative comparisons or statistics.  
- **0.9 = Highly Specific**: Provides comprehensive statistical or experimental data with clear context.  
- **1.0 = Perfectly Specific**: Contains thorough quantitative evidence (e.g., multiple numerical results, statistical tests, confidence intervals) that makes the claim highly credible.  

3. Additional Guidance  
- **Objectivity**: Base evaluation only on the given Evidence.  
- **Clarity**: Keep the explanation precise and concise.  
- **No assumptions**: Do not infer additional data or methods beyond what is explicitly stated.  

Here are the examples:
# Example 1:
{'Claim': 'Topical brimonidine showed an additive IOP-lowering effect to topical PG analogues, although its IOP-lowering effect was inferior to topical timolol as monotherapy.', 
'Evidence': 'When added to PG analogues, the IOP-lowering effect of brimonidine (-2.9 +/- 1.8 mmHg) was greater than that of the placebo (-2.1 +/- 1.8 mmHg) (p = 0.0010).'}
output: {"score": 0.9}

# Example 2:
{'Claim': 'In conclusion, clonidine was not superior to spironolactone in true resistant hypertensive patients, but the overall BP control was low (≈21%).', 
'Evidence': 'Patients with resistant hypertension (no office and ambulatory blood pressure [BP] monitoring control, despite treatment with 3 drugs, including a diuretic, for 12 weeks) were randomized to an additional 12-week treatment with spironolactone (12.5-50 mg QD) or clonidine (0.1-0.3 mg BID). From 1597 patients recruited, 11.7% (187 patients) fulfilled the resistant hypertension criteria.'
output: {"score": 0.8}

# Example 3:
{'Claim': 'In conclusion, clonidine was not superior to spironolactone in true resistant hypertensive patients, but the overall BP control was low (≈21%).', 
'Evidence': 'Compared with the spironolactone group (n=95), the clonidine group (n=92) presented similar rates of achieving the primary end point (20.5% versus 20.8%, respectively; relative risk, 1.01 [0.55-1.88]; P=1.00). Secondary end point analysis showed similar office BP (33.3% versus 29.3%) and ambulatory BP monitoring (44% versus 46.2%) control for spironolactone and clonidine, respectively.'}
output: {"score": 0.9}

Now, please carefully consider the following case 

"""
    user_prompt = f'/nHere is the texts:/n"{text}"/n'
    response = client.chat.completions.create(
        model="qwen3-32b",
        store=True,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_prompt
             }
        ],
        temperature=0,
        response_format={"type":"json_object"},
        extra_body={"enable_thinking": False},
        stream=False,
        timeout=100,
    )
    return response.choices[0].message.content.strip()


specificity_mean = []
specificity_max = []
specificity_min = []
for i in tqdm(Claim_Evidence_f):
    if i:
        specific = []
        for j in i:
            result = evidence_specificity(j)
            pattern = r'Specificity\s*Score\b[^\d]*(\d+\.\d)'
            score = re.findall(pattern, result, flags=re.DOTALL)
            for x in score:
                x = float(x)
                specific.append(x)
        if not specific:
            specific = 0
            print("出错", specific)
        specificity_mean.append(np.mean(specific))
        specificity_max.append(np.max(specific))
        specificity_min.append(np.min(specific))
    else:
        specificity_mean.append(0)
        specificity_max.append(0)
        specificity_min.append(0)

print(specificity_mean)
print(len(specificity_mean))
print(specificity_max)
print(len(specificity_max))
print(specificity_min)
print(len(specificity_min))
