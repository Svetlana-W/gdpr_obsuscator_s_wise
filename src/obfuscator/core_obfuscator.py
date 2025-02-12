from typing import List, Dict, Union, BinaryIO
from io import BytesIO
from src.obfuscator.s3_handler import FileHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
Initialise the GDPRObfuscator class, the main class for handling PII data obfuscation in files, stored in s3 bucket.
"""

class GDPRObfuscator:
    def __init__(self):
        self.s3_handler = FileHandler()

    def obfuscate(self, config: Dict[str, Union[str, List[str]]]) -> BinaryIO:
        """
        Obfuscate the PII fields in the cpecified file.
        Args: config(dict): file_to_obfuscate (s3 path to input file), pii_fields (list of PII fields to obfuscate).
        Returns: BinaryIO (byte stream of the obfuscated data).
        Raises: ValueError (if configuration is invaklid), FileNotFoundError (if s3 file does not exist).
        """
        
        if not isinstance(config, dict):
            raise ValueError("Invalid configuration: config must be a dictionary")
        
        if "file_to_obfuscate" not in config:
            raise ValueError("Invalid configuration: file_to_obfuscate is required")
        
        if "pii_fields" not in config:
            raise ValueError("Invalid configuration: pii_fields is required")
        
        if not isinstance(config["pii_fields"], list):
            raise ValueError("Invalid configuration: pii_fields must be a list")
        
        return self.s3_handler.process(config["file_to_obfuscate"], config["pii_fields"])
        
