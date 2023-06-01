import math
import json
import itertools
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


def load_initial_conditions(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['planets']


def calculate_acceleration(planets, positions):
    G = 6.674 * 10 ** (-11)
    for p1, p2 in itertools.combinations(planets, 2):
        dx = p2['x'] - p1['x']
        dy = p2['y'] - p1['y']
        r = math.sqrt(dx ** 2 + dy ** 2)
        f = G * p1['mass'] * p2['mass'] / r ** 2
        theta = math.atan2(dy, dx)
        p1['ax'] += f * math.cos(theta) / p1['mass']
        p1['ay'] += f * math.sin(theta) / p1['mass']
        p2['ax'] -= f * math.cos(theta) / p2['mass']
        p2['ay'] -= f * math.sin(theta) / p2['mass']

    for planet in planets:
        planet['x'] += planet['vx'] + 0.5 * planet['ax']
        planet['y'] += planet['vy'] + 0.5 * planet['ay']
        planet['vx'] += 0.5 * planet['ax']
        planet['vy'] += 0.5 * planet['ay']
        planet['ax'] = 0
        planet['ay'] = 0

    positions.append([(planet['x'], planet['y']) for planet in planets])


def plot_positions(planets):
    fig, ax = plt.subplots()
    for planet in planets:
        ax.scatter(planet['x'], planet['y'], s=planet['mass'], color='blue')
    plt.show()


def record_positions(planets, positions):
    positions.append([(planet['x'], planet['y']) for planet in planets])


def create_animation(planets, positions):
    fig, ax = plt.subplots()
    x_data = []
    y_data = []
    masses = []
    scat = ax.scatter(x_data, y_data, s=masses, color='blue')

    def update(frame):
        nonlocal x_data, y_data, masses
        x_data, y_data = zip(*positions[frame])
        masses = [planet['mass'] for planet in planets]
        scat.set_offsets(list(zip(x_data, y_data)))
        scat.set_sizes(masses)
        return scat,

    anim = FuncAnimation(fig, update, frames=len(positions), interval=50)
    plt.show()


def save_animation(planets, positions, filename):
    fig, ax = plt.subplots()
    x_data = []
    y_data = []
    masses = []
    scat = ax.scatter(x_data, y_data, s=masses, color='blue')

    def update(frame):
        nonlocal x_data, y_data, masses
        x_data, y_data = zip(*positions[frame])
        masses = [planet['mass'] for planet in planets]
        scat.set_offsets(list(zip(x_data, y_data)))
        scat.set_sizes(masses)
        return scat,

    anim = FuncAnimation(fig, update, frames=len(positions), interval=50)
    anim.save(filename, writer='ffmpeg', fps=30)


def generate_random_conditions(num_planets, min_mass, max_mass, min_distance, max_distance, max_speed):
    planets = []
    for i in range(num_planets):
        mass = random.uniform(min_mass, max_mass)
        x = random.uniform(-max_distance, max_distance)
        y = random.uniform(-max_distance, max_distance)
        while any(math.sqrt((x - planet['x']) ** 2 + (y - planet['y']) ** 2) < min_distance for planet in planets):
            x = random.uniform(-max_distance, max_distance)
            y = random.uniform(-max_distance, max_distance)
        vx = random.uniform(-max_speed, max_speed)
        vy = random.uniform(-max_speed, max_speed)
        planets.append({'mass': mass, 'x': x, 'y': y, 'vx': vx, 'vy': vy, 'ax': 0, 'ay': 0})
    return planets


def main():
    planets = load_initial_conditions('initial_conditions.json')

    # planets = generate_random_conditions(num_planets=5, min_mass=1e10, max_mass=5e10, min_distance=1e9, max_distance=5e9, max_speed=1e3)

    positions = []
    velocities = []

    for i in range(1000):
        calculate_acceleration(planets, positions)

        for planet in planets:
            planet['x'] += planet['vx'] + 0.5 * planet['ax']
            planet['y'] += planet['vy'] + 0.5 * planet['ay']
            planet['vx'] += 0.5 * planet['ax']
            planet['vy'] += 0.5 * planet['ay']
            planet['ax'] = 0
            planet['ay'] = 0

        record_positions(planets, positions)
        velocities.append([(planet['vx'], planet['vy']) for planet in planets])

    save_animation(planets, positions, filename='planets.mp4')


if __name__ == '__main__':
    main()