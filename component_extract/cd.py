import json
from tqdm import tqdm
from openai import OpenAI

client = OpenAI(
    api_key="sk-8d638c8f73e5469e839afb6d2c7f787b",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def component_extract(text):
    prompt = """
You are an expert in scientific discourse analysis and natural language processing. 

You will receive a scientific abstract. Your task is to carefully read each sentence in a scientific abstract and classify whether it constitutes a Claim or Evidence, or neither (null).Make sure your classification of each sentence takes into account the meaning and role of the sentence within the context of the entire abstract, not in isolation.

Instructions:

1. Claim
    The term Claim refers to the main findings reported in the authors’ original research and usually coincides with the conclusions. 

2. Evidence
    The term Evidence is used for the sentences that refer to particular kinds of arguments, such as those based on observations, factual findings, statistics, experimental tests or other scientific findings.

Here are some examples:

# Example 1:
Abstract: 
    "Effects of a telephone-delivered multiple health behavior change intervention (CanChange) on health and behavioral outcomes in survivors of colorectal cancer: a randomized controlled trial.", " Colorectal cancer survivors are at risk for poor health outcomes because of unhealthy lifestyles, but few studies have developed translatable health behavior change interventions.", "This study aimed to determine the effects of a telephone-delivered multiple health behavior change intervention (CanChange) on health and behavioral outcomes among colorectal cancer survivors.", "In this two-group randomized controlled trial, 410 colorectal cancer survivors were randomly assigned to the health coaching intervention (11 theory-based telephone-delivered health coaching sessions delivered over 6 months focusing on physical activity, weight management, dietary habits, alcohol, and smoking) or usual care.", "Assessment of primary (ie, physical activity [Godin Leisure Time Index], health-related quality of life [HRQoL; Short Form-36], and cancer-related fatigue [Functional Assessment of Chronic Illness Therapy Fatigue Scale]) and secondary outcomes (ie, body mass index [kg/m(2)], diet and alcohol intake [Food Frequency Questionnaire], and smoking) were conducted at baseline and 6 and 12 months.", "At 12 months, significant intervention effects were observed for moderate physical activity (28.5 minutes; P = .003), body mass index (-0.9 kg/m(2); P = .001), energy from total fat (-7.0%; P = .006), and energy from saturated fat (-2.8%; P = .016).", "A significant intervention effect was reported for vegetable intake (0.4 servings per day; P = .001) at 6 months.", "No significant group differences were found at 6 or 12 months for HRQoL, cancer-related fatigue, fruit, fiber, or alcohol intake, or smoking.", "The CanChange intervention was effective for improving physical activity, dietary habits, and body mass index in colorectal cancer survivors.", "The intervention is translatable through existing telephone cancer support and information services in Australia and other countries."     
output: [null, null, null, null, null, "Evidence", "Evidence", "Evidence", "Claim", null]

# Example 2:
Abstract:
    "Sensibility following innervated free TRAM flap for breast reconstruction: Part II. Innervation improves patient-rated quality of life.", " Restoring sensory innervation may be a useful adjunct in free flap head and neck reconstruction but, as yet, has not been shown to improve outcomes of breast reconstruction.", "The authors' previous study demonstrated objectively improved sensation in a group of innervated transverse rectus abdominis musculocutaneous (TRAM) flap breast reconstruction patients relative to noninnervated flaps.", "This study compared patient-rated outcomes of free TRAM breast reconstruction in innervated versus noninnervated flaps.", "Twenty-seven women were randomized prospectively to undergo either innervated or noninnervated free TRAM flap breast reconstruction.", "For innervated flaps, the T10 intercostal nerve was harvested with the TRAM flap and neurotized to the T4 sensory nerve at the recipient site.", "Three validated outcome tools were administered after surgery: the Medical Outcomes Study 36-Item Short Form Health Survey, the Body Image after Breast Cancer Questionnaire, and the Functional Assessment of Cancer Therapy-Breast.", "Results were correlated with previously reported objective sensibility outcomes.", "Eighteen of 27 women returned their questionnaires a mean 48 months after free TRAM flap reconstruction.", "Demographic analysis revealed no significant differences in patient age, height, smoking, radiation therapy, and nipple-areola complex reconstruction between randomized patient groups.", "There was a statistically significant improvement in all three measures in patients who were randomized to receive innervated free TRAM flaps compared with those receiving noninnervated flaps.", "This study demonstrates that innervation of free TRAM flaps used for breast reconstruction not only improves sensibility but also has a positive effect on patient-rated quality of life."
output: [null, null, null, null, null, null, null, "Evidence", null, null, "Evidence", "Claim"]

# Example 3:
Abstract:
    "Randomised phase II trial of 4 dose levels of single agent docetaxel in performance status (PS) 2 patients with advanced non-small cell lung cancer (NSCLC): DOC PS2 trial. Manchester lung cancer group.", " The role of chemotherapy for advanced NSCLC patients and ECOG PS2 remains controversial.", "We evaluated 4 doses of 3-weekly docetaxel to identify a less toxic, clinically effective dose.", "Seventy-three patients with stage III (22%) (unsuitable for radical surgery/radiotherapy) and IV (78%) NSCLC were randomized to receive 4 doses of 3-weekly docetaxel, for 4 cycles: arm (A) 40 mg/m(2) (n=17), arm (B) 50 mg/m(2) (n=17), arm (C) 60 mg/m(2) (n=19), arm (D) 50 mg/m(2) escalated by 10 mg/m(2) to a maximum of 70 mg/m(2) (n=19).", "Primary endpoints: maximum tolerated dose, RR, duration of response, symptom improvement, toxicity and QoL.", "Secondary endpoint: overall survival (OS).", "Patients and disease characteristics were well balanced.", "Median age was 67 (range 45-81), there were 32 male and 41 female, histology subtype: squamous/adenocarcinoma/mixed/NOS=42%/49%/4%/5%.", "Seven patients did not receive any treatment because of deterioration in PS or death.", "50% of patients in arm D, who received more than one cycle, received dose escalation.", "There was no statistical difference in the number of cycles administered (arms A, B and D: median 2 cycles and arm C: median 3 cycles) and no difference in RR: arm A=6%, arm B=6%, arm C=10%, and arm D=0%.", "There was no statistically significant difference in grade 3/4 neutropenia and thrombocytopenia between the four arms.", "No difference was observed in hospitalization rate, blood transfusions, antibiotics administration and non-haematological toxicity.", "QoL: no difference in total scores between baseline and cycles 1-4.", "There was a significant decrease in pain scores from baseline to post cycles 2 and 3 (p=0.025 and p=0.002, respectively).", "There was no difference in OS (p=0.992).", "Median survival and 6-month survival were 61, 86, 88 and 97 days and 29%, 33%, 21% and 26% for arms A, B, C, and D, respectively.", "Clinical efficacy of docetaxel was observed at all dose levels.", "Higher dose levels were not associated with increased toxicities, use of IV antibiotics or hospitalization rates.", "However, the median survival observed is shorter than historical data and do not support further evaluation of these doses of single agent docetaxel in this population."
output: [null, null, null, null, null, null, null, null, null, null, "Evidence", "Evidence", "Evidence", null, "Evidence", "Evidence", "Evidence", "Claim", "Claim", "Evidence"]

Now, please carefully consider the following case and return the labels
(The number of sentences of claims and sentences of evidence can vary from that in the provided examples),
The number of extracted claims and evidence should be kept to a minimum:
"""
    user_prompt = f'/nHere is the scientific abstract:/n"{text}"/n'
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

text = [
      "As one of the most important organs of human beings, the eyes can receive external visual information and play an important role in perception.",
      "Therefore, the method of maintaining eye health is a problem that people pay attention to.",
      "Omental disease is one of the most serious microvascular complications in diabetic patients, and it is also the main cause of blindness in patients.",
      "The purpose of this article is to investigate the main factors that influence the prevalence of retinopathy in diabetic patients based on medical big data.",
      "In this article, a method for investigating the causes of the incidence of retinopathy in diabetic patients based on medical big data is proposed, and a questionnaire survey method and other methods are used for experimental investigation.",
      "Combining the data in the figure in the experiment in this article, it can be seen that among diabetic patients, the prevalence of diabetes in men is 12.4%, and the prevalence of diabetes in women is 8.4%.",
      "From the data in the figure, it can be known that the rate of retinopathy caused by various factors is between 5% and 7%, and the total prevalence of retinopathy is 47.5%.",
      "There are many factors affecting the prevalence of retinopathy in diabetic patients, such as the duration of diabetes, urinary albumin index, glycosylated hemoglobin index, and fasting blood glucose level; various factors lead to an increase in the prevalence of retinopathy in diabetic patients.",
      "The results show that there are many factors affecting the prevalence of retinopathy in diabetic patients, so patients should pay attention to exercise, control their diet, and prevent retinopathy."
    ]
result = component_extract(text)
print(result)

