## Zenalytics-Technical-Test
Design a client that visits the website http://www.centricaremit.com/index.asp?pageid=1203 to extract data

### Basic Requirements:
* You are required to extract information from the table and store it into a database
* The data is to be stored in a SQL database (eg. Sqlite) and is meant to be updated everyday. (hint below)
* There should not be duplicates in the database.
* Data type, such as datetime, float, and integer, must be properly defined.
* All datetime fields have to be adjusted for timezone.
* If the time of some entries in a datetime field is ‘unknown’, set it to null
* All nan values and '-' should be converted to null.
* Include documentation for your code
* Keep the code as DRY and readable as possible.

### Additional requirements (Bonus):
* The client should allow for exception handling and retry in case of failure.
* Include tests for your functions where applicable.
* The column ‘MessageID’ contains url links that provides more information. Include these information in the same database.

## Requirements
* Python 3.6 and up

## Installation
Before running the codes, please install the following packages.
* beautifulsoup4
```python
pip install beautifulsoup4
```
* pytz
```python
pip install pytz
```

## Usage
Download the code and run it. 

