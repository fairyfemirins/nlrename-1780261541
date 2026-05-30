from setuptools import setup, find_packages

setup(
    name="nlrename",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "nlrename=nlrename.cli:main",
        ],
    },
)