from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
import time
import json
from bs4 import BeautifulSoup
import os

SBR_WEBDRIVER = '{PATH TO BRIGHT DATA PROXY URL}'


def append_to_json_file(file_path, new_data):
    try:
        with open(file_path, 'r+') as file:
            # Read existing data
            file_data = json.load(file)
            # Append new data
            file_data.extend(new_data)
            # Move the pointer to the beginning of the file
            file.seek(0)
            # Write the updated data
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        # If the file does not exist, create it with the new data
        with open(file_path, 'w') as file:
            json.dump(new_data, file, indent=4)


def get_html_as_json(driver, url):
    driver.get(url)
    time.sleep(1)  # Adjust depending on page load times
    page_source = driver.page_source
    return {"url": url, "html": page_source}


def get_details_from_drive(url, page_source):
    print(url)
    # driver.get(url)
    # time.sleep(1)
    # page_source = driver.page_source
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Scrape the required details
    dict_job = {}
    # Find the job title
    job_title_tag = soup.find('h1', {'class': 'top-card-layout__title'})
    dict_job['job_title'] = job_title_tag.get_text(strip=True) if job_title_tag else 'Not available'
    # dict_job['job_title'] = soup.find('h1', {'class': 'top-card-layout__title'}).get_text(strip=True),
    dict_job['company_name'] = soup.find('a', {'class': 'topcard__org-name-link'}).get_text(strip=True)
    dict_job['location'] = soup.find('span', {'class': 'topcard__flavor--bullet'}).get_text(strip=True)
    # Scrape the workplace type, employment type, and level
    # Find all li elements with the class 'description__job-criteria-item'
    job_criteria_items = soup.find_all('li', {'class':'description__job-criteria-item'})

    # Iterate through each li element and extract the required info
    for item in job_criteria_items:
        subheader = item.find('h3', class_='description__job-criteria-subheader')
        if subheader and subheader.get_text(strip=True).lower() == 'seniority level':
            dict_job['seniority_level'] = item.find('span', class_='description__job-criteria-text description__job-criteria-text--criteria').get_text(strip=True)
        elif subheader and subheader.get_text(strip=True).lower() == 'employment type':
            dict_job['employment_type'] = item.find('span', class_='description__job-criteria-text description__job-criteria-text--criteria').get_text(strip=True)


    # Find the script tag containing the JSON data
    json_data = None
    script_tags = soup.find_all('script', {'type': 'application/ld+json'})
    for script in script_tags:
        try:
            json_data = json.loads(script.string)
            if '@type' in json_data and json_data['@type'] == 'JobPosting':
                break
        except json.JSONDecodeError:
            continue  # Skip if not a valid JSON

    # Extract the required information from the JSON data
    if json_data:
        # Extract education requirements if available
        if 'educationRequirements' in json_data:
            dict_job['education_requirements'] = json_data['educationRequirements']

        # Extract months of experience if available
        if 'experienceRequirements' in json_data and 'monthsOfExperience' in json_data['experienceRequirements']:
            dict_job['months_of_experience'] = json_data['experienceRequirements']['monthsOfExperience']

    dict_job['about'] = soup.find('div', {'class': 'show-more-less-html__markup'}).get_text(strip=True)
    return {"url": url, "dict": dict_job}


def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        current_job_count = 0
        page_number = 0

        while current_job_count < 75:
            driver.get(f'https://www.linkedin.com/jobs/search/?start={page_number * 25}')
            # time.sleep(3)  # Wait for page to load
            elements = driver.find_elements(By.CSS_SELECTOR,
                                            "a.base-card__full-link.absolute.top-0.right-0.bottom-0.left-0.p-0.z-\\[2\\]")[:25]
            # print(len(elements))
            # print(elements)
            # Scrape current page's job postings
            hrefs = [element.get_attribute('href') for element in elements]
            batch_content = []
            for href in hrefs:
                html_data = get_html_as_json(driver, href)
                job_details = get_details_from_drive(html_data['url'], html_data['html'])
                batch_content.append(job_details)
                current_job_count += 1
                if current_job_count >= 75:
                    break

            # Append batch content to JSON file
            append_to_json_file('scraped_data_job_postings_20_03.json', batch_content)

            # Increment page number to move to the next page
            page_number += 1
            print(f'Processed page {page_number}. Total jobs processed: {current_job_count}')

    print('Finished scraping 1000 job postings!')


def original_main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to https://linkedin.com/jobs/search...')
        driver.get('https://linkedin.com/jobs/search')
        elements = driver.find_elements(By.CSS_SELECTOR,
                                        "a.base-card__full-link.absolute.top-0.right-0.bottom-0.left-0.p-0.z-\\[2\\]")[
                   :25]
        hrefs = [element.get_attribute('href') for element in elements]
        print('got hrefs')
        # Scrape each link
        for batch_number in range(0, len(hrefs), 50):
            batch_hrefs = hrefs[batch_number:batch_number + 50]
            scraped_htmls = [get_html_as_json(driver, href) for href in batch_hrefs]
            print(f"Scraped the htmls for batch {batch_number // 50 + 1}")

            file_name = f'scraped_data_job_postings_batch_{batch_number // 50 + 1}.json'
            with open(file_name, 'w') as file:
                scraped_content = [get_details_from_drive(dic['url'], dic['html']) for dic in scraped_htmls]
                json.dump(scraped_content, file, indent=4)

            print(f'Finished batch {batch_number // 50 + 1}! Data saved to {file_name}')

        print('Finished all batches!')
        # scraped_htmls = [get_html_as_json(driver, href) for href in hrefs]
        # print("scraped the htmls for all job postings")
        # # Open or create a JSON file in append mode
        # with open('scraped_data_job_postings_1000.json', 'a') as file:
        #     scraped_content = []
        #     for dic in scraped_htmls:
        #         job_details = get_details_from_drive(dic['url'], dic['html'])
        #         scraped_content.append(job_details)
        #         # Append each job's details to the file
        #         file.write(json.dumps(job_details, indent=4) + ',\n')

    return scraped_content, scraped_htmls


# Call main function and print results
# scraped_content, scraped_htmls = main()
main()
# # Save results to a file
# with open('scraped_data.json', 'w') as file:
#     json.dump(scraped_content, file, indent=4)

# # Save results to a file
# with open('scraped_htmls.json', 'w') as file:
#     json.dump(scraped_htmls, file, indent=4)
# if __name__ == '__main__':
#     main()
