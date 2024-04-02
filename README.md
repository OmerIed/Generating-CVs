# Generating CVs with AI: A Comprehensive Guide

Welcome to the repository for our cutting-edge project, which focuses on scraping LinkedIn job postings and using this data, along with LinkedIn profiles and company information, to create synthetic CVs using Gemini's API. We then train a T5-small model to generate tailored CVs based on these synthetic labels. This project is at the intersection of web scraping, data preprocessing, and advanced machine learning techniques.

## Project Structure

The repository consists of five key files:

- `evaluate_finetuned_t5.ipynb`: This Jupyter notebook takes the T5-small model that we have fine-tuned and generates CVs for each example in the evaluation set. It then assesses the performance using Rouge scores, providing a quantitative measure of the model's effectiveness in CV generation.

- `gemini_cv_generation.py`: A Python script responsible for generating CVs. It amalgamates data from three distinct sources and leverages Gemini's API to produce comprehensive and realistic CVs, serving as the backbone for our synthetic dataset creation.

- `lab_model_training.ipynb`: This notebook contains the code for training the T5-small model. It utilizes HuggingFace's Trainer interface, showcasing the process of model fine-tuning and preparation for the CV generation task.

- `preproccesing_pack`: A collection of utility functions that aid in handling various data types. These functions are crucial for converting raw data into a structured format suitable for our machine learning pipeline.

- `scraping.py`: Utilizes BrightData's platform for scraping job postings from LinkedIn. This script is essential for gathering the real-world data that fuels our project, ensuring a rich and diverse dataset for training and evaluation.

## Getting Started

To get started with this project, clone this repository to your local machine. Ensure you have Python installed and set up the necessary environment, which includes the installation of required libraries and dependencies, such as HuggingFace's Transformers, BrightData's SDK, and others pertinent to data scraping, processing, and model training.

## Usage

1. **Data Collection**: Run `scraping.py` to collect job postings data from LinkedIn.
2. **Data Preprocessing**: Use the `preproccesing_pack` to prepare and structure the collected data for model training.
3. **CV Generation**: Execute `gemini_cv_generation.py` to generate synthetic CVs using Gemini's API.
4. **Model Training**: Train the T5-small model using `lab_model_training.ipynb`.
5. **Evaluation**: Assess the model's performance by running `evaluate_finetuned_t5.ipynb` and review the Rouge scores.

## Contribution

We welcome contributions to this project! If you have suggestions for improvements or want to add new features, feel free to fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

We hope this repository serves as a valuable resource in your AI and machine learning journey, particularly in the realm of automated CV generation. Enjoy exploring and contributing to this innovative project!
