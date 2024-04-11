from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="scrapy-aiohttp-downloader",
    version="1.0.0-beta.1",
    author="Jalil SA (jxlil)",
    description="Scrapy download handler that integrates aiohttp",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jxlil/scrapy-aiohttp-downloader",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
)
