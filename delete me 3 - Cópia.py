import pygame
import random

#32x

pygame.init()

DIFFICULTY = 2

screen_info = pygame.display.Info()
#S_W, S_H = screen_info.current_w, screen_info.current_h
S_W, S_H = (screen_info.current_w/100)*55, (screen_info.current_h/100)*55
screen = pygame.display.set_mode((S_W, S_H),)

def loadscale(file_path, size1, size2):
    image = pygame.image.load(file_path)
    return pygame.transform.scale(image, (size1,size2))

def update_score_file(file_name, score_name, score_time):
    with open(file_name, "r+") as file:
        content = file.readlines()
        file.seek(0)
        file.write(f"{score_name}-{score_time}\n")
        file.writelines(content)
        file.truncate()

def is_within_3x3_area(player_rect, crate_rect):
    return abs(player_rect.centerx - crate_rect.centerx) <= BOX_SIZE and \
           abs(player_rect.centery - crate_rect.centery) <= BOX_SIZE

pygame.mixer.init()
click_sound = pygame.mixer.Sound("click.wav")
click_sound.play()

player_selected = False
crate_selected = None
run = True
state = 'reset'

font_size = int(S_W*(6/167))
font = pygame.font.Font(None, font_size)
intro_message = font.render("A demo based in ST4CK PUSHER from WTTG2", True, (255,255,255))

