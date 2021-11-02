# import sys
# import os

import pygame as pg
import sys, random
import pygame.midi

def ball_animation():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_restart()
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        # print(
        #     "%2i: interface :%s:, name :%s:, opened :%s:  %s"
        #     % (i, interf, name, opened, in_out)
        # )

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7
speed = 8

pg.init()
pg.fastevent.init()
event_get = pg.fastevent.get
event_post = pg.fastevent.post
pygame.midi.init()
_print_device_info()
clock = pygame.time.Clock()
    #
# if device_id is None:
input_id = pygame.midi.get_default_input_id()
# else:
#     input_id = device_id

i = pygame.midi.Input(input_id)
# screen_width = 1280
# screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

going = True
while going:
    events = event_get()
    for e in events:
        if e.type in [pg.QUIT]:
            going = False
        if e.type in [pg.KEYDOWN]:
            print(e)
            # going = False
        if e.type in [pygame.midi.MIDIIN]:
            print(e)


            if e.status == 144:
                print('On')
                if e.data1 == 50:
                    player_speed -= speed
                if e.data1 == 48:
                    player_speed += speed

            if e.status == 128:
                if e.data1 == 50:
                    player_speed += speed
                if e.data1 == 48:
                    player_speed -= speed

            # print(e.data1)
            #STATUS is 144 for noteon and 144 for noteoff

    if i.poll():
        midi_events = i.read(10)
        # convert them into pygame events.
        midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

        for m_e in midi_evs:
            event_post(m_e)

    ball_animation()
    player_animation()
    opponent_ai()
    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    pygame.display.flip()
    clock.tick(60)

del i
pygame.midi.quit()

