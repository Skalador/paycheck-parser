import PyPDF2
import os
import sys
import re
import pandas as pd
import logging


# Configure the logger
logging.basicConfig(level=logging.INFO,  # Set the log level (e.g., INFO, DEBUG, WARNING)
                    format='%(levelname)s: %(message)s')

# Create a logger instance
logger = logging.getLogger('my_logger')


def findFiles():
    # Define a regular expression pattern to match "YYYY_MM.pdf" filenames
    pattern = r'\d{4}_\d{2}\.pdf'

    # Get the current working directory
    current_directory = os.getcwd()
    logger.debug(
        f'Trying to find files in {current_directory} which match the regexp pattern "{pattern}"')

    # List all files in the current directory
    files_in_directory = os.listdir(current_directory)
    logger.debug(
        f'Found the follwing files in this directory:\n {files_in_directory}')

    # Filter the list of files to find those matching the pattern
    matching_files = [
        filename for filename in files_in_directory if re.match(pattern, filename)]

    logger.info(
        f'The following files match the desired regexp pattern:\n {matching_files}')
    return matching_files


def extractTimePeriod(page_text):  # Obtain year and month
    pattern = r'für den Zeitraum (\w+) (\d{4})'
    match = re.search(pattern, page_text)
    if match:
        month = match.group(1)
        year = match.group(2)
        logger.debug(f'Found Year: {year}, Month: {month}')
        return year, month
    else:
        logger.error(
            f'Could not find the year and month with the pattern {pattern}')
        return None


def extractBRU(page_text):  # Obtain "Betriebsratsumlage"
    pattern = r'BRU 0,5 % (\d+,\d+)'
    matches = re.findall(pattern, page_text)

    BRU = 0
    for match in matches:
        logger.debug(f'Found BRU of {match}')
        formatted_match = float(match.replace(',', '.'))
        BRU += formatted_match

    logger.debug(f'Betriebsratsumlage is {BRU}')
    return BRU


def parseFile(filename):
    # creating a pdf file object
    pdfFileObj = open(filename, 'rb')
    logger.debug(f'Parsing file {filename}...')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # creating a page object form the first page
    pageObj = pdfReader.pages[0]

    # extracting text from page
    text = pageObj.extract_text()

    # read year and month from text
    result = extractTimePeriod(text)
    if result is None:
        logger.error(
            f'Could not parse file {filename} for time period, terminating ...')
        sys.exit(1)
    year, month = result

    # read "Betriebsratsumlage" from text
    BRU = extractBRU(text)
    if BRU == 0:
        logger.error(
            f'Could not parse file {filename} for "Betriebsratsumlage" because it is 0, terminating ...')
        sys.exit(1)

    # closing the pdf file object
    pdfFileObj.close()
    new_data_point = pd.DataFrame(
        {'Jahr': year, 'Monat': month, 'Beschreibung': 'Betriebsratsumlage', 'Wert': BRU},  index=[0])

    logger.debug(
        f'Returning datapoint \n {new_data_point.to_string(index=False)} \n for {filename}')
    return new_data_point


if __name__ == "__main__":

    matching_files = findFiles()
    df = pd.DataFrame()
    excel_file = 'Werbungskosten.xlsx'

    if not matching_files:
        logger.error(
            f'No file matches the desired regexp pattern, terminating ...')
        sys.exit(1)

    # Parse all files and append data to dataframe
    for filename in matching_files:
        df = pd.concat([df, parseFile(filename)])

    # Append the sum of the "Betriebsratsumlage"
    sum_bru = df['Wert'].sum()
    sum_bru_df = pd.DataFrame(
        {'Jahr': '', 'Monat': '', 'Beschreibung': 'Summe', 'Wert': sum_bru}, index=[0])
    df = pd.concat([df, sum_bru_df])

    logger.info(f'Full dataframe is \n {df.to_string(index=False)}')

    # Export the data to the Excel file
    df.to_excel(excel_file, index=False)

    logger.info(f'Data exported to {excel_file}')
