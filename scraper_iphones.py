# Request libraries
import requests as r
from bs4 import BeautifulSoup
import csv

###############
# Scrape page
###############

urltoget = "http://drd.ba.ttu.edu/isqs6339/assign/assign_1/"

# Scrape URL
res = r.get(urltoget)

# Parse content into a soup object
soup = BeautifulSoup(res.content, "html")

## Status, headers, etc
# Page status
if res.status_code == 200:
    print("Status code of call: " + str(res.status_code))
else: print("bad request, received code " + str(res.status_code))
# Is redirect?
if res.is_redirect == False:
    print("Page is redirecting: False")
else: print("Page is redirecting")
# Page encoding
print("Current page encoding: " + str(res.encoding))
# Server header
print("Returned header for page: " + str(res.headers))

###################################################
# Deliver details for iPhone 11 Pro, specifically
###################################################

# Identify the phone list
plist = soup.find("div", attrs={"id": "phonelist"})

# Pull iPhone 11 entry and identify attributes
iphone11 = plist.find("ul").find_all("li", attrs={"class" : "root"})[1]
iphone_attr = iphone11.find("ul").find_all("li")

print("\nThe following are values for the iPhone 11 Pro")
# Split text for OS item (item 2 in iphone_attr) at the colon and pull/display
print("\nOS: ", iphone_attr[1].text.split(": ")[1])
# Split text for Color item (item 1 in iphone_attr) at the colon and pull/display
print("\nColor: ", iphone_attr[0].text.split(": ")[1])

#########################################
# Get details from the (child page) link
# for the iPhone 11 Pro
#########################################

# Get the link within the iPhone attributes list - build on original URL
res_childURL = r.get(urltoget + iphone_attr[2].find('a')['href'])

# Parse child page content into a soup object
child_soup = BeautifulSoup(res_childURL.content, 'html')

# Identify the part of the soup object where the phone details live
child_phone = child_soup.find('div', attrs={'id' : 'phonestuff'})
# Create an empty object for the phone features
features = ''
# Select the first node in the Phoneotherstuff div (the one containing item spans)
front_features = child_phone.find('div', attrs={'id' : 'Phoneotherstuff'}).find_all('span', attrs={'class' : 'item'})[0]
# Loop through the contents of that node and extract the text from each li item, adding it to features
for f in front_features.find_all('li'):
    features += f.text + ', '

# Select and print the item in the Phoneinitial div that corresponds to phone storage stat
print('\nStorage: ', child_phone.find('div', attrs={'id' : 'Phoneinitial'}).find_all('td')[3].text)
# Print the features list we looped, minus the last comma and space
print('\nFront camera Features: ', features[:-2])

###############################
# Export the website data for
# all phones to CSV file
###############################

# Define the location to save the file, and the filename
path = "/Users/katiewojciechowski/Desktop/Business_Intelligence/Scraper1/"
fileout = 'assign2.csv'

# Identify the part of the soup object where the needed details live
plistdiv = soup.find('div', attrs={'id' : 'phonelist'})
# Identify the needed details within that div
plistitems = plistdiv.find('ul').find_all('li', attrs={'class' : 'root'})

# Start file handling
with open(path + fileout, 'w') as file1:
    # Write the following attributes to the file
    file1.write('product_name,network,storage,color,os,product_size\n')
    
    # Loop over 
    for p in plistitems:
        # Define phone attributes from list items
        pattr = p.find('ul').find_all('li')
        # Call the child page
        res_child = r.get(urltoget + pattr[2].find('a')['href'])
        # Create a soup object for the child page content
        child_soup = BeautifulSoup(res_child.content, 'html')
        # Identify the part of the soup object where the phone details live
        child_phone = child_soup.find('div', attrs={'id' : 'phonestuff'})
        
        # The following will write a row in the CSV, with the desired data
        file1.write(p.find('span').text + ',' +
            child_phone.find('div', attrs={'id' : 'Phoneinitial'}).find_all('td')[5].text + ',' +
            child_phone.find('div', attrs={'id' : 'Phoneinitial'}).find_all('td')[3].text + ',' +
            pattr[1].text.split(': ')[1] + ',' +
            pattr[0].text.split(': ')[1] + ',' +
            child_phone.find('div', attrs={'id' : 'Phoneinitial'}).find_all('td')[1].text + '\n')