import re

def read_gcode(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def extract_coordinates(gcode_lines):
    x_coords = []
    y_coords = []

    for line in gcode_lines:
        x_match = re.search(r'X(-?\d+(\.\d+)?)', line)
        y_match = re.search(r'Y(-?\d+(\.\d+)?)', line)

        if x_match and y_match:
            x_coords.append(float(x_match.group(1)))
            y_coords.append(float(y_match.group(1)))

    return x_coords, y_coords
