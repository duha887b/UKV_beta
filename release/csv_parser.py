import csv

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        lines = list(reader)
    return lines

def parse_csv_data(lines):
    header = {}
    data = []
    header_end = False

    for line in lines:
        if not header_end:
            if line and line[0] == '':
                header_end = True
                continue
            if len(line) > 1:
                header[line[0]] = line[1]
        else:
            if len(line) == 3 and line[0].isdigit():
                try:
                    data.append((int(line[0]), float(line[1].replace(',', '.')), line[2]))
                except ValueError as e:
                    print(f"Error parsing line: {line} - {e}")

    return header, data
