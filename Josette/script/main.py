import subprocess
import sys

def find_url_with_substring(filename, substring):
    with open(filename, 'r') as file:
        for line in file:
            if substring.upper() in line.upper():
                url = line.strip().split(',')[-1].strip()
                subprocess.run(['python3', './download_excel_file.py', url])
                return url
    return None

if __name__ == "__main__":
    filename = 'all_links.txt'  # replace with your actual text file name

    # Check if the command line argument has been provided
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <DRUG_NAME>")
        sys.exit(1)  # Exit the script

    substring = sys.argv[1]
    url_found = find_url_with_substring(filename, substring)

    if url_found:
        print("URL found:", url_found)
    else:
        print("No URL found with the given substring.")

