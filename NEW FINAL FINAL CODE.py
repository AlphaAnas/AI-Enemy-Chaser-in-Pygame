import pygame
import sys
from random import randint
from pygame import mixer
from heapq import heapify, heappush, heappop

def dijsktra(graph,src,dest): # actual algorithm
    inf = sys.maxsize
    node_data={}
    for i in graph:
        node_data[i]={'cost':inf,'pred':[]}
    node_data[src]['cost'] = 0
    visited = []
    min_heap = []
    heappush(min_heap,(node_data[src]['cost'],src))
    while min_heap:
        temp = heappop(min_heap)[1]
        if temp not in visited:
            visited.append(temp)
            for j in graph[temp]:
                if j[0] not in visited:
                    cost = node_data[temp]['cost'] + j[1]
                    if cost < node_data[j[0]]['cost']:
                        node_data[j[0]]['cost'] = cost
                        node_data[j[0]]['pred'] = node_data[temp]['pred'] + [temp]
                    elif cost == node_data[j[0]]['cost']:
                        node_data[j[0]]['cost'] = cost
                        node_data[j[0]]['pred'] = min(node_data[temp]['pred'] + [temp],node_data[j[0]]['pred'], key=lambda i:len(i))
                    heappush(min_heap,(node_data[j[0]]['cost'],j[0]))
        heapify(min_heap)
    return list(node_data[dest]['pred'] + [dest])

grid_size=60   # each box will be of 60 pixels
rows = 10 ; col = 10

pygame.init() #initialize
screen=pygame.display.set_mode((grid_size*rows, (col*grid_size)+70))
pygame.display.set_caption('Chase Up!')
clock = pygame.time.Clock() #clock for constant frame rate
game_active = False # intro and gameover are same!

# energy , lvl , score
first_run = 0
score = 0 ; high_score = 0 
ad = 25 ; lvl = 1

# font
test_font = pygame.font.Font('Final Game/font/Pixeltype.ttf',45)

# All the Surfaces!
player_surface = pygame.image.load('Final Game/Assets/player.png')
player_surface = pygame.transform.scale(player_surface, (grid_size,grid_size))
player_x=0 ; player_y=0

start_surface = test_font.render('PRESS SPACE TO START!',True,(255,0,0))
start_rectangle = start_surface.get_rect(center = (300,200))

enemy_surface = pygame.image.load('Final Game/Assets/enemy.png').convert_alpha()
enemy_surface = pygame.transform.scale(enemy_surface, (grid_size,grid_size))
enemy_x = col - 1 ; enemy_y = rows - 1

food_surface = pygame.image.load('Final Game/Assets/ad.png').convert_alpha()
food_surface = pygame.transform.scale(food_surface,(40,78))
food_x = randint(0, col - 1) ; food_y = randint(0, rows - 1)

coin_surface = pygame.image.load('Final Game/Assets/coin.png').convert_alpha()
coin_surface = pygame.transform.scale(coin_surface,(35,55))
coin_x = randint(0, col - 1) ; coin_y = randint(0, rows - 1)

background_surface = pygame.image.load('Final Game/Assets/background.jpg').convert_alpha()
background_surface = pygame.transform.scale(background_surface,(610,610))

background2_surface = pygame.image.load('Final Game/Assets/background2.jpg').convert_alpha()
background2_surface = pygame.transform.scale(background2_surface,(610,610))

background3_surface = pygame.image.load('Final Game/Assets/background3.png').convert_alpha()
background3_surface = pygame.transform.scale(background3_surface,(610,610))

backgrounds=[background_surface,background2_surface,background3_surface]
bg_index = 0
# index increases after score is mod of 10.

# title surface
title_surface = test_font.render('CATCH UP!',True,'coral')
title_rectangle = title_surface.get_rect(center = (300,150))

# intruction surfaces
instruction1_surface = test_font.render('Instructions:',True,'Green')
instruction1_rectangle = instruction1_surface.get_rect(center = (300,250))

instruction2_surface = test_font.render('Beware of the Ghost!',True,'coral')
instruction2_rectangle = instruction2_surface.get_rect(center = (300,300))

instruction3_surface = test_font.render('Catch all the Coins!',True,'coral')
instruction3_rectangle = instruction3_surface.get_rect(center = (300,350))

instruction4_surface = test_font.render('Make sure to always have energy!',True,'coral')
instruction4_rectangle = instruction4_surface.get_rect(center = (300,400))

background_colour = pygame.Surface((600,600+70)) #(w,h)
background_colour.fill('coral') #typeofcolor

dumb = 0 # dumb way to slow down the enemy

# add game sound
mixer.music.load("Final Game/Assets/backgroundm.mp3") 
mixer.music.play(-1)
caught =mixer.Sound("Final Game/Assets/caught.wav") 
drink = mixer.Sound("Final Game/Assets/can.wav")
coin = mixer.Sound("Final Game/Assets/coinm.wav")

# grid map # unweighted we thought would be best and a bit easy too!
matrix = [[1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1],
          [1,1,1,1,1,1,1,1,1,1]]

# adj list
graph={}
matrix_length=len(matrix)
for i in range(matrix_length):
    for j in range(matrix_length):
        neighbours=[]
        if i-1>=0:
            neighbours.append(((i-1,j),matrix[i][j])) # neighbour and weight
        if i+1 <matrix_length:
            neighbours.append(((i+1,j),matrix[i][j]))
        if j-1>=0:
            neighbours.append(((i,j-1),matrix[i][j]))     
        if j+1 <matrix_length:
            neighbours.append(((i,j+1),matrix[i][j]))
        graph[(i,j)]=neighbours

