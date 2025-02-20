import pygame
import random

pygame.init()

# Constants
DIFFICULTY = 2
GRID_SIZE = 3+DIFFICULTY*2

# Set up fullscreen mode and get screen resolution
screen_info = pygame.display.Info()
SCREEN_W, SCREEN_H = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)

# Calculate box size based on screen size
BOX_SIZE = min(SCREEN_W, SCREEN_H) // (GRID_SIZE + 1)
BOX_SPACE = BOX_SIZE - 6
BORDER_OFFSET = (min(SCREEN_W, SCREEN_H) - GRID_SIZE * BOX_SIZE) // 2

# SPRITES

def loadscale(file_path, size):
    """Loads an image and scales it to the specified size."""
    image = pygame.image.load(file_path)
    return pygame.transform.scale(image, (size,size))

player_sprite = loadscale('player_sprite.png', BOX_SPACE)
player_sprite_selected = loadscale('player_sprite_selected.png', BOX_SPACE)
crate_sprite = loadscale('crate_sprite.png', BOX_SPACE)
crate_sprite_selected = loadscale('crate_sprite_selected.png', BOX_SPACE)
blocker_sprite = loadscale('blocker_sprite.png', BOX_SPACE)
button_sprite = loadscale('button_sprite.png', BOX_SPACE)
start_button_sprite = loadscale('start_button_sprite.png', 2*BOX_SPACE)

pygame.mixer.init()
click_sound = pygame.mixer.Sound("click.wav")
click_sound.play()

# Border
border = pygame.Rect(
    BORDER_OFFSET + (SCREEN_W - min(SCREEN_W, SCREEN_H)) // 2,
    BORDER_OFFSET + (SCREEN_H - min(SCREEN_W, SCREEN_H)) // 2,
    GRID_SIZE * BOX_SIZE, GRID_SIZE * BOX_SIZE
)
border.inflate_ip(6,6)

# Create boxes (grid)
boxes = []
for i in range(GRID_SIZE):  # Outer loop
    for j in range(GRID_SIZE):  # Inner loop
        boxX = i * BOX_SIZE + BORDER_OFFSET + (SCREEN_W - min(SCREEN_W, SCREEN_H)) // 2
        boxY = j * BOX_SIZE + BORDER_OFFSET + (SCREEN_H - min(SCREEN_W, SCREEN_H)) // 2
        box = pygame.Rect(boxX, boxY, BOX_SIZE, BOX_SIZE)
        boxes.append(box)

# Receiver (spawn in the center square of the grid)
center_index = GRID_SIZE**2 // 2
center_box = boxes[center_index]
receiver = pygame.Rect(center_box.left + 3, center_box.top + 3, BOX_SPACE, BOX_SPACE)

#Butoons
button = pygame.Rect(center_box.left - BOX_SPACE,center_box.top, BOX_SPACE, BOX_SPACE)
start_button= pygame.Rect(center_box.left - BOX_SPACE,center_box.top,2*BOX_SPACE,2*BOX_SPACE)


player_selected = False
crate_selected = None
run = True
state = 'reset'
moves = 0

font = pygame.font.Font(None, 48)
intro_message = font.render("A demo based in ST4CK PUSHER from WTTG2", True, (255,255,255))

def is_within_3x3_area(player_rect, crate_rect):
    return abs(player_rect.centerx - crate_rect.centerx) <= BOX_SIZE and \
           abs(player_rect.centery - crate_rect.centery) <= BOX_SIZE

# Event handler
while run:
    screen.fill((0, 0, 0))

    if state == 'intro':
        screen.blit(start_button_sprite,(start_button.x,start_button.y))
        screen.blit(intro_message, (100, 100))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    state='game'
            if event.type == pygame.QUIT:
                    run = False


    if state == 'game':
        # Draw elements
        pygame.draw.rect(screen, (0, 0, 250), receiver)


        for crate in crates:
            if crate_selected:
                screen.blit(crate_sprite, (crate.x, crate.y))
                screen.blit(crate_sprite_selected, (crate_selected.x, crate_selected.y))
            else:
               screen.blit(crate_sprite, (crate.x, crate.y))

        for blocker in blockers:
            screen.blit(blocker_sprite, (blocker.x, blocker.y))

        for box in boxes:
            pygame.draw.rect(screen, "green", box, 3)

        pygame.draw.rect(screen, (0, 250, 0), border, 6)

        if player_selected:
            screen.blit(player_sprite_selected, (player.x, player.y))
        else:
            screen.blit(player_sprite, (player.x, player.y))

        if h1 == 0: state = 'won'
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Check if any crate within the 3x3 area is clicked
                crate_clicked = False
                for crate in crates:
                    if crate.collidepoint(event.pos) and is_within_3x3_area(player, crate) and player_selected == False and crate_selected == None:
                        crate_selected = crate
                        crate_clicked = True  # Mark that a crate was clicked

                # If no crate was clicked, check for movement
                if crate_selected and not crate_clicked and border.collidepoint(event.pos):
                    for box in boxes:
                        if box.collidepoint(event.pos):
                            if not is_within_3x3_area(player, box):
                                break
                            if player.colliderect(box):
                                break
                            if any(blocker.colliderect(box) for blocker in blockers):
                                break
                            if any(crate.colliderect(box) for crate in crates):
                                break
                            if receiver.colliderect(box):
                                crates.remove(crate_selected)
                                click_sound.play()
                                h1=h1-1
                            crate_selected.center = box.center
                            moves=moves+1
                            break
                    crate_selected = None

                # Handle player movement
                if player.collidepoint(event.pos):
                    player_selected = not player_selected

                elif player_selected and border.collidepoint(event.pos):
                    for box in boxes:
                        if box.collidepoint(event.pos):
                            if receiver.colliderect(box):
                                break
                            if any(crate.colliderect(box) for crate in crates):
                                break
                            if any(blocker.colliderect(box) for blocker in blockers):
                                break
                            player.center = box.center
                            moves=moves+1
                            break
                    player_selected = False

        screen.blit(timer_text, (100, 200))
        move_counter = font.render(str(moves), True, (255, 255, 255))
        screen.blit(move_counter, (100,100))
        

    if state == 'won':

        screen.blit(button_sprite, (button.x, button.y))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    state = 'reset'
            if event.type == pygame.QUIT:
                    run = False

    if state == 'reset':

        available_boxes = [box for box in boxes if box != center_box]
        player_box = random.choice(available_boxes)
        player = pygame.Rect(player_box.left + 3, player_box.top + 3, BOX_SPACE, BOX_SPACE)

        # Crates
        available_boxes = [box for box in boxes if box != center_box and box != player_box]
        h1 = int(1.5*2**DIFFICULTY)
        crates = []
        for h in range(h1):

            crate_box = random.choice(available_boxes)
            crate = pygame.Rect(crate_box.left + 3, crate_box.top + 3, BOX_SPACE, BOX_SPACE)
            crates.append(crate)
            available_boxes.remove(crate_box)


        blockers = []
        for h in range(h1):
            blocker_box = random.choice(available_boxes)
            blocker = pygame.Rect(blocker_box.left + 3, blocker_box.top + 3, BOX_SPACE, BOX_SPACE)
            blockers.append(blocker)
            available_boxes.remove(blocker_box)
        
        moves = 0

        state = 'intro'


    #COUNTER
    if moves == 0: start_ticks = pygame.time.get_ticks()
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000 # convert to seconds
    time_left = float(seconds)
    timer_text = font.render(f"{time_left}", True, (255, 255, 255))
    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()