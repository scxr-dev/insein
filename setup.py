"""
[ INSEIN INSTALLER CONFIGURATION ]
AUTHOR: R H A Ashan Imalka (scxr-dev)
"""

from setuptools import setup, find_packages

setup(
    name="insein",
    version="1.0.0",
    description="The Shapeshifting Network Scanner with Kernel Injection",
    long_description=open("AUTHOR.md").read(),
    long_description_content_type="text/markdown",
    author="R H A Ashan Imalka (scxr-dev)",
    author_email="itrandar@gmail.com", 
    url="https://github.com/scxr-dev/insein", 
    packages=find_packages(),
    py_modules=["insein"], 
    install_requires=[
        "rich",
        "aiohttp",
        "scapy"
    ],
    entry_points={
        'console_scripts': [
            'insein=insein:run', 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
    ],
    python_requires='>=3.6',
)