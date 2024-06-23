import numpy as np

def interpolate_gcode(gcode_x, gcode_y, num_points):
    distance = np.linspace(0, 1, len(gcode_x))
    target_distance = np.linspace(0, 1, num_points)

    interpolated_x = np.interp(target_distance, distance, gcode_x)
    interpolated_y = np.interp(target_distance, distance, gcode_y)

    return interpolated_x, interpolated_y

def synchronize_data(gcode_x, gcode_y, csv_data, first_index, sampling_cycle, num_points):
    time_per_point = sampling_cycle / 1_000_000  # Convert microseconds to seconds
    csv_indices = [index for index, _, _ in csv_data]
    times = [(index - first_index) * time_per_point for index in csv_indices]

    if len(times) > len(gcode_x):
        gcode_x, gcode_y = interpolate_gcode(gcode_x, gcode_y, len(times))

    synchronized_data = []
    step = max(1, len(gcode_x) // num_points)
    for i, (time, (index, thickness, status)) in enumerate(zip(times, csv_data)):
        if i % step == 0 and i < len(gcode_x):
            synchronized_data.append((gcode_x[i], gcode_y[i], thickness, time))

    return synchronized_data