while run:

    if state == 'intro':
        screen.blit(start_button_sprite,(start_button.x,start_button.y))
        screen.blit(settings_button_sprite,(settings_button.x,settings_button.y))
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

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    state='game'
                if settings_button.collidepoint(event.pos):
                    state='settings'
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

    if state == 'game':
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

                crate_clicked = False
                for crate in crates:
                    if crate.collidepoint(event.pos) and is_within_3x3_area(player, crate) and player_selected == False and crate_selected == None:
                        crate_selected = crate
                        crate_clicked = True

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

        screen.blit(timer_text, (SMOL_BOX, 2*SMOL_BOX))
        move_counter = font.render(str(moves), True, (255, 255, 255))
        screen.blit(move_counter, (SMOL_BOX,SMOL_BOX))

    if state == 'settings':


        cg=slider_thing.x-1.03*SMOL_BOX
        slider_percentage = font.render(str(cg), True, (255,255,255))


        screen.blit(slider_sprite,(slider.x,slider.y))
        screen.blit(slider_thing_sprite,(slider_thing.x,slider_thing.y))
        screen.blit(back_button_sprite,(back_button.x,back_button.y))
        screen.blit(slider_percentage, (SMOL_BOX,SMOL_BOX))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    state = 'reset'
        if any(pygame.mouse.get_pressed()):
            if 1.03*SMOL_BOX < pygame.mouse.get_pos()[0] < 5.35*BOX_SPACE:
                slider_thing.x = pygame.mouse.get_pos() [0]



    if state == 'won':

        def get_user_input():
            input_text = ""
            active = True
            input_box = pygame.Rect(50, 50, 140, 32)    
            while active:
                screen.fill((0, 0, 0))
                txt_surface = font.render("Enter a three-letter name: " + input_text, True, (255, 255, 255))
                screen.blit(txt_surface, (50, 50))
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and len(input_text) == 3:
                            active = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        elif len(input_text) < 3 and event.unicode.isalpha():
                            input_text += event.unicode.upper()
            return input_text

        score_name = get_user_input()
        score_time = str(time_left)
        score_moves = str(moves)

        if DIFFICULTY == 1: a="1.txt"
        if DIFFICULTY == 2: a="2.txt"
        if DIFFICULTY == 3: a="3.txt"

        with open(a, "r+") as file:
            content = file.read().strip()
            new_content = content + "\n" + score_name + "-" + score_time + "  " + score_moves
            file.seek(0)
            file.write(new_content)
            file.truncate()
            lines = new_content.split("\n")

        state = 'score'

    if state == 'score':

        text_surfaces = [font.render(line.strip(), True, (255, 255, 255)) for line in lines]

        y_offset = 50
        for surface in text_surfaces:
            screen.blit(surface, (50, y_offset))
            y_offset += 48 + 5

        screen.blit(button_sprite, (button.x, button.y))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    state = 'reset'

            if event.type == pygame.QUIT:
                    run = False

    if state == 'reset':

        GRID_SIZE = 3+DIFFICULTY*2

        BOX_SIZE = min(S_W, S_H) // (GRID_SIZE + 1)
        BOX_SPACE = BOX_SIZE - 6
        BORDER_OFFSET = (min(S_W, S_H) - GRID_SIZE * BOX_SIZE) // 2

        SMOL_BOX = BOX_SPACE*(2/3)

        player_sprite = loadscale('player_sprite.png', BOX_SPACE, BOX_SPACE)
        player_sprite_selected = loadscale('player_sprite_selected.png', BOX_SPACE, BOX_SPACE)
        crate_sprite = loadscale('crate_sprite.png', BOX_SPACE, BOX_SPACE)
        crate_sprite_selected = loadscale('crate_sprite_selected.png', BOX_SPACE, BOX_SPACE)
        blocker_sprite = loadscale('blocker_sprite.png', BOX_SPACE, BOX_SPACE)
        button_sprite = loadscale('button_sprite.png', BOX_SPACE, BOX_SPACE)
        start_button_sprite = loadscale('start_button_sprite.png', 2*BOX_SPACE, 0.6*BOX_SPACE)
        first_button_sprite = loadscale('1.png', SMOL_BOX, SMOL_BOX)
        second_button_sprite = loadscale('2.png', SMOL_BOX, SMOL_BOX)
        third_button_sprite = loadscale('3.png', SMOL_BOX, SMOL_BOX)
        first_button_sprite_selected = loadscale('1_selected.png', SMOL_BOX, SMOL_BOX)
        second_button_sprite_selected = loadscale('2_selected.png', SMOL_BOX, SMOL_BOX)
        third_button_sprite_selected = loadscale('3_selected.png', SMOL_BOX, SMOL_BOX)
        difficulty_sprite = loadscale("difficulty_sprite.png", 4*SMOL_BOX,SMOL_BOX)
        settings_button_sprite = loadscale("settings.png",BOX_SPACE,BOX_SPACE)
        back_button_sprite = loadscale("back_button_sprite.png",2*BOX_SPACE,0.6*BOX_SPACE)
        slider_sprite = loadscale ("green_square.png",5*BOX_SPACE,SMOL_BOX/2)
        slider_thing_sprite = loadscale ("black_square.png",SMOL_BOX/2.3,SMOL_BOX/2.3)


        border = pygame.Rect(
            BORDER_OFFSET + (S_W - min(S_W, S_H)) // 2,
            BORDER_OFFSET + (S_H - min(S_W, S_H)) // 2,
            GRID_SIZE * BOX_SIZE, GRID_SIZE * BOX_SIZE
        )
        border.inflate_ip(6,6)

        boxes = []
        for i in range(GRID_SIZE):  # Outer loop
            for j in range(GRID_SIZE):  # Inner loop
                boxX = i * BOX_SIZE + BORDER_OFFSET + (S_W - min(S_W, S_H)) // 2
                boxY = j * BOX_SIZE + BORDER_OFFSET + (S_H - min(S_W, S_H)) // 2
                box = pygame.Rect(boxX, boxY, BOX_SIZE, BOX_SIZE)
                boxes.append(box)

        center_index = GRID_SIZE**2 // 2
        center_box = boxes[center_index]
        receiver = pygame.Rect(center_box.left + 3, center_box.top + 3, BOX_SPACE, BOX_SPACE)

        #INTRO
        start_button= pygame.Rect((S_W//2)-BOX_SPACE,(S_H//2)-0.3*BOX_SPACE,2*BOX_SPACE,0.6*BOX_SPACE)
        settings_button = pygame.Rect(S_W - 2*BOX_SPACE,S_H - 2*BOX_SPACE,BOX_SPACE,BOX_SPACE)
        difficulty_label = pygame.Rect(SMOL_BOX,1.5*BOX_SPACE, 4*SMOL_BOX, SMOL_BOX)
        first_button = pygame.Rect(4*BOX_SPACE,1.5*BOX_SPACE, SMOL_BOX, SMOL_BOX)
        second_button = pygame.Rect(5*BOX_SPACE,1.5*BOX_SPACE, SMOL_BOX, SMOL_BOX)
        third_button= pygame.Rect(6*BOX_SPACE,1.5*BOX_SPACE, SMOL_BOX, SMOL_BOX)
        #SETTINGS
        back_button = pygame.Rect(BOX_SPACE,S_H-2*BOX_SPACE,2*BOX_SPACE,0.6*BOX_SPACE)
        slider = pygame.Rect(SMOL_BOX,1.5*BOX_SPACE,5*BOX_SPACE,SMOL_BOX/2)
        slider_thing = pygame.Rect(1.04*SMOL_BOX,1.525*BOX_SPACE,SMOL_BOX/2.3,SMOL_BOX/2.3)
        #SCORE
        button = pygame.Rect(center_box.left - BOX_SPACE,center_box.top, BOX_SPACE, BOX_SPACE)

        
        available_boxes = [box for box in boxes if box != center_box]
        player_box = random.choice(available_boxes)
        player = pygame.Rect(player_box.left + 3, player_box.top + 3, BOX_SPACE, BOX_SPACE)

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


    if moves == 0: start_ticks = pygame.time.get_ticks()
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000 # convert to seconds
    time_left = float(seconds)
    timer_text = font.render(f"{time_left}", True, (255, 255, 255))
    pygame.display.update()
    pygame.time.Clock().tick(60)

    screen.fill((0, 0, 0))

pygame.quit()