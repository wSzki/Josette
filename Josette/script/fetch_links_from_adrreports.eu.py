
import requests
from bs4 import BeautifulSoup
import string

# Function to fetch and store <a> elements in a file
def fetch_and_store_links(filename):
    # Start a session to keep cookies
    session = requests.Session()

    # The cookie name and value you want to set
    cookie_name = 'disclaimer_accepted'
    cookie_value = 'true'

    # Set the cookie in the session
    session.cookies.set(cookie_name, cookie_value)

    # Open the file to write
    with open(filename, 'w', encoding='utf-8') as file:
        # Loop over every letter in the alphabet
        for letter in string.ascii_lowercase:
            # Format the URL for the current letter
            url = f'https://www.adrreports.eu/tables/substance/{letter}.html'

            # Make a GET request to the page
            response = session.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Initialize BeautifulSoup to parse the page content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all <tr> elements
                table_rows = soup.find_all('tr')

                # Iterate over each <tr> element and find all <a> tags within it
                for tr in table_rows:
                    # Find all <a> tags within this <tr> tag
                    a_tags = tr.find_all('a')
                    for a in a_tags:
                        # Write the text and the href attribute of each <a> tag to the file
                        file.write(f"{a.text}, {a.get('href')}\n")
            else:
                print(f"Failed to access the page for letter {letter}.")

# Specify the filename where you want to store the links
filename = "all_links.txt"

# Call the function to fetch and store the links
fetch_and_store_links(filename)

print(f"All links have been written to {filename}.")

