import pygame
import sys
import math
import random
import time
from enum import Enum

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Colors - Pixel art palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 30, 30)
GREEN = (40, 180, 40)
YELLOW = (255, 220, 0)
BLUE = (30, 100, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (60, 60, 60)
ROAD_GRAY = (80, 80, 80)
YELLOW_LINE = (255, 255, 100)
ORANGE = (255, 140, 0)
LIGHT_BLUE = (120, 180, 255)
EMERGENCY_RED = (255, 50, 50)
DARK_GREEN = (20, 120, 20)
BROWN = (139, 69, 19)
CONCRETE = (169, 169, 169)

class TrafficLightState(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

class VehicleType(Enum):
    CAR = 1
    AMBULANCE = 2
    TRUCK = 3
    POLICE = 4

def create_car_sprite():
    """Create a pixelated car sprite"""
    surface = pygame.Surface((32, 16), pygame.SRCALPHA)
    # Car body
    pygame.draw.rect(surface, BLUE, (4, 2, 24, 12))
    # Car roof
    pygame.draw.rect(surface, (50, 120, 220), (8, 4, 16, 8))
    # Windows
    pygame.draw.rect(surface, LIGHT_BLUE, (10, 5, 4, 6))
    pygame.draw.rect(surface, LIGHT_BLUE, (18, 5, 4, 6))
    # Wheels
    pygame.draw.circle(surface, BLACK, (8, 14), 3)
    pygame.draw.circle(surface, BLACK, (24, 14), 3)
    pygame.draw.circle(surface, GRAY, (8, 14), 2)
    pygame.draw.circle(surface, GRAY, (24, 14), 2)
    # Headlights
    pygame.draw.rect(surface, YELLOW, (28, 6, 2, 4))
    # Taillights
    pygame.draw.rect(surface, RED, (2, 6, 2, 4))
    return surface

def create_ambulance_sprite():
    """Create a pixelated ambulance sprite"""
    surface = pygame.Surface((40, 20), pygame.SRCALPHA)
    # Ambulance body
    pygame.draw.rect(surface, WHITE, (4, 2, 32, 16))
    # Red cross
    pygame.draw.rect(surface, RED, (16, 6, 8, 2))
    pygame.draw.rect(surface, RED, (19, 4, 2, 6))
    # Windows
    pygame.draw.rect(surface, LIGHT_BLUE, (8, 4, 6, 8))
    pygame.draw.rect(surface, LIGHT_BLUE, (26, 4, 6, 8))
    # Wheels
    pygame.draw.circle(surface, BLACK, (10, 18), 4)
    pygame.draw.circle(surface, BLACK, (30, 18), 4)
    pygame.draw.circle(surface, GRAY, (10, 18), 3)
    pygame.draw.circle(surface, GRAY, (30, 18), 3)
    # Emergency lights
    pygame.draw.rect(surface, RED, (4, 2, 4, 3))
    pygame.draw.rect(surface, BLUE, (32, 2, 4, 3))
    # Headlights
    pygame.draw.rect(surface, YELLOW, (36, 8, 2, 4))
    return surface

def create_truck_sprite():
    """Create a pixelated truck sprite"""
    surface = pygame.Surface((48, 24), pygame.SRCALPHA)
    # Truck cab
    pygame.draw.rect(surface, (150, 75, 0), (4, 4, 16, 16))
    # Truck trailer
    pygame.draw.rect(surface, GRAY, (20, 2, 24, 20))
    # Windows
    pygame.draw.rect(surface, LIGHT_BLUE, (6, 6, 6, 8))
    # Wheels
    pygame.draw.circle(surface, BLACK, (12, 22), 4)
    pygame.draw.circle(surface, BLACK, (28, 22), 4)
    pygame.draw.circle(surface, BLACK, (40, 22), 4)
    pygame.draw.circle(surface, DARK_GRAY, (12, 22), 3)
    pygame.draw.circle(surface, DARK_GRAY, (28, 22), 3)
    pygame.draw.circle(surface, DARK_GRAY, (40, 22), 3)
    # Headlights
    pygame.draw.rect(surface, YELLOW, (44, 10, 2, 4))
    return surface

def create_police_sprite():
    """Create a pixelated police car sprite"""
    surface = pygame.Surface((34, 18), pygame.SRCALPHA)
    # Police car body
    pygame.draw.rect(surface, (0, 0, 100), (4, 2, 26, 14))
    # Police markings
    pygame.draw.rect(surface, WHITE, (6, 4, 22, 4))
    pygame.draw.rect(surface, WHITE, (6, 10, 22, 4))
    # Windows
    pygame.draw.rect(surface, LIGHT_BLUE, (10, 5, 4, 6))
    pygame.draw.rect(surface, LIGHT_BLUE, (20, 5, 4, 6))
    # Wheels
    pygame.draw.circle(surface, BLACK, (8, 16), 3)
    pygame.draw.circle(surface, BLACK, (26, 16), 3)
    pygame.draw.circle(surface, GRAY, (8, 16), 2)
    pygame.draw.circle(surface, GRAY, (26, 16), 2)
    # Light bar
    pygame.draw.rect(surface, RED, (12, 2, 4, 2))
    pygame.draw.rect(surface, BLUE, (18, 2, 4, 2))
    # Headlights
    pygame.draw.rect(surface, YELLOW, (30, 7, 2, 4))
    return surface

def rotate_sprite(surface, angle):
    """Rotate sprite for different directions"""
    return pygame.transform.rotate(surface, angle)

class Vehicle:
    def __init__(self, x, y, direction, vehicle_type=VehicleType.CAR):
        self.x = x
        self.y = y
        self.direction = direction  # 0=right, 1=down, 2=left, 3=up
        self.vehicle_type = vehicle_type
        
        # Set speed based on vehicle type
        if vehicle_type == VehicleType.TRUCK:
            self.speed = 1.5
        elif vehicle_type == VehicleType.AMBULANCE:
            self.speed = 2.5
        elif vehicle_type == VehicleType.POLICE:
            self.speed = 3
        else:
            self.speed = 2
            
        self.original_speed = self.speed
        self.stopped = False
        self.emergency_mode = False
        
        # Create sprite based on vehicle type
        if vehicle_type == VehicleType.CAR:
            self.base_sprite = create_car_sprite()
            self.width, self.height = 32, 16
        elif vehicle_type == VehicleType.AMBULANCE:
            self.base_sprite = create_ambulance_sprite()
            self.width, self.height = 40, 20
        elif vehicle_type == VehicleType.TRUCK:
            self.base_sprite = create_truck_sprite()
            self.width, self.height = 48, 24
        elif vehicle_type == VehicleType.POLICE:
            self.base_sprite = create_police_sprite()
            self.width, self.height = 34, 18
            
        # Rotate sprite based on direction
        rotation_angles = {0: 0, 1: -90, 2: 180, 3: 90}
        self.sprite = rotate_sprite(self.base_sprite, rotation_angles[direction])
        
        # Emergency lights animation
        self.light_timer = 0
        self.siren_radius = 0
        
    def update(self, traffic_lights, emergency_active):
        if self.vehicle_type in [VehicleType.AMBULANCE, VehicleType.POLICE]:
            self.emergency_mode = emergency_active
            
        # Check if vehicle should stop at traffic light
        should_stop = self.check_traffic_light_collision(traffic_lights)
        
        if should_stop and not self.emergency_mode:
            self.speed = 0
            self.stopped = True
        else:
            speed_multiplier = 1.5 if self.emergency_mode else 1
            self.speed = self.original_speed * speed_multiplier
            self.stopped = False
            
        # Move vehicle
        if self.direction == 0:  # Right
            self.x += self.speed
        elif self.direction == 1:  # Down
            self.y += self.speed
        elif self.direction == 2:  # Left
            self.x -= self.speed
        elif self.direction == 3:  # Up
            self.y -= self.speed
            
        # Update emergency effects
        self.light_timer += 1
        if self.emergency_mode:
            self.siren_radius = min(self.siren_radius + 2, 60)
        else:
            self.siren_radius = max(self.siren_radius - 3, 0)
            
    def check_traffic_light_collision(self, traffic_lights):
        for light in traffic_lights:
            approach_distance = 80
            
            if self.direction == 0:  # Moving right
                if (light.x - approach_distance < self.x < light.x and 
                    abs(self.y - light.y) < 30):
                    return light.get_state_for_direction(self.direction) == TrafficLightState.RED
                    
            elif self.direction == 1:  # Moving down
                if (light.y - approach_distance < self.y < light.y and 
                    abs(self.x - light.x) < 30):
                    return light.get_state_for_direction(self.direction) == TrafficLightState.RED
                    
            elif self.direction == 2:  # Moving left
                if (light.x < self.x < light.x + approach_distance and 
                    abs(self.y - light.y) < 30):
                    return light.get_state_for_direction(self.direction) == TrafficLightState.RED
                    
            elif self.direction == 3:  # Moving up
                if (light.y < self.y < light.y + approach_distance and 
                    abs(self.x - light.x) < 30):
                    return light.get_state_for_direction(self.direction) == TrafficLightState.RED
                    
        return False
        
    def draw(self, screen):
        # Draw siren effect for emergency vehicles
        if self.siren_radius > 0:
            # Pulsing siren effect
            alpha = int(100 * (1 - self.siren_radius / 60))
            siren_surface = pygame.Surface((self.siren_radius * 2, self.siren_radius * 2), pygame.SRCALPHA)
            
            color = RED if (self.light_timer // 15) % 2 else BLUE
            pygame.draw.circle(siren_surface, (*color[:3], alpha), 
                             (self.siren_radius, self.siren_radius), self.siren_radius)
            
            screen.blit(siren_surface, 
                       (self.x - self.siren_radius + self.width//2, 
                        self.y - self.siren_radius + self.height//2))
        
        # Draw vehicle sprite
        screen.blit(self.sprite, (int(self.x), int(self.y)))
        
        # Draw flashing emergency lights
        if self.emergency_mode and self.vehicle_type in [VehicleType.AMBULANCE, VehicleType.POLICE]:
            if (self.light_timer // 10) % 2:
                # Front emergency lights
                if self.direction == 0:  # Right
                    pygame.draw.circle(screen, RED, (int(self.x + self.width - 5), int(self.y + 5)), 4)
                    pygame.draw.circle(screen, BLUE, (int(self.x + self.width - 5), int(self.y + self.height - 5)), 4)
                elif self.direction == 1:  # Down
                    pygame.draw.circle(screen, RED, (int(self.x + 5), int(self.y + self.height - 5)), 4)
                    pygame.draw.circle(screen, BLUE, (int(self.x + self.width - 5), int(self.y + self.height - 5)), 4)
                elif self.direction == 2:  # Left
                    pygame.draw.circle(screen, RED, (int(self.x + 5), int(self.y + 5)), 4)
                    pygame.draw.circle(screen, BLUE, (int(self.x + 5), int(self.y + self.height - 5)), 4)
                else:  # Up
                    pygame.draw.circle(screen, RED, (int(self.x + 5), int(self.y + 5)), 4)
                    pygame.draw.circle(screen, BLUE, (int(self.x + self.width - 5), int(self.y + 5)), 4)
                    
    def is_off_screen(self):
        return (self.x < -100 or self.x > SCREEN_WIDTH + 100 or 
                self.y < -100 or self.y > SCREEN_HEIGHT + 100)

class TrafficLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ns_state = TrafficLightState.GREEN
        self.ew_state = TrafficLightState.RED
        self.emergency_mode = False
        self.last_change = pygame.time.get_ticks()
        self.change_interval = 4000
        self.emergency_override = False
        
    def update(self, emergency_detected, ambulance_direction=None):
        current_time = pygame.time.get_ticks()
        
        if emergency_detected and not self.emergency_override:
            self.emergency_mode = True
            self.emergency_override = True
            self.ns_state = TrafficLightState.RED
            self.ew_state = TrafficLightState.RED
            return
            
        if self.emergency_mode and not emergency_detected:
            self.emergency_mode = False
            self.emergency_override = False
            self.last_change = current_time
            
        if not self.emergency_mode and current_time - self.last_change > self.change_interval:
            if self.ns_state == TrafficLightState.GREEN:
                self.ns_state = TrafficLightState.YELLOW
                self.change_interval = 1500
            elif self.ns_state == TrafficLightState.YELLOW:
                self.ns_state = TrafficLightState.RED
                self.ew_state = TrafficLightState.GREEN
                self.change_interval = 4000
            elif self.ew_state == TrafficLightState.GREEN:
                self.ew_state = TrafficLightState.YELLOW
                self.change_interval = 1500
            elif self.ew_state == TrafficLightState.YELLOW:
                self.ew_state = TrafficLightState.RED
                self.ns_state = TrafficLightState.GREEN
                self.change_interval = 4000
                
            self.last_change = current_time
            
    def get_state_for_direction(self, direction):
        if direction in [0, 2]:  # East-West
            return self.ew_state
        else:  # North-South
            return self.ns_state
            
    def clear_for_ambulance(self, ambulance_direction):
        if ambulance_direction in [0, 2]:  # East-West
            self.ew_state = TrafficLightState.GREEN
            self.ns_state = TrafficLightState.RED
        else:  # North-South
            self.ns_state = TrafficLightState.GREEN
            self.ew_state = TrafficLightState.RED
            
    def draw(self, screen):
        # Draw traffic light housing - pixelated style
        # Main post
        pygame.draw.rect(screen, DARK_GRAY, (self.x - 8, self.y - 15, 16, 80))
        
        # Traffic light boxes
        # North-South lights
        pygame.draw.rect(screen, BLACK, (self.x - 12, self.y - 35, 24, 15))
        pygame.draw.rect(screen, GRAY, (self.x - 10, self.y - 33, 20, 11))
        
        # East-West lights  
        pygame.draw.rect(screen, BLACK, (self.x + 15, self.y - 12, 15, 24))
        pygame.draw.rect(screen, GRAY, (self.x + 17, self.y - 10, 11, 20))
        
        # NS light colors
        ns_colors = {
            TrafficLightState.RED: RED,
            TrafficLightState.YELLOW: YELLOW,
            TrafficLightState.GREEN: GREEN
        }
        pygame.draw.circle(screen, ns_colors[self.ns_state], (self.x, self.y - 27), 6)
        pygame.draw.circle(screen, (40, 40, 40), (self.x, self.y - 27), 7, 2)
        
        # EW light colors
        ew_colors = {
            TrafficLightState.RED: RED,
            TrafficLightState.YELLOW: YELLOW,
            TrafficLightState.GREEN: GREEN
        }
        pygame.draw.circle(screen, ew_colors[self.ew_state], (self.x + 22, self.y), 6)
        pygame.draw.circle(screen, (40, 40, 40), (self.x + 22, self.y), 7, 2)
        
        # Emergency mode indicator
        if self.emergency_mode:
            # Flashing emergency beacon
            if (pygame.time.get_ticks() // 200) % 2:
                pygame.draw.circle(screen, EMERGENCY_RED, (self.x, self.y + 35), 8)
                pygame.draw.circle(screen, WHITE, (self.x, self.y + 35), 4)

def draw_road_network(screen):
    """Draw pixelated road network with details"""
    # Main horizontal roads
    road_y_positions = [200, 350, 500, 650]
    for y in road_y_positions:
        # Road surface
        pygame.draw.rect(screen, ROAD_GRAY, (0, y - 40, SCREEN_WIDTH, 80))
        # Road edges
        pygame.draw.rect(screen, WHITE, (0, y - 40, SCREEN_WIDTH, 4))
        pygame.draw.rect(screen, WHITE, (0, y + 36, SCREEN_WIDTH, 4))
        # Center line
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.rect(screen, YELLOW_LINE, (x, y - 2, 20, 4))
    
    # Main vertical roads
    road_x_positions = [300, 500, 700, 900]
    for x in road_x_positions:
        # Road surface
        pygame.draw.rect(screen, ROAD_GRAY, (x - 40, 0, 80, SCREEN_HEIGHT))
        # Road edges
        pygame.draw.rect(screen, WHITE, (x - 40, 0, 4, SCREEN_HEIGHT))
        pygame.draw.rect(screen, WHITE, (x + 36, 0, 4, SCREEN_HEIGHT))
        # Center line
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(screen, YELLOW_LINE, (x - 2, y, 4, 20))
    
    # Draw intersections
    intersections = []
    for x in road_x_positions:
        for y in road_y_positions:
            intersections.append((x, y))
            # Intersection surface
            pygame.draw.rect(screen, ROAD_GRAY, (x - 40, y - 40, 80, 80))
            
    # Add sidewalks and buildings (pixelated)
    # Buildings
    building_positions = [
        (50, 50, 180, 120), (1050, 50, 200, 120),
        (50, 750, 180, 120), (1050, 750, 200, 120)
    ]
    
    for bx, by, bw, bh in building_positions:
        # Building base
        pygame.draw.rect(screen, GRAY, (bx, by, bw, bh))
        # Windows
        for wx in range(bx + 20, bx + bw - 20, 30):
            for wy in range(by + 20, by + bh - 20, 25):
                pygame.draw.rect(screen, LIGHT_BLUE, (wx, wy, 12, 15))
                pygame.draw.rect(screen, BLACK, (wx, wy, 12, 15), 2)
    
    # Sidewalks
    pygame.draw.rect(screen, CONCRETE, (0, 0, SCREEN_WIDTH, 160))  # Top
    pygame.draw.rect(screen, CONCRETE, (0, 690, SCREEN_WIDTH, 210))  # Bottom
    pygame.draw.rect(screen, CONCRETE, (0, 160, 260, 530))  # Left
    pygame.draw.rect(screen, CONCRETE, (940, 160, 460, 530))  # Right

class EmergencySystem:
    def __init__(self):
        self.emergency_active = False
        self.ambulance_detected = False
        self.detection_radius = 200
        self.alert_start_time = 0
        self.cleared_intersections = set()
        self.siren_sound_radius = 0
        
    def detect_ambulance(self, vehicles, traffic_lights):
        emergency_vehicles = [v for v in vehicles if v.vehicle_type in [VehicleType.AMBULANCE, VehicleType.POLICE]]
        
        if not emergency_vehicles and self.emergency_active:
            self.emergency_active = False
            self.cleared_intersections.clear()
            return False, None
            
        closest_emergency = None
        min_distance = float('inf')
        
        for vehicle in emergency_vehicles:
            for i, light in enumerate(traffic_lights):
                distance = math.sqrt((vehicle.x - light.x)**2 + (vehicle.y - light.y)**2)
                if distance < self.detection_radius:
                    if not self.emergency_active:
                        self.emergency_active = True
                        self.alert_start_time = pygame.time.get_ticks()
                        
                    if distance < min_distance:
                        min_distance = distance
                        closest_emergency = vehicle
                        
                    if i not in self.cleared_intersections:
                        light.clear_for_ambulance(vehicle.direction)
                        self.cleared_intersections.add(i)
                        
        return self.emergency_active, closest_emergency
        
    def draw_alerts(self, screen, font):
        if self.emergency_active:
            # Animated emergency banner
            banner_height = 70
            flash_intensity = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 255
            banner_color = (int(flash_intensity), 0, 0)
            
            pygame.draw.rect(screen, banner_color, (0, 0, SCREEN_WIDTH, banner_height))
            pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, banner_height), 4)
            
            # Emergency text with pixel effect
            text = "🚨 EMERGENCY VEHICLE DETECTED - CLEARING TRAFFIC 🚨"
            text_surface = font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, banner_height//2))
            screen.blit(text_surface, text_rect)
            
            # Side warning lights
            light_size = 20
            for i in range(0, SCREEN_HEIGHT, 60):
                color = RED if (pygame.time.get_ticks() // 300 + i // 60) % 2 else BLUE
                pygame.draw.rect(screen, color, (0, i, light_size, light_size))
                pygame.draw.rect(screen, color, (SCREEN_WIDTH - light_size, i, light_size, light_size))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixelated Ambulance Traffic System")
    clock = pygame.time.Clock()
    
    # Pixel-style fonts
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Create traffic lights at intersections
    traffic_lights = []
    road_x_positions = [300, 500, 700, 900]
    road_y_positions = [200, 350, 500, 650]
    
    for x in road_x_positions:
        for y in road_y_positions:
            traffic_lights.append(TrafficLight(x, y))
    
    vehicles = []
    emergency_system = EmergencySystem()
    
    # Spawn timers
    last_regular_spawn = pygame.time.get_ticks()
    last_emergency_spawn = pygame.time.get_ticks()
    regular_spawn_interval = 3000
    
    # Statistics
    vehicles_cleared = 0
    emergency_activations = 0
    total_spawned = 0
    
    running = True
    paused = False
    
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_a:
                    # Spawn ambulance
                    spawn_side = random.randint(0, 3)
                    if spawn_side == 0:  # Left
                        ambulance = Vehicle(50, random.choice(road_y_positions), 0, VehicleType.AMBULANCE)
                    elif spawn_side == 1:  # Top
                        ambulance = Vehicle(random.choice(road_x_positions), 50, 1, VehicleType.AMBULANCE)
                    elif spawn_side == 2:  # Right
                        ambulance = Vehicle(SCREEN_WIDTH - 50, random.choice(road_y_positions), 2, VehicleType.AMBULANCE)
                    else:  # Bottom
                        ambulance = Vehicle(random.choice(road_x_positions), SCREEN_HEIGHT - 50, 3, VehicleType.AMBULANCE)
                    vehicles.append(ambulance)
                    total_spawned += 1
                elif event.key == pygame.K_p:
                    # Spawn police
                    spawn_side = random.randint(0, 3)
                    if spawn_side == 0:  # Left
                        police = Vehicle(50, random.choice(road_y_positions), 0, VehicleType.POLICE)
                    elif spawn_side == 1:  # Top
                        police = Vehicle(random.choice(road_x_positions), 50, 1, VehicleType.POLICE)
                    elif spawn_side == 2:  # Right
                        police = Vehicle(SCREEN_WIDTH - 50, random.choice(road_y_positions), 2, VehicleType.POLICE)
                    else:  # Bottom
                        police = Vehicle(random.choice(road_x_positions), SCREEN_HEIGHT - 50, 3, VehicleType.POLICE)
                    vehicles.append(police)
                    total_spawned += 1
                elif event.key == pygame.K_c:
                    vehicles.clear()
                elif event.key == pygame.K_r:
                    vehicles_cleared = 0
                    emergency_activations = 0
                    total_spawned = 0
                    
        if not paused:
            # Spawn regular vehicles
            if current_time - last_regular_spawn > regular_spawn_interval:
                vehicle_types = [VehicleType.CAR, VehicleType.CAR, VehicleType.CAR, VehicleType.TRUCK]
                vehicle_type = random.choice(vehicle_types)
                
                spawn_side = random.randint(0, 3)
                if spawn_side == 0:  # Left
                    new_vehicle = Vehicle(0, random.choice(road_y_positions), 0, vehicle_type)
                elif spawn_side == 1:  # Top  
                    new_vehicle = Vehicle(random.choice(road_x_positions), 0, 1, vehicle_type)
                elif spawn_side == 2:  # Right
                    new_vehicle = Vehicle(SCREEN_WIDTH, random.choice(road_y_positions), 2, vehicle_type)
                else:  # Bottom
                    new_vehicle = Vehicle(random.choice(road_x_positions), SCREEN_HEIGHT, 3, vehicle_type)
                    
                vehicles.append(new_vehicle)
                total_spawned += 1
                last_regular_spawn = current_time
                
            # Update emergency system
            emergency_active, closest_emergency = emergency_system.detect_ambulance(vehicles, traffic_lights)
            
            if emergency_active and not emergency_system.ambulance_detected:
                emergency_activations += 1
                emergency_system.ambulance_detected = True
            elif not emergency_active:
                emergency_system.ambulance_detected = False
                
            # Update traffic lights
            for light in traffic_lights:
                ambulance_direction = closest_emergency.direction if closest_emergency else None
                light.update(emergency_active, ambulance_direction)
                
            # Update vehicles
            for vehicle in vehicles[:]:
                vehicle.update(traffic_lights, emergency_active and 
                             vehicle.vehicle_type in [VehicleType.AMBULANCE, VehicleType.POLICE])
                if vehicle.is_off_screen():
                    vehicles.remove(vehicle)
                    if vehicle.vehicle_type in [VehicleType.CAR, VehicleType.TRUCK]:
                        vehicles_cleared += 1
        
        # Draw everything
        screen.fill(DARK_GREEN)  # Grass background
        
        # Draw road network
        draw_road_network(screen)
        
        # Draw traffic lights
        for light in traffic_lights:
            light.draw(screen)
            
        # Draw vehicles (sorted by y-position for proper layering)
        vehicles_sorted = sorted(vehicles, key=lambda v: v.y)
        for vehicle in vehicles_sorted:
            vehicle.draw(screen)
            
        # Draw emergency alerts
        emergency_system.draw_alerts(screen, font)
        
        # Draw pixelated UI panel
        ui_panel_height = 200
        pygame.draw.rect(screen, (20, 20, 20), (0, SCREEN_HEIGHT - ui_panel_height, SCREEN_WIDTH, ui_panel_height))
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - ui_panel_height, SCREEN_WIDTH, 4))
        
        # UI Information with pixel styling
        info_texts = [
            f"🚗 Total Vehicles: {len(vehicles)}",
            f"🚑 Emergency Active: {'YES' if emergency_active else 'NO'}",
            f"✅ Vehicles Cleared: {vehicles_cleared}",
            f"🚨 Emergency Calls: {emergency_activations}",
            f"📊 Total Spawned: {total_spawned}",
        ]
        
        controls_texts = [
            "CONTROLS:",
            "SPACE - Pause/Resume",
            "A - Spawn Ambulance 🚑",
            "P - Spawn Police 👮",
            "C - Clear All Vehicles",
            "R - Reset Statistics"
        ]
        
        # Left column - Statistics
        y_offset = SCREEN_HEIGHT - ui_panel_height + 10
        for i, text in enumerate(info_texts):
            color = EMERGENCY_RED if "Emergency Active: YES" in text else WHITE
            if "Emergency Active" in text and emergency_active:
                # Flashing effect for active emergency
                if (pygame.time.get_ticks() // 500) % 2:
                    color = YELLOW
            rendered_text = small_font.render(text, True, color)
            screen.blit(rendered_text, (20, y_offset))
            y_offset += 25
            
        # Right column - Controls
        y_offset = SCREEN_HEIGHT - ui_panel_height + 10
        for text in controls_texts:
            color = YELLOW if text == "CONTROLS:" else LIGHT_BLUE
            rendered_text = small_font.render(text, True, color)
            screen.blit(rendered_text, (SCREEN_WIDTH // 2 + 50, y_offset))
            y_offset += 25
            
        # Draw mini-map in corner
        minimap_size = 150
        minimap_x = SCREEN_WIDTH - minimap_size - 20
        minimap_y = SCREEN_HEIGHT - ui_panel_height - minimap_size - 20
        
        # Minimap background
        pygame.draw.rect(screen, (40, 40, 40), (minimap_x, minimap_y, minimap_size, minimap_size))
        pygame.draw.rect(screen, WHITE, (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Minimap title
        minimap_title = small_font.render("TRAFFIC MAP", True, WHITE)
        screen.blit(minimap_title, (minimap_x + 5, minimap_y - 25))
        
        # Scale factor for minimap
        scale_x = minimap_size / SCREEN_WIDTH
        scale_y = minimap_size / SCREEN_HEIGHT
        
        # Draw roads on minimap
        for x in road_x_positions:
            mini_x = int(x * scale_x) + minimap_x
            pygame.draw.line(screen, ROAD_GRAY, (mini_x, minimap_y), (mini_x, minimap_y + minimap_size), 2)
        
        for y in road_y_positions:
            mini_y = int(y * scale_y) + minimap_y
            pygame.draw.line(screen, ROAD_GRAY, (minimap_x, mini_y), (minimap_x + minimap_size, mini_y), 2)
        
        # Draw vehicles on minimap
        for vehicle in vehicles:
            mini_x = int(vehicle.x * scale_x) + minimap_x
            mini_y = int(vehicle.y * scale_y) + minimap_y
            
            if mini_x >= minimap_x and mini_x <= minimap_x + minimap_size and mini_y >= minimap_y and mini_y <= minimap_y + minimap_size:
                if vehicle.vehicle_type == VehicleType.AMBULANCE:
                    color = RED if vehicle.emergency_mode else WHITE
                elif vehicle.vehicle_type == VehicleType.POLICE:
                    color = BLUE
                elif vehicle.vehicle_type == VehicleType.TRUCK:
                    color = ORANGE
                else:
                    color = GREEN
                    
                pygame.draw.circle(screen, color, (mini_x, mini_y), 2)
        
        # Draw traffic lights on minimap
        for light in traffic_lights:
            mini_x = int(light.x * scale_x) + minimap_x
            mini_y = int(light.y * scale_y) + minimap_y
            
            if light.emergency_mode:
                color = EMERGENCY_RED
            else:
                color = YELLOW
            pygame.draw.circle(screen, color, (mini_x, mini_y), 3)
            
        # Performance indicator
        fps_text = small_font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
        screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))
        
        # Draw pause overlay
        if paused:
            # Semi-transparent overlay
            pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            pause_overlay.set_alpha(128)
            pause_overlay.fill(BLACK)
            screen.blit(pause_overlay, (0, 0))
            
            # Pause text with pixelated border
            pause_text = font.render("GAME PAUSED", True, YELLOW)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            
            # Draw pixelated border
            border_size = 10
            pygame.draw.rect(screen, WHITE, pause_rect.inflate(border_size * 2, border_size * 2))
            pygame.draw.rect(screen, BLACK, pause_rect.inflate(border_size, border_size))
            
            screen.blit(pause_text, pause_rect)
            
            # Instructions
            instruction_text = small_font.render("Press SPACE to continue", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(instruction_text, instruction_rect)
            
        # Emergency vehicle counter in top-left
        emergency_count = len([v for v in vehicles if v.vehicle_type in [VehicleType.AMBULANCE, VehicleType.POLICE]])
        if emergency_count > 0:
            emergency_text = font.render(f"🚨 Emergency Vehicles: {emergency_count}", True, EMERGENCY_RED)
            pygame.draw.rect(screen, BLACK, (10, 80, emergency_text.get_width() + 20, 40))
            pygame.draw.rect(screen, EMERGENCY_RED, (10, 80, emergency_text.get_width() + 20, 40), 3)
            screen.blit(emergency_text, (20, 90))
            
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()