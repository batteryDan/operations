import pygame
import sys
import datetime

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Travel Cartoon - Date Simulation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GREEN = (50, 200, 50)
RED = (255, 50, 50)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Function to draw a car
def draw_car(surface, x, y, color):
    # Car body
    pygame.draw.rect(surface, color, (x, y, 60, 30))
    # Wheels
    pygame.draw.circle(surface, BLACK, (int(x + 15), y + 30), 8)
    pygame.draw.circle(surface, BLACK, (int(x + 45), y + 30), 8)

# Function to draw a person
def draw_person(surface, x, y, color):
    # Head
    pygame.draw.circle(surface, color, (int(x), y), 10)
    # Body
    pygame.draw.line(surface, color, (int(x), y + 10), (int(x), y + 30), 2)
    # Arms
    pygame.draw.line(surface, color, (int(x), y + 15), (int(x - 10), y + 25), 2)
    pygame.draw.line(surface, color, (int(x), y + 15), (int(x + 10), y + 25), 2)
    # Legs
    pygame.draw.line(surface, color, (int(x), y + 30), (int(x - 10), y + 40), 2)
    pygame.draw.line(surface, color, (int(x), y + 30), (int(x + 10), y + 40), 2)

# Define a Car class to manage each car's properties and behavior
class Car:
    def __init__(self, x, y, color, speed, start_date, people_count, destination):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed  # pixels per frame
        self.start_date = start_date  # datetime.date object
        self.people_count = people_count
        self.destination = destination
        self.moving = False

    def update(self, current_date):
        if current_date >= self.start_date:
            self.moving = True
        if self.moving:
            dest_x, dest_y = self.destination
            # Move towards destination
            dx = dest_x - self.x
            dy = dest_y - self.y
            distance = (dx**2 + dy**2) ** 0.5
            if distance > self.speed:
                self.x += self.speed * dx / distance
                self.y += self.speed * dy / distance
            else:
                # Arrived at destination
                self.x = dest_x
                self.y = dest_y
                self.moving = False

    def draw(self, surface):
        draw_car(surface, self.x, self.y, self.color)
        # Draw people above the car
        for i in range(self.people_count):
            person_x = self.x + 30 + (i * 20) - ((self.people_count - 1) * 10)
            draw_person(surface, person_x, self.y - 50, BLACK)

# Map dates to animation times
start_sim_date = datetime.date(2023, 12, 9)
end_sim_date = datetime.date(2023, 12, 20)
total_sim_days = (end_sim_date - start_sim_date).days + 1  # Inclusive
seconds_per_day = 2
total_simulation_time = total_sim_days * seconds_per_day * 1000  # in milliseconds

# Define destinations with updated names and positions
destinations = {
    'MSP-Airport': (100, 100),
    "Guy's House": (800, 400),
    "Girl's House": (800, 100),
    'Cobblestone-Hotel': (500, 300),
}

# Create cars with updated destinations
cars = [
    Car(x=150, y=200, color=RED, speed=2, start_date=datetime.date(2023, 12, 9), people_count=2, destination=destinations["Guy's House"]),
    Car(x=150, y=250, color=BLUE, speed=2, start_date=datetime.date(2023, 12, 11), people_count=1, destination=destinations["Girl's House"]),
    Car(x=150, y=300, color=GREEN, speed=2, start_date=datetime.date(2023, 12, 15), people_count=3, destination=destinations["Guy's House"]),
    Car(x=150, y=350, color=ORANGE, speed=2, start_date=datetime.date(2023, 12, 18), people_count=2, destination=destinations['MSP-Airport']),
    Car(x=150, y=400, color=PURPLE, speed=2, start_date=datetime.date(2023, 12, 20), people_count=4, destination=destinations['Cobblestone-Hotel']),
]

# Main loop
clock = pygame.time.Clock()
running = True
start_ticks = pygame.time.get_ticks()

# Font for displaying text
font = pygame.font.SysFont(None, 24)

while running:
    delta_time = clock.tick(60)  # Limit to 60 frames per second
    elapsed_time = pygame.time.get_ticks() - start_ticks

    # Calculate the current simulated date
    days_passed = elapsed_time / (seconds_per_day * 1000)
    current_date = start_sim_date + datetime.timedelta(days=days_passed)
    if current_date > end_sim_date:
        current_date = end_sim_date

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    window.fill(WHITE)

    # Draw destinations
    for name, (x, y) in destinations.items():
        pygame.draw.rect(window, GREEN, (x, y, 120, 60))
        # Add labels to destinations
        text = font.render(name, True, BLACK)
        text_rect = text.get_rect(center=(x + 60, y + 30))
        window.blit(text, text_rect)

    # Update and draw cars
    for car in cars:
        car.update(current_date)
        car.draw(window)

    # Display the current simulated date
    date_text = font.render(f'Current Date: {current_date.strftime("%b %d, %Y")}', True, BLACK)
    window.blit(date_text, (WIDTH // 2 - 100, 20))

    # Draw a timeline at the bottom
    pygame.draw.line(window, BLACK, (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50), 2)
    for i in range(total_sim_days):
        day_x = 50 + i * ((WIDTH - 100) / (total_sim_days - 1))
        pygame.draw.line(window, BLACK, (day_x, HEIGHT - 45), (day_x, HEIGHT - 55), 2)
        day_date = start_sim_date + datetime.timedelta(days=i)
        day_label = day_date.strftime('%d')
        label = font.render(day_label, True, BLACK)
        window.blit(label, (day_x - 10, HEIGHT - 40))

    # Update the display
    pygame.display.update()

# Clean up
pygame.quit()
sys.exit()
