import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200, 300))

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = text_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time
    

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)


        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return


def collisions(player, obstacle_list):

    if obstacle_list:
        for obstacle in obstacle_list:
            if player.colliderect(obstacle):
                return False
    return True


def player_animation():
    global player_index, player_surface
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner Game')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
player = Player()

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

#Player
player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(0, 300))
player_gravity = 0

#Obstacles
#Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surface = snail_frames[snail_index]

obstacle_rect_list = []

# Fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surf = fly_frames[fly_index]

#Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))
title_surf = text_font.render('Pixel Runner', False, (111, 196,196))
title_rect = title_surf.get_rect(center = (400, 80))
intruction_surf = text_font.render('Press space to run. ', False, (111, 196,196))
instruction_rect = intruction_surf.get_rect(center = (410, 340))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if player_rect.bottom >= 300:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint(event.pos):
                        player_gravity = -20

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            if event.type == snail_animation_timer: 
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_frames[snail_index]

            if event.type == fly_animation_timer: 
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_frames[fly_index]
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)

        score = display_score()

        # Player
        player_gravity +=1
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)   

        #Obstacle
        obstacle_movement(obstacle_rect_list)    

        #Collisions
        game_active = collisions(player_rect, obstacle_rect_list) 
    else:
        screen.fill((94, 129, 162))
        obstacle_rect_list.clear()
        player_rect.midbottom = (100, 80)

        screen.blit(player_stand, player_stand_rect)    
        screen.blit(title_surf, title_rect)

        score_message = text_font.render(f"Your score: {score}", False, (111, 196,196))
        score_rect = score_message.get_rect(midbottom = (400, 350))
        if score == 0:
            screen.blit(intruction_surf, instruction_rect)
            
        else:
            screen.blit(score_message, score_rect)

    pygame.display.update()
    clock.tick(60)

