import os
from openai import OpenAI


client = OpenAI(
    api_key="sk-8d638c8f73e5469e839afb6d2c7f787b",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

abstract = [
"The effect of seated exercise on fatigue and quality of life in women with advanced breast cancer.", " To examine the effects of a seated exercise program on fatigue and quality of life (QOL) in women with metastatic breast cancer.", "Randomized, controlled, longitudinal trial.", "Outpatient clinic of a comprehensive cancer center.", "Convenience sample of 38 women who were beginning outpatient chemotherapy.", "Subjects were randomized to a control or intervention group; the intervention was performance of a seated exercise program using home videotape three times per week for four cycles of chemotherapy.", "All subjects completed the Functional Assessment of Chronic Illness Therapy Fatigue Version IV (FACIT F) at baseline and at the time of the next three cycles.", "Subjects were asked to document the frequency, duration, and intensity of all exercise participation on monthly calendars.", "Exercise, fatigue, and QOL.", "32 subjects, 16 per group, completed the study follow-up.", "With a mixed modeling approach, total FACIT F scores for the entire sample declined at a significant rate (p = 0.003) beginning with cycle 3 but at a slower rate for the experimental group (p = 0.02).", "Fatigue scores indicated less increase and physical well-being subscale scores showed less decline for the experimental group (p = 0.008 and p = 0.02, respectively).", "Women with advanced breast cancer randomized to the seated exercise intervention had a slower decline in total and physical well-being and less increase in fatigue scores starting with the third cycle of chemotherapy.", "Seated exercise may be a feasible exercise program for women with advanced cancer for controlling fatigue and improving physical well-being."

]
full_text = ' '.join(abstract)

system_prompt_claim_evidence_extract = """
You are an expert in scientific discourse analysis and natural language processing. 

You will receive a scientific abstract. Your task is to carefully read each sentence in a scientific abstract and classify whether it constitutes a Claim or Evidence, or neither (do not include sentences that fall into neither category in the output).

Instructions:

1. Claim
    Claim is a statement that expresses the main argument, conclusion, or judgment made by the authors (including implications and overall takeaways).

2. Evidence
    Evidence refers to experimental data, numerical results, observations, or any supporting facts used to substantiate a claim.

Here are some examples:
# Example 1:
Abstract: 
    "Treatment of depression in patients with breast cancer: a comparison between paroxetine and amitriptyline. In the context of chronic physical illness, such as breast cancer, depression is associated with increased morbidity, longer periods of hospitalization, and greater overall disability. Prompt diagnosis and effective treatment is, therefore, essential. Several small studies have established the efficacy of tricyclic antidepressants (TCAs) in this setting, and the selective serotonin reuptake inhibitors (SSRIs) would appear to be an alternative therapeutic option because of their established efficacy and better tolerability profile. This was a multicenter. double-blind, parallel-group study in which 179 women with breast cancer were randomized to treatment with either the SSRI paroxetine (20-40 mg/day), or the TCA, amitriptyline (75-150 mg/day). After 8-weeks treatment, depressive symptomatology had improved markedly and to a similar extent in both groups on the Montgomery Asberg Depression Rating Scale. Clinical global impression (CGI) Global improvement and Patient global evaluation scales indicated that patients were minimally to much improved at study endpoint: a change from moderately/mildly ill to borderline ill on the CGI severity of Illness scale. A steady improvement in quality of life was also observed in both groups. There were no clinically significant differences between the groups. In total, 47 (53.4%) patients in the paroxetine group and 53 (59.6%) patients in the amitriptyline group had adverse experiences, the most common of which were the well-recognized side-effects of the antidepressant medications or chemotherapy. Anticholinergic effects were almost twice as frequent in the amitriptyline group (19.1%) compared with paroxetine (11.4%). This study has demonstrated that paroxetine is a suitable alternative to amitriptyline for the treatment of depression in patients with breast cancer."
Claim: 
    "In the context of chronic physical illness, such as breast cancer, depression is associated with increased morbidity, longer periods of hospitalization, and greater overall disability.",
    "Prompt diagnosis and effective treatment is, therefore, essential.",
    "A steady improvement in quality of life was also observed in both groups.",
    "This study has demonstrated that paroxetine is a suitable alternative to amitriptyline for the treatment of depression in patients with breast cancer."
Evidence: 
    "After 8-weeks treatment, depressive symptomatology had improved markedly and to a similar extent in both groups on the Montgomery Asberg Depression Rating Scale.", 
    "Clinical global impression (CGI) Global improvement and Patient global evaluation scales indicated that patients were minimally to much improved at study endpoint: a change from moderately/mildly ill to borderline ill on the CGI severity of Illness scale.", 
    "There were no clinically significant differences between the groups.",
    "In total, 47 (53.4%) patients in the paroxetine group and 53 (59.6%) patients in the amitriptyline group had adverse experiences, the most common of which were the well-recognized side-effects of the antidepressant medications or chemotherapy.",
    "Anticholinergic effects were almost twice as frequent in the amitriptyline group (19.1%) compared with paroxetine (11.4%)."

# Example 2:
Abstract:
    "Sensibility following innervated free TRAM flap for breast reconstruction: Part II. Innervation improves patient-rated quality of life.", " Restoring sensory innervation may be a useful adjunct in free flap head and neck reconstruction but, as yet, has not been shown to improve outcomes of breast reconstruction.", "The authors' previous study demonstrated objectively improved sensation in a group of innervated transverse rectus abdominis musculocutaneous (TRAM) flap breast reconstruction patients relative to noninnervated flaps.", "This study compared patient-rated outcomes of free TRAM breast reconstruction in innervated versus noninnervated flaps.", "Twenty-seven women were randomized prospectively to undergo either innervated or noninnervated free TRAM flap breast reconstruction.", "For innervated flaps, the T10 intercostal nerve was harvested with the TRAM flap and neurotized to the T4 sensory nerve at the recipient site.", "Three validated outcome tools were administered after surgery: the Medical Outcomes Study 36-Item Short Form Health Survey, the Body Image after Breast Cancer Questionnaire, and the Functional Assessment of Cancer Therapy-Breast.", "Results were correlated with previously reported objective sensibility outcomes.", "Eighteen of 27 women returned their questionnaires a mean 48 months after free TRAM flap reconstruction.", "Demographic analysis revealed no significant differences in patient age, height, smoking, radiation therapy, and nipple-areola complex reconstruction between randomized patient groups.", "There was a statistically significant improvement in all three measures in patients who were randomized to receive innervated free TRAM flaps compared with those receiving noninnervated flaps.", "This study demonstrates that innervation of free TRAM flaps used for breast reconstruction not only improves sensibility but also has a positive effect on patient-rated quality of life."
Claim:
    "This study demonstrates that innervation of free TRAM flaps used for breast reconstruction not only improves sensibility but also has a positive effect on patient-rated quality of life."
Evidence:
    "There was a statistically significant improvement in all three measures in patients who were randomized to receive innervated free TRAM flaps compared with those receiving noninnervated flaps."
    "Results were correlated with previously reported objective sensibility outcomes."
    
# Example 3:
Abstract:
    "Effects of a telephone-delivered multiple health behavior change intervention (CanChange) on health and behavioral outcomes in survivors of colorectal cancer: a randomized controlled trial."," Colorectal cancer survivors are at risk for poor health outcomes because of unhealthy lifestyles, but few studies have developed translatable health behavior change interventions.","This study aimed to determine the effects of a telephone-delivered multiple health behavior change intervention (CanChange) on health and behavioral outcomes among colorectal cancer survivors.","In this two-group randomized controlled trial, 410 colorectal cancer survivors were randomly assigned to the health coaching intervention (11 theory-based telephone-delivered health coaching sessions delivered over 6 months focusing on physical activity, weight management, dietary habits, alcohol, and smoking) or usual care.","Assessment of primary (ie, physical activity [Godin Leisure Time Index], health-related quality of life [HRQoL; Short Form-36], and cancer-related fatigue [Functional Assessment of Chronic Illness Therapy Fatigue Scale]) and secondary outcomes (ie, body mass index [kg/m(2)], diet and alcohol intake [Food Frequency Questionnaire], and smoking) were conducted at baseline and 6 and 12 months.","At 12 months, significant intervention effects were observed for moderate physical activity (28.5 minutes; P = .003), body mass index (-0.9 kg/m(2); P = .001), energy from total fat (-7.0%; P = .006), and energy from saturated fat (-2.8%; P = .016).","A significant intervention effect was reported for vegetable intake (0.4 servings per day; P = .001) at 6 months.","No significant group differences were found at 6 or 12 months for HRQoL, cancer-related fatigue, fruit, fiber, or alcohol intake, or smoking.","The CanChange intervention was effective for improving physical activity, dietary habits, and body mass index in colorectal cancer survivors.","The intervention is translatable through existing telephone cancer support and information services in Australia and other countries."
Claim:
    "The CanChange intervention was effective for improving physical activity, dietary habits, and body mass index in colorectal cancer survivors."
Evidence:
    "At 12 months, significant intervention effects were observed for moderate physical activity (28.5 minutes; P = .003), body mass index (-0.9 kg/m(2); P = .001), energy from total fat (-7.0%; P = .006), and energy from saturated fat (-2.8%; P = .016).", 
    "A significant intervention effect was reported for vegetable intake (0.4 servings per day; P = .001) at 6 months.", 
    "No significant group differences were found at 6 or 12 months for HRQoL, cancer-related fatigue, fruit, fiber, or alcohol intake, or smoking."

Now, please carefully consider the following case 
(The number of sentences of claims and sentences of evidence can vary from that in the provided examples),
The number of extracted claims and evidence should be kept to a minimum:
"""

user_prompt = f'/nHere is the scientific abstract:/n"{full_text}"/n'

response = client.chat.completions.create(
    model="qwen3-32b",
    store=True,
    messages=[
        {"role": "system", "content": system_prompt_claim_evidence_extract},
        {"role": "user", "content": user_prompt
         }
    ],
    temperature=0,
    extra_body={"enable_thinking": False},
    stream=False,
    timeout=100,
)

print(response.choices[0].message.content.strip())