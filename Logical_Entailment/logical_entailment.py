import json
from tqdm import tqdm
from openai import OpenAI
from Semantic_Relevance.pre import Claim_Evidence
import re
import numpy as np

client = OpenAI(
    api_key="sk-8d638c8f73e5469e839afb6d2c7f787b",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def logical_entailment(text):
    prompt = """
You are an expert in scientific discourse analysis and natural language processing. 

You are given two pieces of text, one is classified as 'Claim', the other one is classified as 'Evidence'.

Your task is to evaluate and score the degree to which the Evidence supports the Claim logically.

Instructions:
1. Reasoning
Analyze the Evidence by identifying key information and how it relates to the Claim.
Identify key information in the Evidence and determine whether it provides direct proofs, partial insights, or background context relevant to the Claim.
Explain your reasoning in a few sentences, referencing specific elements of the Evidence to justify your evaluation.
Avoid assumptions—focus solely on the content provided.

2. Support Score (0 to 1, increments of 0.1)
0 = Completely Unsupportive: The Evidence has no logical connection to the Claim.
0.1 = Virtually Unsupportive: Only a vague or minimal connection.
0.2 = Very Slightly Supporting: Extremely minimal or tangential support.
0.3 = Slightly Supporting: Addresses a small aspect of the Claim but lacks substantive support.
0.4 = Somewhat Supporting: Provides partial support but is incomplete.
0.5 = Moderately Supporting: Offers some support but limited in scope or strength.
0.6 = Fairly Supporting: Provides relevant support but lacks depth or specificity.
0.7 = Supporting: Clearly supports the Claim, but not comprehensively.
0.8 = Very Supporting: Strongly supports the Claim with significant evidence.
0.9 = Highly Supporting: Almost completely supports the Claim with clear and specific evidence.
1.0 = Perfectly Supporting: Directly and comprehensively supports the Claim with all necessary details.

3. Additional Guidance:
 - Objectivity: Evaluation should be based solely on the content of the Evidence in relation to the Claim.
 - Clarity: Be clear and concise in your justifications. 
 - No assumptions: Do not infer information beyond what's explicitly stated in the texts.
 
Here are the examples:
# Example 1:
{'Claim': 'Topical brimonidine showed an additive IOP-lowering effect to topical PG analogues, although its IOP-lowering effect was inferior to topical timolol as monotherapy.', 
'Evidence': 'When added to PG analogues, the IOP-lowering effect of brimonidine (-2.9 +/- 1.8 mmHg) was greater than that of the placebo (-2.1 +/- 1.8 mmHg) (p = 0.0010).'}
output: {"score": 0.8}

# Example 2:
{'Claim': 'In conclusion, clonidine was not superior to spironolactone in true resistant hypertensive patients, but the overall BP control was low (≈21%).', 
'Evidence': 'Patients with resistant hypertension (no office and ambulatory blood pressure [BP] monitoring control, despite treatment with 3 drugs, including a diuretic, for 12 weeks) were randomized to an additional 12-week treatment with spironolactone (12.5-50 mg QD) or clonidine (0.1-0.3 mg BID). From 1597 patients recruited, 11.7% (187 patients) fulfilled the resistant hypertension criteria.'
output: {"score": 0.4}

# Example 3:
{'Claim': 'In conclusion, clonidine was not superior to spironolactone in true resistant hypertensive patients, but the overall BP control was low (≈21%).', 
'Evidence': 'Compared with the spironolactone group (n=95), the clonidine group (n=92) presented similar rates of achieving the primary end point (20.5% versus 20.8%, respectively; relative risk, 1.01 [0.55-1.88]; P=1.00). Secondary end point analysis showed similar office BP (33.3% versus 29.3%) and ambulatory BP monitoring (44% versus 46.2%) control for spironolactone and clonidine, respectively.'}
output: {"score": 1.0}

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
        extra_body={"enable_thinking": False},
        stream=False,
        timeout=100,
    )
    return response.choices[0].message.content.strip()


logical_mean = []
logical_max = []
logical_min = []
for i in tqdm(Claim_Evidence):
    if i:
        logi = []
        for j in i:
            result = logical_entailment(j)
            pattern = r'Support\s*Score\b[^\d]*(\d+\.\d)'
            score = re.findall(pattern, result, flags=re.DOTALL)
            for x in score:
                x = float(x)
                logi.append(x)
        logical_mean.append(np.mean(logi))
        logical_max.append(np.max(logi))
        logical_min.append(np.min(logi))
    else:
        logical_mean.append(0)
        logical_max.append(0)
        logical_min.append(0)

print(logical_mean)
print(len(logical_mean))
print(logical_max)
print(len(logical_max))
print(logical_min)
print(len(logical_min))
