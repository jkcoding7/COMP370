import argparse
import csv
from collections import defaultdict
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='Process borough complaints from a CSV file.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-s', '--start', required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('-e', '--end', required=True, help='End date in YYYY-MM-DD format')
    parser.add_argument('-o', '--output', help='Output CSV file (optional)')
    return parser.parse_args()

def read_complaints(input_file):
    complaints = []
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            complaints.append(row)
    return complaints

def filter_complaints(complaints, start_date, end_date):
    filtered = []
    for complaint in complaints:
        created_date = datetime.strptime(complaint[1], '%m/%d/%Y %I:%M:%S %p')  # Adjusted format
        if start_date <= created_date <= end_date:
            filtered.append(complaint)
    return filtered

def count_complaints(complaints):
    counts = defaultdict(lambda: defaultdict(int))
    for complaint in complaints:
        complaint_type = complaint[5]  # Index for complaint_type
        borough = complaint[25]         # Index for borough
        counts[complaint_type][borough] += 1
    return counts

def write_output(counts, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['complaint type', 'borough', 'count'])
        for complaint_type, boroughs in counts.items():
            for borough, count in boroughs.items():
                writer.writerow([complaint_type, borough, count])

def print_output(counts):
    print('complaint type, borough, count')
    for complaint_type, boroughs in counts.items():
        for borough, count in boroughs.items():
            print(f'{complaint_type}, {borough}, {count}')

def main():
    args = parse_args()
    start_date = datetime.strptime(args.start, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')
    
    complaints = read_complaints(args.input)
    filtered_complaints = filter_complaints(complaints, start_date, end_date)
    counts = count_complaints(filtered_complaints)
    
    if args.output:
        write_output(counts, args.output)
    else:
        print_output(counts)

if __name__ == '__main__':
    main()
