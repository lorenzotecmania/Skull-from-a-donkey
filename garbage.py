import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADIUS = 150
FPS = 60

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock Animation")
clock = pygame.time.Clock()

def draw_clock_segments(surface, center, radius, angle_filled):
    """
    Draw the clock with green and black segments.
    angle_filled: angle in degrees that should be filled with black (0-360)
    """
    # Clear the area where we'll draw the clock
    pygame.draw.circle(surface, WHITE, center, radius + 5)
    
    if angle_filled <= 0:
        # Draw completely green circle
        pygame.draw.circle(surface, GREEN, center, radius)
    elif angle_filled >= 360:
        # Draw completely black circle
        pygame.draw.circle(surface, BLACK, center, radius)
    else:
        # Draw the green part first (full circle)
        pygame.draw.circle(surface, GREEN, center, radius)
        
        # Calculate points for the black segment
        # Start from 12 o'clock (top) and go clockwise
        points = [center]  # Center point
        
        # Add the starting point (12 o'clock)
        start_x = center[0]
        start_y = center[1] - radius
        points.append((start_x, start_y))
        
        # Add points along the arc
        num_points = max(3, int(angle_filled / 5))  # More points for smoother arc
        for i in range(num_points + 1):
            angle = (i * angle_filled / num_points) * math.pi / 180  # Convert to radians
            # Subtract pi/2 to start from 12 o'clock instead of 3 o'clock
            angle_adjusted = angle - math.pi / 2
            x = center[0] + radius * math.cos(angle_adjusted)
            y = center[1] + radius * math.sin(angle_adjusted)
            points.append((x, y))
        
        # Draw the black segment as a polygon
        if len(points) > 2:
            pygame.draw.polygon(surface, BLACK, points)

def main():
    running = True
    start_time = pygame.time.get_ticks()
    duration = 10000  # 10 seconds for complete animation
    
    while running:
        current_time = pygame.time.get_ticks()
        seconds = current_time - start_time
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset animation
                    start_time = current_time
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Calculate how much of the circle should be filled
        progress = min(seconds / duration, 1.0)  # 0.0 to 1.0
        angle_filled = progress * 360  # 0 to 360 degrees
        
        # Clear screen
        screen.fill(WHITE)
        
        # Draw the clock
        draw_clock_segments(screen, (CENTER_X, CENTER_Y), RADIUS, angle_filled)
        
        # Draw a border around the clock
        pygame.draw.circle(screen, BLACK, (CENTER_X, CENTER_Y), RADIUS + 2, 3)
        
        # Display instructions
        font = pygame.font.Font(None, 36)        
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()