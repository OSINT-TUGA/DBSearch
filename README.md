
# DBSearch
**DBSearch - Data Breach / Database Search Tool:** A Python script for querying and viewing data from SQLite databases, tailored for Data Breach analysis.

## Introduction
Have you ever faced the challenge of managing a super mega hyper gigantic Data Base / Data Breach file and finding it impossible to search or even open it? If so, this script is for you! It simplifies and speeds up the search process within SQLite databases, turning cumbersome data handling into a breeze.

## Disclaimer
*This tool is specifically designed for security researchers. If you wish to check whether your data has been compromised, please consult other resources such as the renowned site [Have I Been Pwned](https://haveibeenpwned.com/).*

*This repository and its linked locations do not contain any databases or personal data. Any requests for sharing such information will be ignored. The contributors to this repository are not responsible for providing any personal or database-related data The example database included in the code was created by ChatGPT and contains only random data.*

## Features
- **Multi-Database Support**: Supports multiple databases with distinct settings configured in the config file.
- **Command Line Interface:** Simple, effective, and only requires Python 3.
- **List and Detail Configuration:** Define search fields and the fields to be displayed in the listing. In the detailed view, all fields are shown.
- **Sample Database Included:** Comes with an example database for testing purposes.

## TO-DO
- **Expand Database Compatibility:** Add support for additional database types beyond SQLite.
- **Implement Export Functionality:** Enable exporting search results to a CSV file for easier data analysis and sharing.

## Installation
- **With wget:**
    `wget https://github.com/OSINT-TUGA/DBSearch/archive/refs/heads/main.zip && unzip main.zip`

- **With git:**
    `git clone --depth 1 https://github.com/OSINT-TUGA/DBSearch.git`

- **Install requirements:**

    'pip3 install -r requirements'

## Usage

- **Execute the script:**

    `python3 DBSearch.py`

## Changelog
For a detailed account of changes made to the script, refer to CHANGELOG.md in this repository.


## License
This project is licensed under the Attribution 4.0 International (CC BY 4.0). You are free to use and modify the script as you see fit, as long as you provide attribution to the original author.
