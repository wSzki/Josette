import requests

def find_url(substring, file_path='all_links.txt'):
    # Make the search case-insensitive by lowering the substring
    lower_substring = substring.lower()
    with open(file_path, 'r') as file:
        for line in file:
            if lower_substring in line.lower():
                # Extract the URL from the line
                url = line.strip().split(', ')[-1]  # Assuming the format is Name, URL
                return url
    return None

def download_file_from_url(url, download_name, session):
    # Set the necessary headers to mimic a browser session
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        # Add any other necessary headers here
    }

    # Make a GET request to the URL to initiate the session and get any required tokens
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        # Check if there are any tokens or session variables you need to extract here

        # Then request the file download
        download_url = 'https://dap.ema.europa.eu/analytics/saw.dll?generateDashboardExcel'
        download_response = session.get(download_url, headers=headers, stream=True)

        if download_response.status_code == 200:
            # Set the file name based on the input
            filename = f'{download_name.replace(" ", "_")}.xlsx'

            # Stream the download to handle large files
            with open(filename, 'wb') as f:
                for chunk in download_response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f'File downloaded successfully and saved as {filename}')
        else:
            print('Failed to download the file. Status code:', download_response.status_code)
    else:
        print('Failed to reach the URL. Status code:', response.status_code)

# Main code
if __name__ == "__main__":
    # Create a session object that will be used throughout
    session = requests.Session()

    # Take input from the user
    drug_name = input("Enter the drug name or substring to search for: ")

    # Find the corresponding URL
    found_url = find_url(drug_name)
    if found_url:
        print(f'URL found: {found_url}')
        # Download the file and rename it as per the input
        download_file_from_url(found_url, drug_name, session)  # Pass the session to maintain state
    else:
        print('No matching URL found in the file.')

