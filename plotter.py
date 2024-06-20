import plotly.graph_objects as go
import numpy as np


def plot_2d(x_coords, y_coords, synchronized_data, num_points):
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)

    indices = np.linspace(0, len(x_coords) - 1, num_points).astype(int)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_coords[indices],
        y=y_coords[indices],
        mode='lines+markers',
        name='G-Code Path'
    ))

    sync_x = [data[0] for data in synchronized_data]
    sync_y = [data[1] for data in synchronized_data]
    sync_thickness = [data[2] for data in synchronized_data]

    fig.add_trace(go.Scatter(
        x=sync_x,
        y=sync_y,
        mode='markers',
        marker=dict(color='red', size=8),
        name='Thickness Points'
    ))

    fig.update_layout(
        title='2D Plot of G-Code Path with Thickness Measurements',
        xaxis_title='X Coordinate',
        yaxis_title='Y Coordinate'
    )

    return fig


def plot_3d(x_coords, y_coords, synchronized_data, num_points):
    if not synchronized_data:
        print("No synchronized data to plot.")
        return None

    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)

    indices = np.linspace(0, len(x_coords) - 1, num_points).astype(int)

    sync_x = [data[0] for data in synchronized_data]
    sync_y = [data[1] for data in synchronized_data]
    sync_thickness = [data[2] for data in synchronized_data]

    fig = go.Figure()

    # Plot G-Code Path (z=0)
    fig.add_trace(go.Scatter3d(
        x=x_coords[indices],
        y=y_coords[indices],
        z=[0] * len(x_coords[indices]),
        mode='lines+markers',
        name='G-Code Path',
        marker=dict(size=4, symbol='circle')
    ))

    # Plot Thickness Measurement (using thickness as z)
    fig.add_trace(go.Scatter3d(
        x=sync_x,
        y=sync_y,
        z=sync_thickness,
        mode='markers',
        marker=dict(color='red', size=5, symbol='circle'),
        name='Thickness Measurement'
    ))

    # Add vertical lines connecting G-Code path to thickness measurement points
    for x, y, thickness in zip(sync_x, sync_y, sync_thickness):
        fig.add_trace(go.Scatter3d(
            x=[x, x],
            y=[y, y],
            z=[0, thickness],
            mode='lines',
            line=dict(color='gray', width=1),
            showlegend=False
        ))

    fig.update_layout(
        title='3D Plot of G-Code Path with Thickness Measurements',
        scene=dict(
            xaxis=dict(title='X Coordinate', tickformat='.2f'),
            yaxis=dict(title='Y Coordinate', tickformat='.2f'),
            zaxis=dict(title='Z/Thickness (um)', tickformat='.2f')
        ),
        showlegend=True
    )

    return fig


def plot_time(csv_data, sampling_cycle, first_index, num_points):
    indices = [index for index, thickness, status in csv_data]
    thicknesses = [thickness for index, thickness, status in csv_data]

    times = [(index - first_index) * (sampling_cycle / 1_000_000) for index in indices]

    times = np.array(times)
    thicknesses = np.array(thicknesses)

    indices = np.linspace(0, len(times) - 1, num_points).astype(int)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times[indices],
        y=thicknesses[indices],
        mode='lines+markers',
        name='Thickness over Time'
    ))

    fig.update_layout(
        title='Thickness Measurement Over Time',
        xaxis_title='Time (seconds)',
        yaxis_title='Thickness (um)'
    )

    return fig


