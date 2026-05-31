from setuptools import setup, find_packages

setup(
    name="nlrename",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["nlrename"],
    install_requires=[
        "click>=8.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "nlrename=nlrename:cli",
        ],
    },
    author="Femirins",
    description="A CLI tool to rename files using natural language expressions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fairyfemirins/nlrename",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)