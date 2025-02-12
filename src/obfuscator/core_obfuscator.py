from typing import List, Dict, Union, BinaryIO
from io import BytesIO
from src.obfuscator.s3_handler import FileHandler

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
        


        # self.validate_config(config)
        # file_path - config["file_to_obfuscate"]
        # pii_fields = config["pii_fields"]
        
        # return self.s3_handler.obfuscate(config, file)
