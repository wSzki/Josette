import subprocess


def find_url_with_substring(filename, substring):
    # Open the file for reading
    with open(filename, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Check if the substring is in the line
            if substring.upper() in line.upper():
                # Assuming the URL is the last element after splitting the line by comma
                url = line.strip().split(',')[-1].strip()
                subprocess.run(['python3', './download_excel_file.py', url])
                return url
    # Return None if the substring is not found
    return None

# The script can be used with a function call like this:
# Replace 'drug_list.txt' with the actual file name and 'DIPHENHYDRAMINE' with the desired substring.
# url_found = find_url_with_substring('drug_list.txt', 'DIPHENHYDRAMINE')
# if url_found:
#     print("URL found:", url_found)
# else:
#     print("No URL found with the given substring.")

# For the script to work interactively, you can use input() to ask the user for a substring.
if __name__ == "__main__":
    filename = 'all_links.txt'  # replace with your actual text file name
    substring = input("Enter the drug name to search for: ")
    url_found = find_url_with_substring(filename, substring)
    if url_found:
        print("URL found:", url_found)
    else:
        print("No URL found with the given substring.")

