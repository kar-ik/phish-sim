from setuptools import setup, find_packages

setup(
    name="phish-sim-tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "pdfplumber",
        "cryptography",
        "sendgrid",  
    ],
    entry_points={
        "console_scripts": [
            "phish-sim=phish_sim.cli:cli",
        ],
    },
    author="Your Name",
    description="Consent-first phishing simulation CLI",
)
