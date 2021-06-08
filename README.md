WORKFLOW AUTOMATION

# How it works
The program makes a request to the API with the given timeframe. It collects the data of each drug from the response, ignoring the previously rejected ones. It then stores this data in a MongoDB Collection. Then, the text from the label of each drug is extracted, and a list of cancer-related keywords is referenced. If a word from the list is found in the text, the drug is `flagged`. If the drug, does not have a label, the label field is filled with `missing`. The timestamp of when the drug was recorded is also present in the database.

When the API response has been fully parsed, the program will fetch the data of all drugs recorded within the given timeframe, and lay it out into google spreadsheets:
1. A list of all cancer-related drugs. 
2. A list of all drugs who have a label. 
3. A list of all drugs without a label.
4. A list of all drugs which were present in the database before the given timeframe, and whose data has been updated. 

A thorough log file is created after each program is run.

# Usage

Run `main.py`.
All settings can be configured in the UI.

Requirements can be found at `requirements.txt`.

**Please raise an issue in this repository if you encounter a problem.**

# Performance

I have tried multiple mechanisms to improve performance, namely asyncio, threading and multiprocessing. The code is I/O bound for making HTTP requests, however it is CPU-intensive when extracting text from the PDFs. In my testing, I have found multiprocessing via the concurrent.futures package to be the fastest, but also the most resource intensive due to the usage of multiple cores. As a result, I have decided to give the user an option to use a very fast and resource intensive script, or a slower but single-threaded script to ensure that the script can run on most hardware.

# Contributing

Please use the [Black](https://black.readthedocs.io/en/stable/) code formatter to format your code. 
The Python Discord's [style guide](https://pythondiscord.com/pages/guides/pydis-guides/contributing/style-guide/) should be adhered to as much as possible.

