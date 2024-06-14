import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter

# Function to fetch DNA sequence from a webpage
def fetch_sequence(url):
    try:
        # Send HTTP GET request to the URL
        response = requests.get(url)
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find relevant content where DNA sequence might be located
        # Adjust according to the structure of the webpage
        sequence = soup.find('pre').get_text()  
        return sequence.strip() 
    except Exception as e:
        print(f"Error fetching sequence from {url}: {e}")
        return None

# Function to calculate GC percentage
def calculate_gc_percentage(sequence):
    if not sequence:
        return None
    
    # Count occurrences of each nucleotide
    nucleotide_counts = Counter(sequence.upper())
    
    # Calculate GC percentage
    g_count = nucleotide_counts['G']
    c_count = nucleotide_counts['C']
    total_gc = g_count + c_count
    total_nucleotides = len(sequence)
    
    if total_nucleotides == 0:
        return 0.0
    else:
        return (total_gc / total_nucleotides) * 100

def process_csv(csv_file):
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(csv_file)

        # Add columns for GC percentage and sequences
        df['GC Percentage'] = None
        df['Sequence'] = None

        # Iterate over each row (assuming 'GenBank FTP' is the column name)
        for index, row in df.iterrows():
            url = row['GenBank FTP']
            # Fetch DNA sequence from URL
            sequence = fetch_sequence(url)
            if sequence:
                # Calculate GC percentage
                gc_percentage = calculate_gc_percentage(sequence)
                df.at[index, 'GC Percentage'] = gc_percentage
                df.at[index, 'Sequence'] = sequence
            else:
                print(f"Sequence not found for URL: {url}")

        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_file, index=False)
        print(f"Updated CSV file saved: {csv_file}")
    except Exception as e:
        print(f"Error processing CSV file: {e}")

# Example usage
if __name__ == "__main__":
    csv_file = 'viruses.csv'  
    process_csv(csv_file)
