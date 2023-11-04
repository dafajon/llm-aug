from setuptools import setup, find_packages

# Package information
PACKAGE_NAME = "llm-aug"
VERSION = "1.0.0"
DESCRIPTION = "A Python package for performing data annotation and augmentation in natural language processing tasks by harnessing the power of LLMs"
URL = "https://github.com/yourusername/llm-aug"
AUTHOR = "Dorukhan Afacan"
AUTHOR_EMAIL = "dorukhan.afacan@gmail.com"

# Required dependencies with versions
INSTALL_REQUIRES = [
    "openai>=0.27.6",
    "tiktoken>=0.4.0",
    "boto3>=1.18.3",
    # Add any other required dependencies here
]

# Optional dependencies
EXTRAS_REQUIRE = {
    # Add any extra dependencies for optional features here
}

# Package classifiers
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Topic :: Text Processing :: Linguistic :: LLM",
]

# Read the long description from a README file
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=CLASSIFIERS,
)
