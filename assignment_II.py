import argparse
import urllib.request
import logging
import datetime
import sys

url = "https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv"

def downloadData(url):
    """Downloads the content from the given URL and returns it as a string."""
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

def processData(file_content):
    """Processes the CSV data and returns a dictionary mapping IDs to (name, birthday)."""
    data_dict = {}
    lines = file_content.splitlines()
    
    logger = logging.getLogger('assignment2')
    
    for linenum, line in enumerate(lines[1:], 2):  # Start from 2 to account for the header
        try:
            person_id, name, birthday = line.split(',')
            birthday = datetime.datetime.strptime(birthday.strip(), "%d/%m/%Y").date()
            data_dict[int(person_id)] = (name.strip(), birthday)
        except ValueError as e:
            logger.error(f"Error processing line #{linenum} for ID #{person_id.strip()}")
    
    return data_dict

def displayPerson(person_id, personData):
    """Displays the person's name and birthday or an error message if the ID is not found."""
    if person_id in personData:
        name, birthday = personData[person_id]
        print(f"Person #{person_id} is {name} with a birthday of {birthday}")
    else:
        print("No user found with that id")

def setup_logger():
    """Sets up the logger to log errors to errors.log."""
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log')
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main(url):
    """Main function to download, process data and handle user interaction."""
    print(f"Running main with URL = {url}...")
    setup_logger()

    try:
        csvData = downloadData(url)
    except Exception as e:
        print(f"Failed to download data: {e}")
        sys.exit(1)

    personData = processData(csvData)

    while True:
        try:
            person_id = int(input("Enter an ID to look up (or 0 or negative to exit): "))
            if person_id <= 0:
                break
            displayPerson(person_id, personData)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main(url)
