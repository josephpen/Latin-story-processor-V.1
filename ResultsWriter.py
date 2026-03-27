# ResultsWriter.py
# Module: writes the looked-up vocab results to a text file.
 
import os
 
def write_results(results: list, output_folder: str, filename: str = "output.txt"):
    """
    Writes a list of (lemma, entry) tuples to a text file.
 
    Args:
        results:       List of (lemma, entry) tuples.
        output_folder: Folder path to write the file into.
        filename:      Name of the output file (default: output.txt).
    """
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
 
    with open(output_path, "w", encoding="utf-8") as f:
        for lemma, entry in results:
            f.write(f"{entry}\n")
 
    print(f"\nResults written to: {output_path}")