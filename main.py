import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d import Axes3D

radius =10
cluster_centers = [
    (10, 30, 15),
    (70, 30, 20),
    (70, 70, 25)
]
color = ["#000000"]
points = []


def setup():
    for center in cluster_centers:
        for _ in range(30):
            x = random.uniform(center[0] - random.uniform(5, 15), center[0] + random.uniform(5, 15))
            y = random.uniform(center[1] - random.uniform(5, 15), center[1] + random.uniform(5, 15))
            z = random.uniform(center[2] - random.uniform(5, 15), center[2] + random.uniform(5, 15))
            points.append([x, y, z, -1])

    for _ in range(10):
        points.append([
            random.uniform(0, 110),
            random.uniform(0, 110),
            random.uniform(0, 50),
            -1
        ])


def find_neighbors(point1, point2):
    return math.dist([point1[0], point1[1], point1[2]], [point2[0], point2[1], point2[2]]) < radius


def set_ensemble(coeur, ensemble, visited=None):
    if visited is None:
        visited = set()

    visited.add(tuple(coeur))

    for point in points:
        if tuple(point) in visited:
            continue

        if find_neighbors(coeur, point) and point[3] == -1:
            point[3] = ensemble
            set_ensemble(point, ensemble, visited)


def dbscan():
    for point in points:
        if point[3] != -1:
            continue

        random_color = "#" + ''.join(random.choice('0123456789ABCDEF') for _ in range(6))
        color.append(random_color)

        point_color = len(color) - 1
        point[3] = point_color

        set_ensemble(point, point_color)
        delete_noise(point_color)


def delete_noise(couleur):
    filtered_points = [point for point in points if point[3] == couleur]
    if len(filtered_points) < 3:
        for point in filtered_points:
            point[3] = 0


def display_graph():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    z_coords = [point[2] for point in points]
    point_color = [color[point[3]] for point in points]

    ax.scatter(x_coords, y_coords, z_coords, color=point_color, label="Points")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.title("3D DBSCAN Algorithm")

    plt.legend()
    plt.grid(True)
    plt.show()


setup()
dbscan()
display_graph()
