# GDPR Obfuscator

A Python tool for GDPR-compliant data obfuscation in AWS s3.

## Overview

This tool automates the anonymisation of sensitive data, personally identifiable information (PII), stored in AWS s3. It creates obfuscated copies of files while maintaining their original structure, ensuring GDPR compliance and enabling secure data analysis. It supports CSV, JSON, and Parquet files.

## Target Audience

Data engineers, analysts, and product owners working with sensitive data in AWS s3.

## Features

*   Obfuscates PII in CSV, JSON, and Parquet files.
*   Handles files up to 1MB (configurable).
*   Seamless integration with AWS s3.
*   Command-line interface (CLI) for easy automation and integration with other tools.
*   Python library for programmatic usage.


## Getting Started

### Prerequisites
- Python 3.8+
- AWS credentials configured (see [AWS Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html))
- AWS CLI installed (optional, for interacting with s3 directly)


### Installation

1. Clone the repository:
```bash
git clone https://github.com/Svetlana-W/gdpr_obsuscator_s_wise.git
cd gdpr_obfuscator_s_wise
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
```

3. Install the required packages:
```bash
make install
```

### Usage

## As a Python Library
```python
from core_obfuscator import GDPRObfuscator

obfuscator = GDPRObfuscator()
config = {
    "file_to_obfuscate": "s3://my-bucket/data.csv",
    "pii_fields": ["name", "email_address"]
    }
result = obfuscator.obfuscate(config) #  'result' is a BytesIO object; upload it to s3 or process as needed.
```

## As a CLI
```bash
python src/cli.py config.json --output-bucket my-bucket --output-key output/data.csv
```

* `config.json`: path to your configuration file 
* `my-bucket`: your s3 bucket name 
* `--output-bucket`: the s3 bucket to store the anonimised file
* `--output-key`: path/key for the anonimised file within the s3 bucket

#### Example `config.json` (Replace placeholders with your actual s3 URI and PII fields):
``` json
{
  "file_to_obfuscate": "s3://your-input-bucket/path/to/input.csv",
  "pii_fields": ["name", "email_address"]
}
```


### Testing
```bash
make test
```
This runs the test suit using `pytest`. Tests use `moto` to mock AWS services, so real AWS credentials for are not needed for testing.


### MakeFile Usage

* `make install`: Installs the project dependencies.
* `make test`: Runs the test suite.
* `make run` : Runs the application using CLI (requires a config.json file – see example above). 
Important: Before running `make run`, replace placeholder values in the `run` command in the Makefile with your actual configuration and AWS credentials (bucket and file paths).
* `make clean`: Removes the temporary files and build artifacts.


### Project Structure

```tree
gdpr_obfuscator/
├── src/                 # Source code
│   ├── gdpr_obfuscator/  # Python package directory 
│   │   ├── __init__.py   # Makes gdpr_obfuscator a package
│   │   ├── cli.py        # Entry point for the Command-Line Interface (CLI)
│   │   ├── core_obfuscator.py  # Core obfuscation logic
│   │   └── s3_handler.py       # Handles s3 interactions
├── tests/               # Test files
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration
│   ├── test_core_obfuscator.py     # Tests for core obfuscation logic
│   └── test_s3_handler.py          # Tests for s3_handler.py
├── requirements.txt # Project dependencies
├── setup.py         # Project setup for installation
├── Makefile         # Makefile for simplified commands
├── README.md        # This file is the README
└── config.json      # Example configuration file (Replace with your values)
```




