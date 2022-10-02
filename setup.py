
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aurora",
    version="0.0.1",
    author="sj",
    author_email="songjian@codeorder.cn",
    description="用Python写的管理极光VPN的软件。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/songjian/aurora",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests==2.28.1',
        'pandas==1.5.0',
        'psutil==5.9.2'
    ],
    python_requires='>=3'
)