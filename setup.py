from setuptools import setup, find_packages

setup(
    name="gdpr_obfuscator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "boto3>=1.26.0",
        "pandas>=1.5.0",
        "pyarrow>=12.0.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
            "moto>=4.1.0",
        ],
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for GDPR-compliant data obfuscation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="gdpr,aws,data,privacy",
    url="https://github.com/yourusername/gdpr_obfuscator",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)