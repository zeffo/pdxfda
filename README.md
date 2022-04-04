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



