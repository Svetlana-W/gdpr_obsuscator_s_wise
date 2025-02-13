"""
Tests for core GDPR obfuscator functionality.
"""
import pytest
from io import BytesIO
from src.obfuscator.core_obfuscator import GDPRObfuscator

@pytest.fixture
def obfuscator():
    return GDPRObfuscator()

@pytest.fixture
def valid_config():
    return {
        "file_to_obfuscate": "s3://test-bucket/test.csv",
        "pii_fields": ["name", "email"]
    }

class TestGDPRObfuscator:
    def test_valid_config(self, obfuscator, valid_config, mocker):
        # Mock S3 handler
        mock_process = mocker.patch.object(
            obfuscator.s3_handler, 
            'process',
            return_value=BytesIO()
        )
        
        obfuscator.obfuscate(valid_config)
        mock_process.assert_called_once_with(
            valid_config["file_to_obfuscate"],
            valid_config["pii_fields"]
        )

    @pytest.mark.parametrize("invalid_config,error_msg", [
        (
            None,
            "Config must be a dictionary"
        ),
        (
            {},
            "Missing required keys: {'file_to_obfuscate', 'pii_fields'}"
        ),
        (
            {"file_to_obfuscate": "s3://bucket/file.csv"},
            "Missing required keys: {'pii_fields'}"
        ),
        (
            {"pii_fields": ["name"]},
            "Missing required keys: {'file_to_obfuscate'}"
        ),
        (
            {
                "file_to_obfuscate": "s3://bucket/file.csv",
                "pii_fields": "name"
            },
            "pii_fields must be a list"
        ),
        (
            {
                "file_to_obfuscate": "s3://bucket/file.csv",
                "pii_fields": []
            },
            "pii_fields cannot be empty"
        ),
        (
            {
                "file_to_obfuscate": 123,
                "pii_fields": ["name"]
            },
            "file_to_obfuscate must be a string"
        ),
    ])
    def test_invalid_configs(self, obfuscator, invalid_config, error_msg):
        with pytest.raises(ValueError, match=error_msg):
            obfuscator.obfuscate(invalid_config)