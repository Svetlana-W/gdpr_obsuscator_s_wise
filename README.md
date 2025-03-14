# GDPR Obfuscator

A Python tool for GDPR-compliant data obfuscation in AWS s3.

## Overview

This tool processes data being ingested to AWS and intercepts personally identifiable information (PII). 
It creates obfuscated copies of files while maintaining their original structure, ensuring GDPR compliance for data analysis.

## Features

- Processes CSV files (MVP)
- Supports JSON and Parquet files (extended functionality)
- Handles files up to 1MB
- AWS s3 integration
- Command-Line Interface (CLI)
- GDPR-compliant data anonymization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Svetlana-W/gdpr_obsuscator_s_wise.git
cd gdpr_obfuscator_s_wise

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`

3. Install the required packages:
```bash
pip install -r requirements.txt

## Usage

# As a Library
from core_obfuscator import GDPRObfuscator

obfuscator = GDPRObfuscator()
config = {
    "file_to_obfuscate": "s3://my-bucket/data.csv",
    "pii_fields": ["name", "email_address"]
}
result = obfuscator.obfuscate(config)

# As a CLI
python src/cli.py config.json --output-bucket my-bucket --output-key output/data.csv


## Testing
```bash
pytest tests


