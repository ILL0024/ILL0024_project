"""
import math
import json
import itertools
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random


class Planet:
    def __init__(self, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0


class Simulation:
    def __init__(self, planets):
        self.planets = planets
        self.positions = []

    def calculate_acceleration(self, dt):
        G = 6.674 * 10 ** (-11)
        for p1, p2 in itertools.combinations(self.planets, 2):
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            r = math.sqrt(dx ** 2 + dy ** 2)
            f = G * p1.mass * p2.mass / r ** 2
            theta = math.atan2(dy, dx)
            p1.ax += f * math.cos(theta) / p1.mass
            p1.ay += f * math.sin(theta) / p1.mass
            p2.ax -= f * math.cos(theta) / p2.mass
            p2.ay -= f * math.sin(theta) / p2.mass

        for planet in self.planets:
            planet.x += planet.vx * dt + 0.5 * planet.ax * dt ** 2
            planet.y += planet.vy * dt + 0.5 * planet.ay * dt ** 2
            planet.vx += planet.ax * dt
            planet.vy += planet.ay * dt
            planet.ax = 0
            planet.ay = 0

    def simulate(self, num_steps, dt):
        for _ in range(num_steps):
            self.calculate_acceleration(dt)
            self.update_positions()

    def update_positions(self):
        for planet in self.planets:
            planet.x += planet.vx + 0.5 * planet.ax
            planet.y += planet.vy + 0.5 * planet.ay
            planet.vx += 0.5 * planet.ax
            planet.vy += 0.5 * planet.ay
            planet.ax = 0
            planet.ay = 0

        self.positions.append([(planet.x, planet.y) for planet in self.planets])

    def plot_positions(self):
        fig, ax = plt.subplots()

        for planet in self.planets:
            circle = plt.Circle((planet.x, planet.y), planet.mass, color='blue')
            ax.add_artist(circle)

        ax.set_aspect('equal')
        ax.autoscale_view()
        plt.show()

    def create_animation(self):
        fig, ax = plt.subplots()
        x_data = []
        y_data = []
        masses = []
        scat = ax.scatter(x_data, y_data, s=masses, color='blue')

        def update(frame):
            x_data, y_data = zip(*self.positions[frame])
            masses = [planet.mass for planet in self.planets]
            scat.set_offsets(list(zip(x_data, y_data)))
            scat.set_sizes(masses)
            return scat,

        anim = FuncAnimation(fig, update, frames=len(self.positions), interval=50)
        plt.show()

    def save_animation(self, filename):
        fig, ax = plt.subplots()
        x_data = []
        y_data = []
        masses = []
        scat = ax.scatter(x_data, y_data, s=masses, color='blue')

        def update(frame):
            nonlocal x_data, y_data, masses
            x_data, y_data = zip(*self.positions[frame])
            masses = [planet.mass for planet in self.planets]
            scat.set_offsets(list(zip(x_data, y_data)))
            scat.set_sizes(masses)
            return scat,

        anim = FuncAnimation(fig, update, frames=len(self.positions), interval=50)
        anim.save(filename, writer='ffmpeg', fps=30)


def load_initial_conditions(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [Planet(p['mass'], p['x'], p['y'], p['vx'], p['vy']) for p in data['planets']]


def generate_random_conditions(num_planets, min_mass, max_mass, min_distance, max_distance, max_velocity):
    planets = []
    for _ in range(num_planets):
        mass = random.uniform(min_mass, max_mass)
        distance = random.uniform(min_distance, max_distance)
        velocity = random.uniform(0, max_velocity)
        angle = random.uniform(0, 2 * math.pi)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        vx = velocity * math.sin(angle)
        vy = velocity * math.cos(angle)
        planets.append(Planet(mass, x, y, vx, vy))
    return planets


def main():
    planets = load_initial_conditions('initial_conditions.json')

    #planets = generate_random_conditions(num_planets=5, min_mass=1e10, max_mass=5e10, min_distance=1e9, max_distance=5e9, max_velocity=1e3)

    simulation = Simulation(planets)
    simulation.simulate(num_steps=1000, dt=0.01)
    simulation.plot_positions()

    simulation.create_animation()

    simulation.save_animation('animation.mp4')


if __name__ == '__main__':
    main()


"""

import json
import numpy as np
import matplotlib.pyplot as plt


class Planet:
    def __init__(self, name, position, velocity, mass):
        self.name = name
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.mass = mass


class PlanetaryMotionSimulator:
    def __init__(self, planets, G=6.67430e-11, time_step=3600):
        self.planets = planets
        self.G = G
        self.time_step = time_step
        self.positions = {planet.name: [] for planet in self.planets}

    def calculate_acceleration(self, planet):
        acceleration = np.zeros(2)
        for other_planet in self.planets:
            if planet != other_planet:
                position_diff = other_planet.position - planet.position
                distance = np.linalg.norm(position_diff)
                force = self.G * planet.mass * other_planet.mass / distance**2
                acceleration += force * position_diff / distance
        return acceleration

    def simulate_motion(self, num_steps):
        for _ in range(num_steps):
            for planet in self.planets:
                acceleration = self.calculate_acceleration(planet)
                planet.velocity += acceleration * self.time_step
                planet.position += planet.velocity * self.time_step
                self.positions[planet.name].append(planet.position.copy())

    def save_positions_to_json(self, file_path):
        data = {}
        for planet in self.planets:
            data[planet.name] = [pos.tolist() for pos in self.positions[planet.name]]

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

    def plot_motion(self):
        for planet in self.planets:
            planet_positions = self.positions[planet.name]
            x = [pos[0] for pos in planet_positions]
            y = [pos[1] for pos in planet_positions]
            plt.plot(x, y, label=planet.name)

        plt.xlabel('X position')
        plt.ylabel('Y position')
        plt.title('Planetary Motion')
        plt.legend()
        plt.savefig('planetary_motion.png')  # Save the plot as an image
        plt.show()

    def generate_random_scenario(cls, num_planets):
        planets = []
        for i in range(num_planets):
            name = "Planet " + str(i + 1)
            position = np.random.uniform(-1e12, 1e12, size=(2,))
            velocity = np.random.uniform(-1000, 1000, size=(2,))
            mass = np.random.uniform(1e20, 1e30)
            planet = Planet(name, position, velocity, mass)
            planets.append(planet)
        return cls(planets)


def load_initial_conditions_from_json(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)

    planets = []
    for name, planet_data in data.items():
        position = planet_data['position']
        velocity = planet_data['velocity']
        mass = planet_data['mass']
        planet = Planet(name, position, velocity, mass)
        planets.append(planet)

    return PlanetaryMotionSimulator(planets)


file_path = 'planets.json'
simulator = load_initial_conditions_from_json(file_path)

num_steps = 50  # Number of simulation steps

simulator.simulate_motion(num_steps)
simulator.save_positions_to_json('positions.json')
simulator.plot_motion()

