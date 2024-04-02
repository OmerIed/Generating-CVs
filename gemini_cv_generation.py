import google.generativeai as genai
import os
from preprocessing_pack import prepare_profile_data, prepare_company_data, prepare_job_data
import pandas as pd
import json
from random import choice
import time
from tqdm import tqdm

df_companies = pd.read_csv('data/companies_100.csv')
PROFILES_PATH = 'data/profiles_small.csv'
df_profiles = pd.read_csv(PROFILES_PATH)
# file_path = 'scraped_data_job_postings_1000.json'
genai.configure(api_key='{our_token}')

model = genai.GenerativeModel('gemini-pro')
# Keep it short and concise.
init_prompt = """Below is information about a company, a job description in that company, a profile, and a CV template for you to fill in.
Your job is to create a resume for the profile, fitting to the company and job.
Do not make up details that are not listed, but you can do infering in order to fill needed sections. 
if an information is missing and you cannot infer it, remove that section, do not write None in a section.
The CV should be final, **do not leave details for filling in**. fill in dates if can be inferred. If you do not know information, delete it.
Your response should contain the resume and nothing else.
The template:
**[Candidate Name. this is the name of the profile, which is a data given below.]**

**Summary**

[Summary about the candidate. Infer from the data given below, do not make up false information.]

**Experience**

**[Current Role]**, [Current Company Name], [Start Date] - [End Date]
* [Description of role]

**[Previous Role]**, [Previous Company Name], [Start Date] - [End Date]
* [Description of role]

**Education**

**[Last Degree]**, [University Name], [Graduation Date]
**[Previous degree. Enter multiple degrees only if there's more than one]**, [University Name], [Graduation Date]

**Skills**

* [First skill. Infer the skills if not given explicitly. write a skill only if you are sure with high probability.]
* [Second skill]
* [Third skill]"""

file_path = 'scraped_data_job_postings_batch_1.json'
with open(file_path, 'r') as file:
    data_jobs = json.load(file)

lst_inputs = []
lst_outputs = []
for _ in tqdm(range(200)):
    # Sample one item from each source
    company_row = df_companies.sample(1).iloc[0]
    profile_row = df_profiles.sample(1).iloc[0]
    job_row = choice(data_jobs)    # company_row = df_companies.iloc[idx]

    company_string = prepare_company_data(company_row)
    # profile_row = df_profiles.iloc[idx]
    profile_string = prepare_profile_data(profile_row)
    # job_row = data_jobs[idx]
    job_string = prepare_job_data(job_row)
    final_prompt = '\n'.join([init_prompt, job_string, company_string, profile_string])
    response = model.generate_content(final_prompt)
    # for candidate in response.candidates:
    #     response_text.append([part.text for part in candidate.content.parts])
    try:
        # Assuming response.text is the correct way to access the generated text
        response_text = response.text

    except AttributeError:
        # Handle the case where 'text' attribute is not present in the response
        print("Error: 'text' attribute not found in the response object")
        continue
    except Exception as e:
        # Handle any other exceptions that may occur
        print(f"An error occurred: {e}")
        continue
    lst_outputs.append(response_text)
    lst_inputs.append(final_prompt)

    # print(response_text)
    time.sleep(0.5)

df_save = pd.DataFrame({'input': lst_inputs, 'output': lst_outputs})
df_save.to_csv('data/cv_extra200.csv', index=False)

