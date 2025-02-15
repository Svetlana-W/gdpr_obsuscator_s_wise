# Processing SCV, JSON and Parquet files in S3 bucket

import boto3
import pandas as pd
import json
import pyarrow.parquet as pq
from io import BytesIO
import logging
from typing import List, Dict, Union, Tuple, BinaryIO
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Processing s3 files for  CSV, JSON and Parquet formats.
class FileHandler:
    def __init__(self):
        self.s3_client = boto3.client("s3")


    # Processing file from the s3 bucket, obfuscating the PII fields.
    def process(self, file_path: str, pii_fields: List[str]) -> BinaryIO:
        try:
            bucket, key = self._parse_s3_path(file_path)
            file_format = self._get_file_format(key)

            try:
                # Checking the file size.
                response = self.s3_client.head_object(Bucket=bucket, Key=key)
                file_size = response['ContentLength']
                if file_size > 1_048_576:  # = 1MB in bytes
                    raise ValueError("File size (1MB) exceeds limit")

                # Getting and processing file from s3 bucket
                response = self.s3_client.get_object(Bucket=bucket, Key=key)

                if response['ContentLength'] == 0:
                    raise ValueError("File is empty")

                if file_format == "csv":
                    return self.process_csv(response["Body"], pii_fields)
                elif file_format == "json":
                    return self.process_json(response["Body"], pii_fields)
                elif file_format == "parquet":
                    return self.process_parquet(response["Body"], pii_fields)
                else:
                    raise ValueError(f"Unsupported file format: {file_format}")

            # except self.s3_client.exceptions.NoSuchKey:
            #     raise FileNotFoundError(f"File not found: {file_path}")
            except self.s3_client.exceptions.ClientError as e:
                if e.response['Error']['Code'] in ['NoSuchKey', '404']:
                    raise FileNotFoundError(f"File not found: {file_path}")
                raise

        except (ValueError, FileNotFoundError) as e:
            raise  # Re-raising ValueError from parse_s3_path or get_file_format
        except Exception as e:
            raise ValueError(f"Error processing file: {str(e)}")  # Handling any other unexpected errors     


    # Processing CSV file.
    def process_csv(self, file_content: BinaryIO, pii_fields: List[str]) -> BinaryIO:

        df = pd.read_csv(file_content)
        processed_df = self.process_dataframe(df, pii_fields)

        output = BytesIO()
        processed_df.to_csv(output, index=False)
        output.seek(0)
        return output
    
    # Processing JSON file.
    def process_json(self, file_content: BinaryIO, pii_fields: List[str]) -> BinaryIO:

        data = json.loads(file_content.read().decode("utf-8"))

        # Convertin JSON to DataFrame based on structure.
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            raise ValueError("JSON must contain an object or an array of objects")
        
        processed_df = self.process_dataframe(df, pii_fields)

        # Converting back into JSON structure.
        output = BytesIO()
        if isinstance(data, dict):
            json_data = json.loads(processed_df.to_json(orient="records"))[0]
        else:
            json_data = json.loads(processed_df.to_json(orient="records"))

        output.write(json.dumps(json_data, indent=2).encode('utf-8'))
        output.seek(0)
        return output
    
    # Processing Parquet file.
    def process_parquet(self, file_content: BinaryIO, pii_fields: List[str]) -> BinaryIO:

        # Creating a temporary buffer for parquet file.
        temp_buffer = BytesIO(file_content.read())
        df = pq.read_table(temp_buffer).to_pandas()

        processed_df = self.process_dataframe(df, pii_fields)

        # Converting back into Parquet structure.
        output = BytesIO()
        processed_df.to_parquet(output)
        output.seek(0)
        return output
    
    # Processing DataFrame, regardless of source format.
    def process_dataframe(self, df: pd.DataFrame, pii_fields: List[str]) -> pd.DataFrame:

        # Validating PII fields.
        missing_fields = [field for field in pii_fields if field not in df.columns]
        if missing_fields:
            raise ValueError(f"Fields not found: {missing_fields}")
        
        # Obfuscating PII fields.
        for field in pii_fields:
            df[field] = "***"

        return df
    

    # Parsing the s3 path to get bucket and key.
    def _parse_s3_path(self, s3_path: str) -> Tuple[str, str]:

        if not isinstance(s3_path, str):
            raise ValueError("Invalid s3 path: path must be a string")
        
        if not s3_path.startswith("s3://"):
            raise ValueError("Invalid s3 path: path must start with 's3://'")
        
        path = s3_path.replace('s3://', '')
        parts = path.split('/')

        if len(parts) < 2 or not parts[0] or not parts[1:]:
            raise ValueError("Invalid s3 path: must include bucket and key")

        bucket = parts[0]
        key = '/'.join(parts[1:])
        
        return bucket, key
    
    # Determine file format.
    def _get_file_format(self, file_path: str) -> str:

        if file_path.lower().endswith(".csv"):
            return "csv"
        elif file_path.lower().endswith(".json"):
            return "json"
        elif file_path.lower().endswith(".parquet"):
            return "parquet"
        else:
            raise ValueError("Unsupported file format")

