# import libraries
import urllib
import pandas as pd
import sqlite3 as lite
from pytz import timezone
from datetime import datetime
from bs4 import BeautifulSoup

###################### THIS PORTION REQUIRES USER INPUT ######################

# specify url to scrape
url = 'http://www.centricaremit.com/index.asp?pageid=1203'

# specify SQL connection
SQL_con = 'mydb.sqlite3' # this is a dummy connection

############################ FUNCTION DEFINITIONS ############################

def check_duplicates(df):
    """Check for duplicated rows in the dataframe and returns the dataframe with duplicated rows removed (if any)
    
    Arg:
        df: dataframe
    
    Return:
        df: if dataframe has duplicated rows, function will return the dataframe with duplicated rows removed.
            otherwise, the original dataframe will be returned (dataframe)
    """
    if (df.duplicated().any()==True):
        df.drop_duplicates(inplace=True)
    return(df)

def define_datatype(df):
    """Define the data types for each element in the dataframe and returns the dataframe with data types properly defined 
    
    Arg:
        df: dataframe
    
    Return:
        df: dataframe with data types properly defined (dataframe)
    """
    # initialise col_name
    col_name = df.columns.astype(list)
    
    # convert elements in dataframe to str
    for i in range(19):
        df[col_name[i]] = [str(x) for x in df.iloc[:,i]]
        
    # replace empty fields (eg. '-' and NaN values) with None
    df = df.where(df!='\r\n            -\r\n          ', None)
    df = df.where(df!='\r\n            Unknown\r\n          ', None)
        
    # convert elements in columns 0, 4 and 5 to datetime
    uk_tz = timezone('Europe/London') # define correct timezone (eg.UK)
    for i in [0, 4, 5]:
        df[col_name[i]] = [uk_tz.localize(datetime.strptime(x,'%d.%m.%Y %H:%M')) if x is not None else None for x in df.iloc[:,i]]

    # convert elements in columns 1, 2, 3, 6, 7, 8, 9, 10, 14, 15, 16, 17 and 18 to str
    for i in [1, 2, 3, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18]:
        df[col_name[i]] = [str(x) if x is not None else None for x in df.iloc[:,i]]
        
    # convert elements in columns 11, 12 and 13 to float
    for i in [11, 12, 13]: 
        df[col_name[i]] = [float(x) if x is not None else None for x in df.iloc[:,i]]
    
    return(df)
    
################################# MAIN CODE ################################## 

# query the website and return the html to the variable 'webpage'
webpage = urllib.request.urlopen(url)
    
# parse the html in the 'webpage' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(webpage, 'html.parser')
    
right_table = soup.find_all('table', class_='financial remit_content_upstream')
    
# generate lists
A = [] # Publication Date (datetime)
B = [] # MessageID (str)
C = [] # URL (str)
D = [] # Unavailability Type (str)
E = [] # Event Start (datetime)
F = [] # Estimated Event Stop (datetime)
G = [] # Asset (str)
H = [] # Market Area (str)
I = [] # Balancing Zone (str)
J = [] # EMT Status (str)
K = [] # Event Status (str)
L = [] # Technical Capacity (float)
M = [] # Approximate Available Capacity (float)
N = [] # Approximate Unavailable Capacity (float)
O = [] # Unit (str)
P = [] # Unavailability Reason (str)
Q = [] # Event Type (str)
R = [] # Market Participant (str)
S = [] # Market Participant Code (str)
    
col_name = [] # Column names
    
# extract information and append it to the lists
row_no=1
for row in right_table[0].find_all('tr'):
    if row_no==1:
        cells = row.find_all('th')
        for i in range(len(cells)):
            col_name.append(cells[i].find(text=True)) 
            if (i==2):
                col_name.append('URL')
        
    else: 
        cells = row.find_all('td')
        A.append(cells[0].find(text=True))
        B.append(cells[1].find(text=True))
        C.append('http://www.centricaremit.com/'+str(cells[1].find('a').get('href')))
        D.append(cells[2].find(text=True))
        E.append(cells[3].find(text=True))
        F.append(cells[4].find(text=True))
        G.append(cells[5].find(text=True))
        H.append(cells[6].find(text=True))
        I.append(cells[7].find(text=True))
        J.append(cells[8].find(text=True))
        K.append(cells[9].find(text=True))
        L.append(cells[10].find(text=True))
        M.append(cells[11].find(text=True))
        N.append(cells[12].find(text=True))
        O.append(cells[13].find(text=True))
        P.append(cells[14].find(text=True))
        Q.append(cells[15].find(text=True))
        R.append(cells[16].find(text=True))
        S.append(cells[17].find(text=True))
        
    row_no += 1
        
    # convert lists to dataframe
    col_name = [header.replace(' ', '_') for header in col_name] # replace whitespaces with underscores
    col_name = [header.replace('_(local_time)', '') for header in col_name] # remove _(local time)_  
        
    df = pd.DataFrame(A, columns=[col_name[0]])
    df[col_name[1]] = B
    df[col_name[2]] = C
    df[col_name[3]] = D
    df[col_name[4]] = E
    df[col_name[5]] = F
    df[col_name[6]] = G
    df[col_name[7]] = H
    df[col_name[8]] = I
    df[col_name[9]] = J
    df[col_name[10]] = K
    df[col_name[11]] = L
    df[col_name[12]] = M
    df[col_name[13]] = N
    df[col_name[14]] = O
    df[col_name[15]] = P
    df[col_name[16]] = Q
    df[col_name[17]] = R
    df[col_name[18]] = S
    
    # check for duplicates
    df = check_duplicates(df)
    
    # define the datatype for each element in the dataframe
    df = define_datatype(df)
    
    # initialize the sql connection.
    con = lite.connect(SQL_con)
    
    # convert to dataframe and write to sql database.
    df.to_sql('test', con, flavor='sqlite', schema=None, if_exists='replace', index=False, index_label=None)
     
    # close the SQL connection
    con.close()


