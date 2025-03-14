from typing import List, Dict, Union, BinaryIO
from s3_handler import FileHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
Initialise the GDPRObfuscator class: 
the main class for handling PII data obfuscation in files, stored in s3 bucket.
"""


class GDPRObfuscator:
    def __init__(self):
        self.s3_handler = FileHandler()

    # Validating the configuration dictionary
    def _validate_config(self, config: Dict[str, Union[str, List[str]]]) -> None:

        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")

        required_keys = {"file_to_obfuscate", "pii_fields"}
        missing_keys = required_keys - set(config.keys())
        if missing_keys:
            raise ValueError(f"Missing required keys: {missing_keys}")

        if not isinstance(config["file_to_obfuscate"], str):
            raise ValueError("file_to_obfuscate must be a string")

        if not isinstance(config["pii_fields"], list):
            raise ValueError("pii_fields must be a list")

        if not config["pii_fields"]:
            raise ValueError("pii_fields cannot be empty")

    """
    Obfuscating the PII fields in the cpecified file.
    Args: config(dict): file_to_obfuscate (s3 path to input file), pii_fields (list of PII fields to obfuscate).
    Returns: BinaryIO (byte stream of the obfuscated data).
    Raises: ValueError (if configuration is invaklid), FileNotFoundError (if s3 file does not exist).
    """

    def obfuscate(self, config: Dict[str, Union[str, List[str]]]) -> BinaryIO:

        self._validate_config(config)
        return self.s3_handler.process(
            config["file_to_obfuscate"], config["pii_fields"]
        )
