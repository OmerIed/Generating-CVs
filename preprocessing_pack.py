import pandas as pd
import os
import json
from transformers import GPT2Tokenizer


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
def trim_to_k_tokens(text, K=150):

    tokens = tokenizer.encode(text, add_special_tokens=False)

    # Trim to the first K tokens if necessary
    if len(tokens) > K:
        tokens = tokens[:K]

    # Convert the tokens back to a string
    trimmed_text = tokenizer.decode(tokens)
    return trimmed_text


parameters = {'max_tokens_to_generate': 400,
              'max_about_tokens_length': 150}

JOB_EXAMPLE_JSON = {
    "url": "https://www.linkedin.com/jobs/view/guest-relations-specialist-theme-park-remote-at-navigate-new-horizons-3854109813?position=7&pageNum=0&refId=dAybijAqwWI0ZNSt6bmGnA%3D%3D&trackingId=5T7onI8k8zBFvG2cUG%2FMng%3D%3D&trk=public_jobs_jserp-result_search-card",
    "dict": {
        "job_title": "Guest Relations Specialist-Theme Park (Remote)",
        "company_name": "Navigate New Horizons",
        "location": "United States",
        "seniority_level": "Entry level",
        "employment_type": "Full-time",
        "about": "Summary: The Guest Relations Specialist plays a vital role in managing reservations and bookings for theme parks, ensuring guests have a seamless and enjoyable experience from start to finish. Below are the main duties and qualifications for this position:Main Responsibilities:Booking Management: Oversee the booking process for individuals, families, and groups to ensure efficiency. Assist guests in choosing suitable ticket packages and accommodations based on their preferences. Monitor and optimize reservation systems to maximize park capacity.Guest Interaction: Deliver outstanding customer service by addressing inquiries, fulfilling special requests, and resolving booking-related issues promptly. Educate guests about park policies, pricing, and ongoing promotions. Foster a welcoming and hospitable environment for all park visitors.Record-Keeping: Maintain precise records of reservations, ticket sales, and guest details. Generate reports to analyze booking patterns and support data-driven decision-making. Ensure online booking platforms remain current and user-friendly.Revenue Maximization: Identify opportunities for upselling, such as meal plans, fast passes, or premium experiences. Collaborate with marketing and sales teams to devise strategies for boosting bookings and revenue.Issue Resolution: Effectively handle booking-related concerns, including modifications, cancellations, and refunds. Address guest complaints and escalate complex issues as necessary.Compliance and Safety: Ensure adherence to health and safety regulations, particularly in challenging circumstances like pandemics. Stay abreast of park policies and procedures, and communicate them clearly to guests.Qualifications:High school diploma or equivalent; while a degree in hospitality or business is advantageous, it's not mandatory. Previous experience in customer service, preferably within hospitality, travel, or entertainment sectors, is a bonus but not obligatory. Excellent communication and interpersonal skills. Strong attention to detail and organizational prowess. Ability to thrive in a dynamic, fast-paced setting. Knowledge of theme park attractions is beneficial but not essential.As a Theme Park Specialist, you'll play a crucial role in shaping guests' experiences, ensuring their satisfaction, and contributing to the park's overall success. Your adeptness in managing reservations, delivering exceptional customer service, and assisting guests in maximizing their visit will be pivotal in upholding the park's reputation and driving its prosperity.Benefits:Flexible Schedule Travel Perks Commission-based Licensed & Bonded Personal Website E&O Insurance with Fraud Protection Daily Training Available Travel Agent Certification Remote Business Opportunity Full Training Provided Work FT or PT No experience necessaryRequirements:A dedicated home workspace, including: Computer Cell phone High-speed internet Minimal distractions Must be 18+ Must be authorized to work in the USA, AustraliaPowered by JazzHRYyEDI0QMC6"
    }
}

def prepare_job_data(job_data):
    job_dict = job_data['dict']
    job_dict['about'] = trim_to_k_tokens(job_dict['about'])
    job_string_array = [k + ': ' + v for k, v in job_dict.items() if isinstance(v,str)]
    job_string = '\n'.join(job_string_array)
    final_string = 'This is the information about the job posting: \n' + job_string
    return final_string


def prepare_company_data(company_data):
    company_dict = company_data.to_dict()

    company_dict['about'] = trim_to_k_tokens(company_dict['about'])

    company_string_array = [k + ': ' + str(v) for k, v in company_dict.items()]
    company_string = '\n'.join(company_string_array)
    final_string = 'This is the information about the company: \n' + company_string
    return final_string


def prepare_profile_data(profile_data):
    profile_data = profile_data.to_dict()

    profile_data['about'] = trim_to_k_tokens(profile_data['about'])
    profile_data['experience'] = trim_to_k_tokens(profile_data['experience'])
    profile_string_array = [k + ': ' + str(v) for k, v in profile_data.items()]
    profile_string = '\n'.join(profile_string_array)
    final_string = 'This is the information about the profile: \n' + profile_string
    return final_string



