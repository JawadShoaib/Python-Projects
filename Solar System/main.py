import pygame
import math
# Jawad Shoaib
from pygame.constants import SCALED

pygame.init()
pygame.display.set_caption('Solar System Simulation')

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = 	(231,125,17)
DARK_GREY = "#B7B8B9"
WHITE = '#928590'

FONT = pygame.font.SysFont('Lexend', 16)
class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200/ AU # 1 AU = 100 pixel
    TIMESTEP = 3600 *24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_velv = 0
        self.y_velv = 0
        
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2 
        y = self.y * self.SCALE + HEIGHT/2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000)}Km", 1, WHITE)
            WIN.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()))
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x , other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance **2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velv += total_fx / self.mass * self.TIMESTEP
        self.y_velv += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_velv * self.TIMESTEP
        self.y += self.y_velv * self.TIMESTEP

        self.orbit.append((self.x, self.y))
def mainloop():
    run = True
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 30, YELLOW, 1.9891*10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 15, BLUE, 5.972 * 10**24)
    earth.y_velv = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_velv = 24.077 * 1000

    mercury = Planet(-0.387 * Planet.AU, 0, 8, DARK_GREY, 3.285 * 10**23)
    mercury.y_velv = 47.4 * 1000

    venus = Planet(-0.723 * Planet.AU, 0, 13, WHITE, 4.867 * 10**24)
    venus.y_velv = 35.02 * 1000


    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()

#dd
mainloop()