# game loop
while True:
    # event loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT: #quit
            pygame.quit() #exit loop when window is closed # opposite of pygame.init()
            sys.exit() #breaks while True loop

        if game_active: # game running
            if event.type == pygame.KEYDOWN: # movement conditions
                ad -= 1 # energy going down gradually
                if event.key == pygame.K_LEFT:
                    if player_x > 0:
                        player_x -= 1
                if event.key == pygame.K_RIGHT :
                    if player_x < col - 1:
                        player_x += 1
                if event.key == pygame.K_UP:
                    if player_y > 0:
                        player_y -= 1
                if event.key == pygame.K_DOWN:
                    if player_y < rows - 1:
                        player_y += 1

        else:

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE: # gonna start game again...
                # food random
                food_x = randint(0, col - 1) ; food_y = randint(0, rows - 1)
                # coin random
                coin_x = randint(0, col - 1) ; coin_y = randint(0, rows - 1)
                # enemy at last
                enemy_x = col - 1 ; enemy_y = rows - 1
                # resetting everything
                score = 0 ; first_run = 0 ; ad = 25 ; bg_index = 0
                # game active
                game_active = True

    if game_active:
        # Displaying all Surfaces!
        screen.blit(background_colour,(0,0))
        screen.blit(backgrounds[bg_index],(-4,0))
        screen.blit(food_surface,( food_x  * grid_size,  food_y * grid_size))
        screen.blit(coin_surface,( coin_x  * grid_size,  coin_y * grid_size))

        # update of player and enemy
        screen.blit(player_surface, ( player_x  * grid_size,  player_y * grid_size))
        screen.blit(enemy_surface, ((enemy_x * grid_size), (enemy_y * grid_size)))

        # borders
        pygame.draw.line(screen,'black',(0,611),(600,611),7)
        pygame.draw.line(screen,'black',(245,611),(245,670),7)
        pygame.draw.line(screen,'black',(414,611),(414,670),7)
        pygame.draw.line(screen,'black',(0,666),(600,666),7)

        # level
        if score == 10:
            bg_index = 1
            lvl = 2
        elif score == 20:
            bg_index = 2
            lvl = 3
        elif score == 30:
            game_active = False
        level_surface = test_font.render(f'Level : {lvl}',True,(64,64,64))
        level_rectangle = level_surface.get_rect(center = (500,640))
        screen.blit(level_surface,level_rectangle)
    
        # score
        score_surface = test_font.render(f'Score : {score}',True,(64,64,64))
        score_rectangle = score_surface.get_rect(center = (330,640))
        screen.blit(score_surface,score_rectangle)

        # energy
        ad_surface = test_font.render(f'Energy : {ad}',True,(64,64,64))
        ad_rectangle = ad_surface.get_rect(center = (120,640))
        screen.blit(ad_surface,ad_rectangle)
        
        # pathfinding implementation
        start = (enemy_x,enemy_y)
        end = (player_x,player_y)
        path = dijsktra(graph,start,end)
        print(path)
        if dumb%6 == 0: # making the enemy slower
            try:
                enemy_x = path[1][0]
                enemy_y = path[1][1]
                # print(enemy_x,enemy_y)
            except:
                pass

        # collisions
        if player_x == enemy_x and player_y == enemy_y: # player and enemy
            player_x , player_y = 0 , 0
            enemy_x , enemy_y = col - 1 , rows - 1
            caught.play()
            game_active = False

        if ad <= 1: # energy 0
            player_x , player_y = 0 , 0
            enemy_x , enemy_y = col - 1 , rows - 1
            caught.play()
            game_active = False

        if player_x == food_x and player_y == food_y: # player and energy
            food_x = randint(0, col - 1) ; food_y = randint(0, rows - 1)
            ad += 25
            drink.play()
        
        if player_x == coin_x and player_y == coin_y: # player and coin
            coin_x = randint(0, col - 1) ; coin_y = randint(0, rows - 1)
            score += 1 ; first_coin = True 
            coin.play()

    else: # before // after game starts

        # displaying highscore!
        high_score_surface = test_font.render(f'High Score : {high_score}',True,'gold2')
        high_score_rectangle = high_score_surface.get_rect(center = (300,450))
        # screen.fill((94,129,162))
        starting_surface = pygame.image.load('Final Game/Assets/starting.png').convert_alpha()
        starting_surface = pygame.transform.scale(starting_surface,(rows*grid_size,(col*grid_size)+70))
        screen.blit(starting_surface,(0,0))
        screen.blit(start_surface,start_rectangle)

        if score != 0 or (score==0 and first_run == 0): # gameoverrrr...
            end_msg = test_font.render(f'Game Over!!!',True,(250,0,0)) # rgb
            end_msg_rectangle = end_msg.get_rect(center=(300, 500))
            screen.blit(end_msg, end_msg_rectangle)
            if score > high_score:
                high_score = score

        # title screen
        screen.blit(title_surface,title_rectangle)

        # all the instruction surfaces blitting!
        screen.blit(instruction1_surface,instruction1_rectangle)
        screen.blit(instruction2_surface,instruction2_rectangle)
        screen.blit(instruction3_surface,instruction3_rectangle)
        screen.blit(instruction4_surface,instruction4_rectangle)

        # high score blitting
        screen.blit(high_score_surface,high_score_rectangle)
        first_run += 1

        # game winning!
        if score == 30:
            winning_surface = test_font.render('You Won!',True,(0,255,0)) # rgb
            winning_surface = pygame.transform.scale2x(winning_surface)
            winning_rectangle = winning_surface.get_rect(center = (300,400))
            # screen.fill((94,129,162))
            screen.blit(start_surface,start_rectangle)
            screen.blit(winning_surface,winning_rectangle)

    pygame.display.update() # update each frame
    dumb += 1
    clock.tick(5) # 10fps