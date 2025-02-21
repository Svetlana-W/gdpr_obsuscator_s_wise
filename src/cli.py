"""
Command Line Interface (CLI) for GDPR Obfuscator.
"""
import click
import json
import boto3
from core_obfuscator import GDPRObfuscator

@click.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--output-bucket', required=True, help='S3 bucket for output')
@click.option('--output-key', required=True, help='S3 key for output file')
def main(config_file: str, output_bucket: str, output_key: str):
    # Processing file according to configuration and saving it to s3.
    try:
        # Reading config
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Processing file
        obfuscator = GDPRObfuscator()
        output_stream = obfuscator.obfuscate(config)
        
        # Saving to s3
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=output_stream
        )
        
        click.echo(f"File processed and saved to s3://{output_bucket}/{output_key}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()
