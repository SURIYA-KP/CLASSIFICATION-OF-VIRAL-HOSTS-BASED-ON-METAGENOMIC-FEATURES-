import pandas as pd

# Function to find coding sequences (CDS) in a given DNA sequence
def find_coding_sequences(sequence):
    sequence = sequence.upper()
    start_codon = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]
    cds_list = []

    i = 0
    while i < len(sequence) - 2:
        # Look for the start codon
        if sequence[i:i+3] == start_codon:
            for j in range(i + 3, len(sequence) - 2, 3):
                # Look for the stop codon
                if sequence[j:j+3] in stop_codons:
                    cds_list.append(sequence[i:j+3])
                    i = j + 3
                    break
            else:
                # No stop codon found, move to next codon
                i += 3
        else:
            i += 1
    return cds_list

# Function to process the CSV file
def process_csv(input_csv_file, output_csv_file):
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(input_csv_file)
        
        # Check if the required column exists
        if 'sequences' not in df.columns:
            print(f"Column 'sequences' not found in {input_csv_file}")
            return
        
        # Find CDS for each sequence and store it in a new column
        df['CDS'] = df['sequences'].apply(lambda seq: find_coding_sequences(seq))
        
        # Save the DataFrame with the new column to a new CSV file
        df.to_csv(output_csv_file, index=False)
        print(f"CDS saved to {output_csv_file}")
        
    except Exception as e:
        print(f"Error processing CSV file: {e}")

# Example usage
if __name__ == "__main__":
    input_csv_file = 'sequences.csv'  # Replace with your input CSV file path
    output_csv_file = 'cds_sequences.csv'  # Replace with your output CSV file path
    process_csv(input_csv_file, output_csv_file)
