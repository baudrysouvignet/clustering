import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
from scipy.constants import point

DIMENSION = 3
CENTROID = 3

centroid_info = []

points = [[random.uniform(0, 10) for _ in range(DIMENSION)] for _ in range(200)]


# ---Global functions---

def euclidean_distance(point1, point2):
    return math.sqrt(sum((point1[i] - point2[i]) ** 2 for i in range(DIMENSION)))


def loop():
    centroids_changed = True

    while centroids_changed:
        assign_points_to_centroid()

        old_centroids = [centroid.copy() for centroid in centroid_info]

        update_centroids()
        assign_points_to_centroid()

        centroids_changed = old_centroids != centroid_info


def run():
    setup_centroids()
    loop()
    display_graph()


# ---Centroid functions---

def append_centroid(point):
    random_color = "#" + ''.join(random.choice('0123456789ABCDEF') for _ in range(6))
    centroid_info.append([
        point,
        random_color
    ])


def find_farthest_points():
    max_distance = 0
    max_distance_points = None

    for point in points:
        distance = min(euclidean_distance(point, centroid_info[i][0]) for i in range(len(centroid_info)))
        if distance > max_distance:
            max_distance = distance
            max_distance_points = point

    return max_distance_points


def define_centroid():
    if len(centroid_info) == 0:
        append_centroid(random.choice(points))
        return
    append_centroid(find_farthest_points())


def setup_centroids():
    while len(centroid_info) < CENTROID:
        define_centroid()


def new_centroid_position(centroid_index):
    centroid_points = [point for point in points if point[DIMENSION] == centroid_index]
    if len(centroid_points) == 0:
        return None

    new_coords = [sum(point[i] for point in centroid_points) / len(centroid_points) for i in range(DIMENSION)]

    return new_coords


def update_centroids():
    for i in range(len(centroid_info)):
        centroid_info[i][0] = new_centroid_position(i)
        if centroid_info[i][0] == None:
            centroid_info.remove(centroid_info[i])


# ---Define points on centroids functions---

def nearest_centroid(point):
    min_distance = float('inf')
    nearest_centroid = None
    for i in range(len(centroid_info)):
        distance = euclidean_distance(point, centroid_info[i][0])
        if distance < min_distance:
            min_distance = distance
            nearest_centroid = i
    return nearest_centroid


def assign_points_to_centroid():
    for point in points:
        if len(point) < DIMENSION + 1:
            point.append(nearest_centroid(point))
        else:
            point[DIMENSION] = nearest_centroid(point)


# ---Display functions---

def display_graph():
    if DIMENSION == 2:
        fig, ax = plt.subplots()

        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]
        point_color = [centroid_info[point[2]][1] for point in points]

        ax.scatter(x_coords, y_coords, color=point_color, label="Points")

        centroid_x_coords = [centroid[0][0] for centroid in centroid_info]
        centroid_y_coords = [centroid[0][1] for centroid in centroid_info]

        ax.scatter(centroid_x_coords, centroid_y_coords, color="red", label="Centroids", s=20)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        plt.title("2D K-means Algorithm")

    elif DIMENSION == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]
        z_coords = [point[2] for point in points]
        point_color = [centroid_info[point[3]][1] for point in points]

        ax.scatter(x_coords, y_coords, z_coords, color=point_color, label="Points")

        centroid_x_coords = [centroid[0][0] for centroid in centroid_info]
        centroid_y_coords = [centroid[0][1] for centroid in centroid_info]
        centroid_z_coords = [centroid[0][2] for centroid in centroid_info]

        ax.scatter(centroid_x_coords, centroid_y_coords, centroid_z_coords, color="red", label="Centroids", s=20)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.title("3D K-means Algorithm")

    plt.legend()
    plt.grid(True)
    plt.show()


# Run the functions
run()
