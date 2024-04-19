# Generating CVs with AI: A Comprehensive Guide

Welcome to the repository for our cutting-edge project, which focuses on scraping LinkedIn job postings and using this data, along with LinkedIn profiles and company information, to create synthetic CVs using Gemini's API. We then train a T5-small model to generate tailored CVs based on these synthetic labels. This project is at the intersection of web scraping, data preprocessing, and advanced machine learning techniques.

## Project Structure

The repository consists of five key files:

- `evaluate_finetuned_t5.ipynb`: This Jupyter notebook takes the T5-small model that we have fine-tuned and generates CVs for each example in the evaluation set. It then assesses the performance using Rouge scores, providing a quantitative measure of the model's effectiveness in CV generation.

- `gemini_cv_generation.py`: A Python script responsible for generating CVs. It amalgamates data from three distinct sources and leverages Gemini's API to produce comprehensive and realistic CVs, serving as the backbone for our synthetic dataset creation.

- `lab_model_training.ipynb`: This notebook contains the code for training the T5-small model. It utilizes HuggingFace's Trainer interface, showcasing the process of model fine-tuning and preparation for the CV generation task.

- `preproccesing_pack.py`: A collection of utility functions that aid in handling various data types. These functions are crucial for converting raw data into a structured format suitable for our machine learning pipeline.

- `scraping.py`: Utilizes BrightData's platform for scraping job postings from LinkedIn. This script is essential for gathering the real-world data that fuels our project, ensuring a rich and diverse dataset for training and evaluation.

- `Data_analysis.ipynb` - Data analysis notebook extracted from DataBricks' platform 


### Data Folder

The `Data` folder contains essential files for the project:

- `TemplateCV.txt`: This file contains the template used by both Gemini and our T5 model for generating CVs, ensuring consistency and realism in the output.

- `scraped_data_job_posting_{number-of-jobs}.json`: These two files contain a total of 100 scraped job postings, providing a rich dataset for training and evaluation.

- `train_cv_data.csv`: The training data for our fine-tuned model, containing the input prompts and Gemini's generated CVs for these prompts, which are used for model training and fine-tuning.

## Getting Started

To get started with this project, clone this repository to your local machine. Ensure you have Python installed and set up the necessary environment, which includes the installation of required libraries and dependencies, such as HuggingFace's Transformers, BrightData's SDK, and others pertinent to data scraping, processing, and model training.

## Usage

1. **Data Collection**: Run `scraping.py` to collect job postings data from LinkedIn.
2. **Data Preprocessing**: Use the `preproccesing_pack.py` to prepare and structure the collected data for model training.
3. **CV Generation**: Execute `gemini_cv_generation.py` to generate synthetic CVs using Gemini's API.
4. **Model Training**: Train the T5-small model using `lab_model_training.ipynb`.
5. **Evaluation**: Assess the model's performance by running `evaluate_finetuned_t5.ipynb` and review the Rouge scores.

---
### A link to our finetuned model weights: **https://drive.google.com/drive/folders/13ivKSJ7NMLzT9iCG-vyltMVLHG4OOLH3?usp=sharing**
We hope this repository serves as a valuable resource in your AI and machine learning journey, particularly in the realm of automated CV generation. Enjoy exploring and contributing to this innovative project!
