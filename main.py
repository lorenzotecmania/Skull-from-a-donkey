import pygame
import random
import math

__version__ = "0.3"

#32x

pygame.init()

DIFFICULTY = 2


screen_info = pygame.display.Info()
S_W, S_H = screen_info.current_w, screen_info.current_h
#S_W, S_H = (screen_info.current_w/100)*55, (screen_info.current_h/100)*55
screen = pygame.display.set_mode((S_W, S_H),)

def ls(file_path, size1, size2):
    image = pygame.image.load(file_path)
    return pygame.transform.scale(image, (size1,size2))

def is_within_3x3_area(player_rect, crate_rect):
    return abs(player_rect.centerx - crate_rect.centerx) <= BOX_SIZE and \
           abs(player_rect.centery - crate_rect.centery) <= BOX_SIZE

def sort_leaderboard(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            header = lines[0].strip()
            score_lines = lines[1:]
            
            # Parse scores
            scores = []
            for line in score_lines:
                line = line.strip()
                if line:
                    try:
                        name, details = line.split('-')
                        time, moves = details.split('  ')
                        scores.append((name, float(time), int(moves)))
                    except ValueError as e:
                        print(f"Error parsing line '{line}': {e}")
            
            best_scores = {}
            for name, time, moves in scores:
                if name not in best_scores or time < best_scores[name][0]:
                    best_scores[name] = (time, moves)

            # Sort scores by time (ascending)
            sorted_scores = sorted([(name, t, m) for name, (t, m) in best_scores.items()], key=lambda x: x[1])
            
            # Prepare content to write
            output_lines = [header + "\n"]
            for name, time, moves in sorted_scores:
                output_lines.append(f"{name}-{time:.3f}  {moves}\n")
            
            # Write back to file
            with open(filename, "w") as outfile:
                outfile.writelines(output_lines)
    
    except Exception as e:
        print(f"Error sorting leaderboard: {e}")
        import traceback
        traceback.print_exc()

def draw_clock_segments(surface, center, radius, angle_filled):
    """
    Draw the clock with green and black segments.
    angle_filled: angle in degrees that should be filled with black (0-360)
    """
    if angle_filled <= 0:
        # Draw completely green circle
        pygame.draw.circle(surface, N_GREEN, center, radius)
    elif angle_filled >= 360:
        # Draw completely black circle
        pygame.draw.circle(surface, (0,0,0), center, radius)
    else:
        # Draw the green part first (full circle)
        pygame.draw.circle(surface, N_GREEN, center, radius)
        
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
            pygame.draw.polygon(surface, (0,0,0), points)
def handle_intro():
    global turn
    global state
    global run
    global DIFFICULTY
    # Handle intro screen events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                state='game'
            if settings_button.collidepoint(event.pos):
                state='settings'
            if leaderboard_b.collidepoint(event.pos):
                state='won'
            if how_to_play_button.collidepoint(event.pos):
                state='how_to_play'
            if vs_b.collidepoint(event.pos):
                turn = 1
                state='tela_preta'
            if first_button.collidepoint(event.pos):
                DIFFICULTY=1
                state='reset'
            if second_button.collidepoint(event.pos):
                DIFFICULTY=2
                state='reset'
            if third_button.collidepoint(event.pos):
                DIFFICULTY=3
                state='reset'

        if event.type == pygame.QUIT:
            run = False

def handle_settings():
    global state
    global run
    global hardcore_mode
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                state = 'intro'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                state = 'reset'
            if hardcore_b.collidepoint(event.pos):
                hardcore_mode = not hardcore_mode
   

        if any(pygame.mouse.get_pressed()) and slider.collidepoint(pygame.mouse.get_pos()):

            slider_thing.x = pygame.mouse.get_pos() [0] - SMOL_BOX/4.6
            click_sound.set_volume(0.5)
            click_sound.play()

            if 1.25*SMOL_BOX > pygame.mouse.get_pos()[0]:
                slider_thing.x = 1.03*SMOL_BOX
            if pygame.mouse.get_pos()[0] > 5.40*BOX_SPACE:
                slider_thing.x = 5.35*BOX_SPACE

def handle_score():
    global state
    global run
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                state = 'intro'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                state = 'reset'

        if event.type == pygame.QUIT:
                run = False
"""""
def handle_game(not working rn):
    global state
    global run 
    global moves
    global h1_crates
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                h1_crates=0

        if event.type == pygame.MOUSEBUTTONDOWN:

            crate_clicked = False
            for crate in crates:
                if crate.collidepoint(event.pos) and is_within_3x3_area(player, crate) and player_selected == False and crate_selected == None:
                    crate_selected = crate
                    crate_clicked = True

            if crate_selected and not crate_clicked and border.collidepoint(event.pos):
                for box in boxes:
                    if box.collidepoint(event.pos):
                        if not is_within_3x3_area(player, box):
                            error_sound.play()
                            break
                        if player.colliderect(box):
                            error_sound.play()
                            break
                        if any(blocker.colliderect(box) for blocker in blockers):
                            error_sound.play()
                            break
                        if any(crate.colliderect(box) for crate in crates):
                            error_sound.play()
                            break
                        if receiver.colliderect(box):
                            crates.remove(crate_selected)
                            click_sound.play()
                            h1_crates=h1_crates-1
                        crate_selected.center = box.center
                        moves=moves+1
                        break
                crate_selected = None

            if player.collidepoint(event.pos):
                player_selected = not player_selected

            elif player_selected and border.collidepoint(event.pos):
                for box in boxes:
                    if box.collidepoint(event.pos):
                        if receiver.colliderect(box):
                            error_sound.play()
                            break
                        if any(crate.colliderect(box) for crate in crates):
                            error_sound.play()
                            break
                        if any(blocker.colliderect(box) for blocker in blockers):
                            error_sound.play()
                            break
                        player.center = box.center
                        moves=moves+1
                        break
                player_selected = False 
"""""
def handle_wonvs():
    global state
    global run
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if foward_button.collidepoint(event.pos):
                state = 'reset'

        if event.type == pygame.QUIT:
                run = False    
pygame.mixer.init()
click_sound = pygame.mixer.Sound("click.wav")
error_sound = pygame.mixer.Sound("error.mp3")
click_sound.set_volume(1)

player_selected = False
last_box_space = None
crate_selected = None
actual_time = None
actual_time_p1 = None
actual_time_p2 = None
score_p1 = 0
score_p2 = 0
run = True
turn = None
round = 0
state = 'reset'
hardcore_mode = False
N_GREEN = (5, 227, 5)
duration1 = 3
duration2 = 8
duration3 = 27

font_size = int(S_W*(6/167))
font_size3 = font_size * 3
font = pygame.font.Font(None, font_size)
font3 = pygame.font.Font(None, font_size3)
intro_message = font.render("A demo based in ST4CK PUSHER from WTTG2", True, (255,255,255))
message1 = font.render("Hello there!", True, (255,255,255))
message2 = font.render("Your main objective is to move the GREEN CRATES to the center box.", True, (255,255,255))
message3 = font.render("To move the crates you need to go grab them with the MOVER.", True, (255,255,255))
message4 = font.render("The MOVER has a 3x3 grabbing area can go anywhere on the grid.", True, (255,255,255))
message5 = font.render("At the end your time and move count will be stored on the leaderboard.", True, (255,255,255))
hardcore_exp = font.render ("HARDCORE MODE — time limit + extra blockers", True, (255,255,255))

# Screen keyboard variables
keyboard_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
keyboard_buttons = {}
input_text = ""
letter_size = None  # Will be calculated during reset

while run:

    if state == 'intro':
        screen.blit(start_button_sprite,(start_button.x,start_button.y))
        screen.blit(settings_button_sprite,(settings_button.x,settings_button.y))
        screen.blit(leaderboard_b_s,(leaderboard_b.x,leaderboard_b.y))
        screen.blit(how_to_play_button_sprite,(how_to_play_button.x,how_to_play_button.y))
        screen.blit(vs_b_s,(vs_b.x,vs_b.y))

        if blocker_near == 8: state = 'reset'

        if DIFFICULTY == 1:
            screen.blit(first_button_sprite_selected,(first_button.x,first_button.y))
        else:
            screen.blit(first_button_sprite,(first_button.x,first_button.y))
        if DIFFICULTY == 2:
            screen.blit(second_button_sprite_selected,(second_button.x,second_button.y))
        else:
            screen.blit(second_button_sprite,(second_button.x,second_button.y))
        if DIFFICULTY == 3:
            screen.blit(third_button_sprite_selected,(third_button.x,third_button.y))
        else:
            screen.blit(third_button_sprite,(third_button.x,third_button.y))

        screen.blit(intro_message, (SMOL_BOX,SMOL_BOX))
        screen.blit(difficulty_sprite,(difficulty_label.x,difficulty_label.y))

        handle_intro()

    if state == 'game' or state == 'vs':
        pygame.draw.rect(screen, (0, 0, 250), receiver)

        if DIFFICULTY==1:duration=duration1
        if DIFFICULTY==2:duration=duration2
        if DIFFICULTY==3:duration=duration3

        if hardcore_mode:
            progress = min(seconds / duration, 1.0)
            angle_filled = progress * 360
            print (progress)
            if progress == 1.0 and seconds != 0: state = 'gameover'

            draw_clock_segments(screen, (S_W - 100, 100), 80, angle_filled)
            pygame.draw.circle(screen, (0,0,0), (S_W - 100, 100), 80 + 2, 3)

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

        if h1_crates == 0 and state == 'game': 
            state = 'won' 
            actual_time = time_left
        if h1_crates == 0 and state == 'vs': 
            state = 'wonvs'  
            actual_time = time_left
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = 'intro'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    h1_crates=0

            if event.type == pygame.MOUSEBUTTONDOWN:

                crate_clicked = False
                for crate in crates:
                    if crate.collidepoint(event.pos) and is_within_3x3_area(player, crate) and player_selected == False and crate_selected == None:
                        crate_selected = crate
                        crate_clicked = True

                if crate_selected and not crate_clicked and border.collidepoint(event.pos):
                    for box in boxes:
                        if box.collidepoint(event.pos):
                            if not is_within_3x3_area(player, box):
                                error_sound.play()
                                break
                            if player.colliderect(box):
                                error_sound.play()
                                break
                            if any(blocker.colliderect(box) for blocker in blockers):
                                error_sound.play()
                                break
                            if any(crate.colliderect(box) for crate in crates):
                                error_sound.play()
                                break
                            if receiver.colliderect(box):
                                crates.remove(crate_selected)
                                click_sound.play()
                                h1_crates=h1_crates-1
                            crate_selected.center = box.center
                            moves=moves+1
                            break
                    crate_selected = None

                if player.collidepoint(event.pos):
                    player_selected = not player_selected

                elif player_selected and border.collidepoint(event.pos):
                    for box in boxes:
                        if box.collidepoint(event.pos):
                            if receiver.colliderect(box):
                                error_sound.play()
                                break
                            if any(crate.colliderect(box) for crate in crates):
                                error_sound.play()
                                break
                            if any(blocker.colliderect(box) for blocker in blockers):
                                error_sound.play()
                                break
                            player.center = box.center
                            moves=moves+1
                            break
                    player_selected = False 

        screen.blit(timer_text, (SMOL_BOX, 2*SMOL_BOX))
        move_counter = font.render(str(moves), True, (255, 255, 255))
        screen.blit(move_counter, (SMOL_BOX,SMOL_BOX))

    if state == 'settings':
        
        cg=int(slider_thing.x-1.03*SMOL_BOX)
        cg1=(4.18/60)*SMOL_BOX
        cg2=int(cg/cg1)
        slider_percentage = font.render("Volume "+str(cg2), True, (255,255,255))
        
        screen.blit(slider_sprite,(slider.x,slider.y))
        screen.blit(slider_thing_sprite,(slider_thing.x,slider_thing.y))
        screen.blit(back_button_sprite,(back_button.x,back_button.y))
        screen.blit(slider_percentage, (SMOL_BOX,SMOL_BOX))
        screen.blit(hardcore_exp, (hardcore_b.x+2*SMOL_BOX,hardcore_b.y+(1/4)*SMOL_BOX))

        if not hardcore_mode: screen.blit(hardcore_b_s, (hardcore_b.x,hardcore_b.y))
        else: screen.blit(hardcore_b_selected_s ,(hardcore_b_selected.x,hardcore_b_selected.y))

        handle_settings()
            
    if state == 'how_to_play':

        page_text = font.render(str(page), True, N_GREEN)

        screen.blit(back_button_sprite,(back_button.x,back_button.y))
        screen.blit(foward_button_sprite,(foward_button.x,foward_button.y))
        if page == 1:screen.blit(message1, (SMOL_BOX,SMOL_BOX))
        if page == 2:
         screen.blit(message2, (SMOL_BOX,SMOL_BOX))
         screen.blit(slide1_s,(slide1.x,slide1.y))
        if page == 3:
         screen.blit(message3, (SMOL_BOX,SMOL_BOX))
         screen.blit(slide2_s,(slide2.x,slide2.y))
        if page == 4:
         screen.blit(message4, (SMOL_BOX,SMOL_BOX))
         screen.blit(slide2_s,(slide2.x,slide2.y))
        if page == 5:
         screen.blit(message5, (SMOL_BOX,SMOL_BOX))
         screen.blit(slide3_s,(slide3.x,slide3.y))
        if page > 5: state = 'reset'

        screen.blit(page_text, (foward_button.x+0.4*BOX_SPACE, foward_button.y+0.35*BOX_SPACE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if foward_button.collidepoint(event.pos):
                    page = page+1
                if back_button.collidepoint(event.pos):
                    state = 'reset'          

    if state == 'won':
        screen.fill((0, 0, 0))

        if DIFFICULTY == 1: a="1.txt"
        if DIFFICULTY == 2: a="2.txt"
        if DIFFICULTY == 3: a="3.txt"

        if time_left == 0:
            with open(a, "r+") as file:
                content=file.read().strip()
                lines = content.split("\n")
            state = "score"
            

        
        # Display current input text
        txt_surface = font.render("Enter a three-letter name: " + input_text, True, (255, 255, 255))
        screen.blit(txt_surface, (S_W//2 - txt_surface.get_width()//2, S_H//4))
        
        # Draw keyboard
        for letter, button in keyboard_buttons.items():
            # Highlight letter if it's already in input_text
            color = (50, 0, 0) if letter in input_text else (0, 0, 0)
            pygame.draw.rect(screen, color, button)
            letter_surf = font.render(letter, True, N_GREEN)
            screen.blit(letter_surf, (button.x + (letter_size//4), button.y + (letter_size//4)))
        
        # Draw backspace button
        pygame.draw.rect(screen, (250, 0, 0), backspace_button)
        
        # Draw submit button
        pygame.draw.rect(screen, (100, 200, 100) if len(input_text) == 3 else (150, 150, 150), submit_button)
        submit_text = font.render("OK", True, (0, 0, 0))
        screen.blit(submit_text, (submit_button.x + letter_size//3, submit_button.y + letter_size//4))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a letter was clicked
                for letter, button in keyboard_buttons.items():
                    if button.collidepoint(event.pos) and len(input_text) < 3:
                        input_text += letter
                        click_sound.play()
                        break
                
                # Check if backspace was clicked
                if backspace_button.collidepoint(event.pos) and len(input_text) > 0:
                    input_text = input_text[:-1]
                    click_sound.play()
                
                # Check if submit was clicked
                if submit_button.collidepoint(event.pos) and len(input_text) == 3:
                    score_name = input_text
                    score_time = str(actual_time)
                    score_moves = str(moves)
                    
                    # Determine the correct leaderboard file based on difficulty
                    if DIFFICULTY == 1: a = "1.txt"
                    if DIFFICULTY == 2: a = "2.txt"
                    if DIFFICULTY == 3: a = "3.txt"
                    
                    with open(a, "r+") as file:
                        content = file.read().strip()
                        new_content = content + "\n" + score_name + "-" + score_time + "  " + score_moves
                        file.seek(0)
                        file.write(new_content)
                        file.truncate()
                    
                    # Sort the leaderboard file
                    sort_leaderboard(a)
                    
                    # Reload the sorted lines
                    with open(a, "r") as file:
                        lines = file.readlines()
                    
                    input_text = ""  # Reset input text
                    state = 'score'
                    click_sound.play()

    if state == 'tela_preta':
        screen.fill ((0,0,0))
        score_text = font3.render( "P1   " + str(score_p1) + "-" + str(score_p2) + "   P2", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(S_W // 2, S_H // 2))
        screen.blit(score_text, score_rect)
        screen.blit(foward_button_sprite,(foward_button.x, foward_button.y))

        handle_wonvs()

    if state == 'wonvs':
        screen.fill((0, 0, 0))
        screen.blit(foward_button_sprite,(foward_button.x, foward_button.y))
        actual_time_text = font.render(str(actual_time), True, (255, 255, 255))
        screen.blit(actual_time_text, (SMOL_BOX,SMOL_BOX))
        if turn == 1 : actual_time_p1 = actual_time
        if turn == 2 : actual_time_p2 = actual_time
        
        handle_wonvs()

    if state == 'score':


        text_surfaces = [font.render(line.strip(), True, (255, 255, 255)) for line in lines]

        special_offset = 1.5*font_size
        for surface in text_surfaces:
            screen.blit(surface, (51, special_offset))
            special_offset += 1.2*font_size

        screen.blit(button_sprite, (button.x, button.y))
        handle_score()

    if state == 'gameover':

        screen.blit(game_over_s,(game_over.x,game_over.y))
        screen.blit(foward_button_sprite,(foward_button.x, foward_button.y))
        handle_wonvs()

    if state == 'reset':

        GRID_SIZE = 3+DIFFICULTY*2

        page=1

        pygame.mixer.music.set_volume = 1

        BOX_SIZE = min(S_W, S_H) // (GRID_SIZE + 1)
        BOX_SPACE = BOX_SIZE - 6
        BORDER_OFFSET = (min(S_W, S_H) - GRID_SIZE * BOX_SIZE) // 2

        SMOL_BOX = BOX_SPACE*(2/3)

        boxes = []
        for i in range(GRID_SIZE):  # Outer loop
            for j in range(GRID_SIZE):  # Inner loop
                boxX = i * BOX_SIZE + BORDER_OFFSET + (S_W - min(S_W, S_H)) // 2
                boxY = j * BOX_SIZE + BORDER_OFFSET + (S_H - min(S_W, S_H)) // 2
                box = pygame.Rect(boxX, boxY, BOX_SIZE, BOX_SIZE)
                boxes.append(box)
        
        center_index = GRID_SIZE**2 // 2
        center_box = boxes[center_index]
        near_center_indices = [
            center_index + 1, center_index - 1,
            center_index + GRID_SIZE, center_index + GRID_SIZE - 1,
            center_index + GRID_SIZE + 1, center_index - GRID_SIZE,
            center_index - GRID_SIZE + 1, center_index - GRID_SIZE - 1
        ]

        # Get the actual box objects
        near_center_boxes = [boxes[i] for i in near_center_indices if 0 <= i < len(boxes)]


        if BOX_SPACE != last_box_space:

            player_sprite = ls('player_sprite.png', BOX_SPACE, BOX_SPACE)
            player_sprite_selected = ls('player_sprite_selected.png', BOX_SPACE, BOX_SPACE)
            crate_sprite = ls('crate_sprite.png', BOX_SPACE, BOX_SPACE)
            crate_sprite_selected = ls('crate_sprite_selected.png', BOX_SPACE, BOX_SPACE)
            blocker_sprite = ls('blocker_sprite.png', BOX_SPACE, BOX_SPACE)
            button_sprite = ls('button_sprite.png', BOX_SPACE, BOX_SPACE)
            start_button_sprite = ls('start_button_sprite.png', 2*BOX_SPACE, 0.6*BOX_SPACE)
            first_button_sprite = ls('1.png', SMOL_BOX, SMOL_BOX)
            second_button_sprite = ls('2.png', SMOL_BOX, SMOL_BOX)
            third_button_sprite = ls('3.png', SMOL_BOX, SMOL_BOX)
            hardcore_b_s = ls('blank_b.png', SMOL_BOX, SMOL_BOX)
            hardcore_b_selected_s = ls ('blank_y_s.png', SMOL_BOX, SMOL_BOX)
            first_button_sprite_selected = ls('1_selected.png', SMOL_BOX, SMOL_BOX)
            second_button_sprite_selected = ls('2_selected.png', SMOL_BOX, SMOL_BOX)
            third_button_sprite_selected = ls('3_selected.png', SMOL_BOX, SMOL_BOX)
            difficulty_sprite = ls("difficulty_sprite.png", 4*SMOL_BOX,SMOL_BOX)
            settings_button_sprite = ls("settings.png",BOX_SPACE,BOX_SPACE)
            leaderboard_b_s = ls("leaderboard_b_s.png",BOX_SPACE,BOX_SPACE)
            how_to_play_button_sprite = ls("how_to_play_button_sprite.png",2.73*BOX_SPACE,0.6*BOX_SPACE)
            back_button_sprite = ls("back_button_sprite.png",2*BOX_SPACE,0.6*BOX_SPACE)
            foward_button_sprite = ls("blank_b.png",BOX_SPACE,BOX_SPACE)
            game_over_s = ls("game_over_s.png", (34/7)*BOX_SPACE, BOX_SPACE)
            #34x7
            slider_sprite = ls ("green_square.png",5*BOX_SPACE,SMOL_BOX/2)
            slider_thing_sprite = ls ("black_square.png",SMOL_BOX/2.3,SMOL_BOX/2.3)
            slide1_s = ls ("slide1_s.png",5*BOX_SPACE,5*BOX_SPACE)
            slide2_s = ls ("slide2_s.png",5*BOX_SPACE,5*BOX_SPACE)
            slide3_s = ls ("slide3_s.png",5*BOX_SPACE,5*BOX_SPACE)
            vs_b_s = ls ("1v1_s.png",1.27*BOX_SPACE,0.6*BOX_SPACE)

            #INTRO
            start_button= pygame.Rect((S_W//2)-BOX_SPACE,(S_H//2)-0.3*BOX_SPACE,2*BOX_SPACE,0.6*BOX_SPACE)
            settings_button = pygame.Rect(S_W - 2*BOX_SPACE,S_H - 2*BOX_SPACE,BOX_SPACE,BOX_SPACE)
            leaderboard_b = pygame.Rect(BOX_SPACE,S_H - 2*BOX_SPACE,BOX_SPACE,BOX_SPACE)
            how_to_play_button = pygame.Rect((S_W//2)-1.365*BOX_SPACE,(S_H//2)+0.6*BOX_SPACE,2.73*BOX_SPACE,0.6*BOX_SPACE)
            difficulty_label = pygame.Rect(SMOL_BOX,1.5*BOX_SPACE, 4*SMOL_BOX, SMOL_BOX)
            first_button = pygame.Rect(4*BOX_SPACE,1.5*BOX_SPACE, SMOL_BOX, SMOL_BOX)
            second_button = pygame.Rect(5*BOX_SPACE,1.5*BOX_SPACE, SMOL_BOX, SMOL_BOX)
            third_button= pygame.Rect(6*BOX_SPACE,1.5*BOX_SPACE, SMOL_BOX, SMOL_BOX)
            vs_b = pygame.Rect((S_W//2)-0.64*BOX_SPACE,(S_H//2)+1.5*BOX_SPACE,1.27*BOX_SPACE,0.6*BOX_SPACE)
            #SETTINGS
            back_button = pygame.Rect(BOX_SPACE,S_H-2*BOX_SPACE,2*BOX_SPACE,0.6*BOX_SPACE)
            foward_button = pygame.Rect(S_W-2*BOX_SPACE,S_H-2*BOX_SPACE,BOX_SPACE,BOX_SPACE)
            slider = pygame.Rect(SMOL_BOX,1.5*BOX_SPACE,5*BOX_SPACE,SMOL_BOX/1.7)
            slider_thing = pygame.Rect(1.04*SMOL_BOX,1.525*BOX_SPACE,SMOL_BOX/1.8,SMOL_BOX/1.8)
            hardcore_b = pygame.Rect(4*BOX_SPACE,4*BOX_SPACE,SMOL_BOX,SMOL_BOX)
            hardcore_b_selected = pygame.Rect(4*BOX_SPACE,4*BOX_SPACE,SMOL_BOX,SMOL_BOX)

            
            hardcore_b_s = ls('blank_b.png', SMOL_BOX, SMOL_BOX)
            hardcore_b_selected_s = ls ('blank_y_s.png', SMOL_BOX, SMOL_BOX)
            #SCORE
            button = pygame.Rect(center_box.left - BOX_SPACE,center_box.top, BOX_SPACE, BOX_SPACE)
            #GAMEOVER
            game_over = pygame.Rect((S_W/2)-(17/7)*BOX_SPACE,(S_H/2)-BOX_SPACE,(34/7)*BOX_SPACE,BOX_SPACE)
            
            #HOW TO PLAY
            slide1 = pygame.Rect(5*BOX_SPACE,2*BOX_SPACE,5*BOX_SPACE,5*BOX_SPACE)
            slide2 = pygame.Rect(5*BOX_SPACE,2*BOX_SPACE,5*BOX_SPACE,5*BOX_SPACE)
            slide3 = pygame.Rect(5*BOX_SPACE,2*BOX_SPACE,5*BOX_SPACE,5*BOX_SPACE)
            #VS

            last_box_space = BOX_SPACE

        # Setup screen keyboard
        letter_size = min(S_W // 10, S_H // 10)  # Size of each letter button
        keyboard_buttons = {}
        
        # Create keyboard layout (3 rows of letters)
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for row_idx, row in enumerate(rows):
            for col_idx, letter in enumerate(row):
                x_offset = (S_W - len(row) * letter_size) // 2 + col_idx * letter_size
                y_offset = S_H // 2 + row_idx * letter_size
                keyboard_buttons[letter] = pygame.Rect(x_offset, y_offset, letter_size, letter_size)
        
        # Create backspace and submit buttons
        backspace_button = pygame.Rect(S_W//2 - letter_size*1.5, S_H//2 + 3*letter_size, letter_size*1.5, letter_size)
        submit_button = pygame.Rect(S_W//2 + letter_size*0.2, S_H//2 + 3*letter_size, letter_size*1.5, letter_size)
        
        # Reset input text
        input_text = ""

        border = pygame.Rect(
            BORDER_OFFSET + (S_W - min(S_W, S_H)) // 2,
            BORDER_OFFSET + (S_H - min(S_W, S_H)) // 2,
            GRID_SIZE * BOX_SIZE, GRID_SIZE * BOX_SIZE
        )
        border.inflate_ip(6,6)

        receiver = pygame.Rect(center_box.left + 3, center_box.top + 3, BOX_SPACE, BOX_SPACE)
        
        available_boxes = [box for box in boxes if box != center_box]
        player_box = random.choice(available_boxes)
        player = pygame.Rect(player_box.left + 3, player_box.top + 3, BOX_SPACE, BOX_SPACE)

        available_boxes = [box for box in boxes if box != center_box and box != player_box]
        h1_crates = int(1.5*2**DIFFICULTY)
        crates = []
        for h in range(h1_crates):

            crate_box = random.choice(available_boxes)
            crate = pygame.Rect(crate_box.left + 3, crate_box.top + 3, BOX_SPACE, BOX_SPACE)
            crates.append(crate)
            available_boxes.remove(crate_box)

        if hardcore_mode : h1_crates_blockers = h1_crates*3
        else: h1_crates_blockers = h1_crates
        blockers = []
        blocker_near = 0
        for h in range(h1_crates_blockers):
            blocker_box = random.choice(available_boxes)
            if blocker_box in near_center_boxes: blocker_near += 1
            blocker = pygame.Rect(blocker_box.left + 3, blocker_box.top + 3, BOX_SPACE, BOX_SPACE)
            blockers.append(blocker)
            available_boxes.remove(blocker_box)
        
        
        if turn == 1 and actual_time_p1 != None: turn = 2
        if round == 1 and turn == 1:
            actual_time_p1 = None 
            actual_time_p2 = None 
            


        click_sound.play()
        moves = 0
        if turn == None:
            state = 'intro'
        if turn == 1: state = 'vs'
        if turn == 2:
            if actual_time_p2 == None: state = 'vs'
            if actual_time_p2 != None:
                if actual_time_p1 > actual_time_p2:
                    score_p2 += 1
                if actual_time_p1 < actual_time_p2:
                    score_p1 += 1
                

                round += 1
                actual_time_p1 = None 
                actual_time_p2 = None 
                turn = 1
                state = 'tela_preta'
 
    if moves == 0: start_ticks = pygame.time.get_ticks()
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000 # convert to seconds
    time_left = float(seconds)
    timer_text = font.render(f"{time_left}", True, (255, 255, 255))
    pygame.display.update()
    pygame.time.Clock().tick(60)
    #print (near_center_indexes)
    #print(blockers)
    #print (blocker_near)

    screen.fill((0, 0, 0))

pygame.quit()