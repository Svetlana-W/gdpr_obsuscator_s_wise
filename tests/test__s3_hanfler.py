"""
<<<<<<< HEAD
Tests for s3 file handler functionality.
=======
Tests for S3 file handler functionality.
>>>>>>> 5648f1c (Updated primary setup for tests.)
"""
import pytest
import pandas as pd
import json
import pyarrow.parquet as pq
from io import BytesIO
from botocore.exceptions import ClientError
from src.obfuscator.s3_handler import FileHandler

@pytest.fixture
def handler():
    return FileHandler()

@pytest.fixture
def mock_csv_content():
    df = pd.DataFrame({
        'id': [1, 2],
        'name': ['John Doe', 'Jane Smith'],
        'email': ['john@example.com', 'jane@example.com'],
        'age': [30, 25]
    })
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

@pytest.fixture
def mock_json_content():
    data = {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    }
    buffer = BytesIO()
    buffer.write(json.dumps(data).encode('utf-8'))
    buffer.seek(0)
    return buffer

class TestFileHandler:
    def test_parse_s3_path_valid(self, handler):
        bucket, key = handler._parse_s3_path("s3://my-bucket/path/to/file.csv")
        assert bucket == "my-bucket"
        assert key == "path/to/file.csv"

    @pytest.mark.parametrize("invalid_path", [
        None,
        123,
        "not-an-s3-path",
        "s3://",
        "s3://bucket",
    ])
    def test_parse_s3_path_invalid(self, handler, invalid_path):
        with pytest.raises(ValueError):
            handler._parse_s3_path(invalid_path)

    @pytest.mark.parametrize("file_path,expected_format", [
        ("file.csv", "csv"),
        ("file.JSON", "json"),
        ("file.parquet", "parquet"),
    ])
    def test_get_file_format_valid(self, handler, file_path, expected_format):
        assert handler._get_file_format(file_path) == expected_format

    def test_get_file_format_invalid(self, handler):
        with pytest.raises(ValueError, match="Unsupported file format"):
            handler._get_file_format("file.txt")

    def test_process_csv(self, handler, mock_csv_content, mocker):
        # Mock S3 client
        mocker.patch.object(
            handler.s3_client,
            'head_object',
            return_value={'ContentLength': 100}
        )
        mocker.patch.object(
            handler.s3_client,
            'get_object',
            return_value={'Body': mock_csv_content, 'ContentLength': 100}
        )

        result = handler.process(
            "s3://test-bucket/test.csv",
            ["name", "email"]
        )
        
        # Read result back into DataFrame
        df = pd.read_csv(BytesIO(result.getvalue()))
        
        assert all(df['name'] == '***')
        assert all(df['email'] == '***')
        assert df['age'].tolist() == [30, 25]

    def test_process_json(self, handler, mock_json_content, mocker):
        # Mock S3 client
        mocker.patch.object(
            handler.s3_client,
            'head_object',
            return_value={'ContentLength': 100}
        )
        mocker.patch.object(
            handler.s3_client,
            'get_object',
            return_value={'Body': mock_json_content, 'ContentLength': 100}
        )

        result = handler.process(
            "s3://test-bucket/test.json",
            ["name", "email"]
        )
        
        # Parse result
        data = json.loads(result.getvalue())
        
        assert data['name'] == '***'
        assert data['email'] == '***'
        assert data['age'] == 30

    def test_file_size_limit(self, handler, mocker):
        # Mock file larger than 1MB
        mocker.patch.object(
            handler.s3_client,
            'head_object',
            return_value={'ContentLength': 2_000_000}
        )

        with pytest.raises(ValueError, match="File size .* exceeds limit"):
            handler.process(
                "s3://test-bucket/test.csv",
                ["name"]
            )

    def test_file_not_found(self, handler, mocker):
        # Mock S3 client to raise NoSuchKey
        mocker.patch.object(
            handler.s3_client,
            'head_object',
            side_effect=ClientError(
                {'Error': {'Code': 'NoSuchKey', 'Message': 'Not found'}},
                'HeadObject'
            )
        )

        with pytest.raises(FileNotFoundError):
            handler.process(
                "s3://test-bucket/missing.csv",
                ["name"]
            )

    def test_empty_file(self, handler, mocker):
        # Mock empty file
        mocker.patch.object(
            handler.s3_client,
            'head_object',
            return_value={'ContentLength': 0}
        )
        mocker.patch.object(
            handler.s3_client,
            'get_object',
            return_value={'Body': BytesIO(), 'ContentLength': 0}
        )

        with pytest.raises(ValueError, match="File is empty"):
            handler.process(
                "s3://test-bucket/empty.csv",
                ["name"]
            )

    def test_missing_fields(self, handler, mock_csv_content, mocker):
        mocker.patch.object(
            handler.s3_client,
            'head_object',
            return_value={'ContentLength': 100}
        )
        mocker.patch.object(
            handler.s3_client,
            'get_object',
            return_value={'Body': mock_csv_content, 'ContentLength': 100}
        )

        with pytest.raises(ValueError, match="Fields not found"):
            handler.process(
                "s3://test-bucket/test.csv",
                ["non_existent_field"]
            )