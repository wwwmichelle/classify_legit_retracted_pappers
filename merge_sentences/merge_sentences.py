import json
from tqdm import tqdm
from openai import OpenAI
from format__sentences import data_all

client = OpenAI(
    api_key="sk-8d638c8f73e5469e839afb6d2c7f787b",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def merge_sentences(text):
    prompt = """
You are an expert in scientific discourse analysis and natural language processing. 

You are given sentences classified into two group - "Claim" and "Evidence".

Your task is to merge sentences in the two group respectively, group sentences that express the same Claim or the same Evidence. You need to be precise in merging – only group sentences when they clearly contribute to the same argumentative function. You can choose not to perform any merging.

Here are the examples:
# Example 1:
Evidence:
    "The mean changes were -4.7 +/- 2.1 (S. D.) in the timolol and -4.0 +/- 2.0 mmHg in the brimonidine group (p = 0.0138).",
    "The 95% confidence interval of the inter-group difference was greater than the pre-determined criterion of non-inferiority of brimonidine to timolol.",
    "When added to PG analogues, the IOP-lowering effect of brimonidine (-2.9 +/- 1.8 mmHg) was greater than that of the placebo (-2.1 +/- 1.8 mmHg) (p = 0.0010).",
    "No appreciable adverse side effects were encountered.",
Claim:    
    "Topical brimonidine showed an additive IOP-lowering effect to topical PG analogues, although its IOP-lowering effect was inferior to topical timolol as monotherapy."

output:
{"Evidence": 3, "Claim": 1}
{"Evidence": ["The mean changes were -4.7 +/- 2.1 (S. D.) in the timolol and -4.0 +/- 2.0 mmHg in the brimonidine group (p = 0.0138). The 95% confidence interval of the inter-group difference was greater than the pre-determined criterion of non-inferiority of brimonidine to timolol.",
"When added to PG analogues, the IOP-lowering effect of brimonidine (-2.9 +/- 1.8 mmHg) was greater than that of the placebo (-2.1 +/- 1.8 mmHg) (p = 0.0010).",
"No appreciable adverse side effects were encountered."],
"Claim": ["Topical brimonidine showed an additive IOP-lowering effect to topical PG analogues, although its IOP-lowering effect was inferior to topical timolol as monotherapy."]}

# Example 2:
Evidence:
    "Compared with the spironolactone group (n=95), the clonidine group (n=92) presented similar rates of achieving the primary end point (20.5% versus 20.8%, respectively; relative risk, 1.01 [0.55-1.88]; P=1.00).",
    "Secondary end point analysis showed similar office BP (33.3% versus 29.3%) and ambulatory BP monitoring (44% versus 46.2%) control for spironolactone and clonidine, respectively.",
    "However, spironolactone promoted greater decrease in 24-h systolic and diastolic BP and diastolic daytime ambulatory BP than clonidine.",
    "Per-protocol analysis (limited to patients with \u226580% adherence to spironolactone/clonidine treatment) showed similar results regarding the primary end point.",
Claim:    
    "In conclusion, clonidine was not superior to spironolactone in true resistant hypertensive patients, but the overall BP control was low (\u224821%).",
    "Considering easier posology and greater decrease in secondary end points, spironolactone is preferable for the fourth-drug therapy."

output:
{"Evidence": 3, "Claim": 1}
{"Evidence": ["Compared with the spironolactone group (n=95), the clonidine group (n=92) presented similar rates of achieving the primary end point (20.5% versus 20.8%, respectively; relative risk, 1.01 [0.55-1.88]; P=1.00).",
"Secondary end point analysis showed similar office BP (33.3% versus 29.3%) and ambulatory BP monitoring (44% versus 46.2%) control for spironolactone and clonidine, respectively.",
"However, spironolactone promoted greater decrease in 24-h systolic and diastolic BP and diastolic daytime ambulatory BP than clonidine. Per-protocol analysis (limited to patients with \u226580% adherence to spironolactone/clonidine treatment) showed similar results regarding the primary end point."],
"Claim": [In conclusion, clonidine was not superior to spironolactone in true resistant hypertensive patients, but the overall BP control was low (\u224821%). Considering easier posology and greater decrease in secondary end points, spironolactone is preferable for the fourth-drug therapy.]}
    
# Example 3:
Evidence:
    "At study completion, mean CLAS, FACT-An, FACT-An Anemia subscale, and FACT-An Fatigue subscale scores were significantly higher for patients given epoetin alfa than for those treated with BSC.", 
    "Compared with population norms, both groups had impaired QOL at baseline.", 
    "Differences in mean QOL change scores from baseline to study end for epoetin alfa versus BSC were 3.17 points for the FACT-General Total, 9.90 for the FACT-An Fatigue subscale, and 7.30 for the FACT-An Anemia subscale.", 
    "This was equivalent to corrections in QOL deficits attributable to epoetin alfa of 97.3%, 40.7%, and 38.0% for the FACT-General Total, FACT-An Fatigue, and FACT-An Anemia subscale scores, respectively, versus BSC.", 
    "A somewhat greater QOL benefit was observed for the FACT-An Fatigue and FACT-An Anemia subscales in the subset of patients with baseline Hb levels >10.5 g/dl.", 
Claim:
    "Patients in this study had impaired QOL compared with population norms.", 
    "Early treatment with epoetin alfa to correct anemia improved QOL in a statistically significant and clinically meaningful way, and improvements were greater in patients with baseline Hb levels >10.5 g/dl."

output:
{"Evidence": 3, "Claim": 2}
{"Evidence": ["At study completion, mean CLAS, FACT-An, FACT-An Anemia subscale, and FACT-An Fatigue subscale scores were significantly higher for patients given epoetin alfa than for those treated with BSC. Differences in mean QOL change scores from baseline to study end for epoetin alfa versus BSC were 3.17 points for the FACT-General Total, 9.90 for the FACT-An Fatigue subscale, and 7.30 for the FACT-An Anemia subscale. This was equivalent to corrections in QOL deficits attributable to epoetin alfa of 97.3%, 40.7%, and 38.0% for the FACT-General Total, FACT-An Fatigue, and FACT-An Anemia subscale scores, respectively, versus BSC.",
"Compared with population norms, both groups had impaired QOL at baseline.",
"A somewhat greater QOL benefit was observed for the FACT-An Fatigue and FACT-An Anemia subscales in the subset of patients with baseline Hb levels >10.5 g/dl."],
"Claim": ["Patients in this study had impaired QOL compared with population norms.",
"Early treatment with epoetin alfa to correct anemia improved QOL in a statistically significant and clinically meaningful way, and improvements were greater in patients with baseline Hb levels >10.5 g/dl."]}

Now, please carefully consider the following case 

"""
    user_prompt = f'/nHere is the sentences:/n"{text}"/n'
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


for i in tqdm(data_all):
    result = merge_sentences(i)
    print(result)
    with open("legit/legit_merge_sentence_record.txt", 'a', encoding="utf-8") as f:
        f.write(result)

