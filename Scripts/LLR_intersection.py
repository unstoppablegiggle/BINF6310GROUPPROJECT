"""Importing required modules"""
import argparse
import csv

from utils.utils import get_filehandle


def read_llr_file(file_path):
    """
    Read LLR values from a CSV file and return a set of unique symbols.

    Parameters:
    - file_path (str): The path to the CSV file containing LLR values.

    Returns:
    set: A set of unique LLR values.
    """
    llr_set = set()
    with open(file_path, 'r', newline='') as csvfile:
        # Create a CSV reader
        csv_reader = csv.reader(csvfile, delimiter=',')

        # Skip header line if present
        next(csv_reader, None)

        # Return a set of unique LLR values
        for row in csv_reader:
            if len(row) > 2:  # Assuming the LLR value is in the third column
                llr_score = row[2]
                llr_set.add(llr_score)

    return llr_set


def find_intersection(file1, file2):
    """
    Find the intersection of gene symbols between two files.

    Parameters:
    - file1 (str): The path to the first file containing gene symbols.
    - file2 (str): The path to the second file containing gene symbols.

    Returns:
    tuple: A tuple containing:
        - list: A list of common gene symbols found in both files.
        - int: The number of common gene symbols.
    """
    set1 = read_llr_file(file1)
    set2 = read_llr_file(file2)

    common_llr = list(set1.intersection(set2))
    common_count = len(common_llr)

    return common_llr, common_count


def main():
    """
    The main function that performs the business logic
     of finding the intersection of gene symbols between two files.

    Returns:
    None
    """
    # Argument parser
    parser = argparse.ArgumentParser(description='Provide two llr lists, find intersection.')
    parser.add_argument('-i1', '--infile1', help='LLR list 1 to open', default='test.csv')
    parser.add_argument('-i2', '--infile2', help='LLR list 2 to open', default='benchmark_with_tiled_scores.csv')

    # Parse command line arguments
    args = parser.parse_args()

    # Find the intersection
    common_llr, common_count = find_intersection(args.infile1, args.infile2)

    # Print the results to the terminal
    print(f'Number of unique LLR in {args.infile1}: {len(read_llr_file(args.infile1))}')
    print(f'Number of unique LLR in {args.infile2}: {len(read_llr_file(args.infile2))}')
    print(f'Number of common LLR found: {common_count}')

    # Write the results to the output file
    output_file = 'intersection_output.txt'
    with get_filehandle(output_file, 'w') as output:
        for llr in sorted(common_llr):
            output.write(f'{llr}\n')

    print(f'Output stored in {output_file}')


if __name__ == '__main__':
    main()
