import pygame
import random
import math
import socket # for multiplayer over internet
import select # for multiplayer over internet

pygame.init()

# Pong game - single player, local multiplayer and multiplayer over internet
# To keep things simple, each part of the game is contained in its own 'while' loop
# Only 1 resolution is available at the moment

# Currently stuck - client seems to find its own message

# screen size
size = (640, 480)
screen = pygame.display.set_mode(size)

# title
pygame.display.set_caption("Multiplayer Pong!")

# startup stuff
done = False                # if true, quit game
clock = pygame.time.Clock() # sets fps to 60
ball_list = []              # may implement multiple balls later
player_score = 0            # initial score
cpu_score = 0               # initial score
player2_score = 0           # initial score
main_menu = 1               # show main menu before playing game
single_player = 0           # is 1 if playing single player
multiplayer_local = 0       # is 1 if playing multiplayer local
multiplayer_internet = 0    # is 1 if playing multiplayer internet
scored = 0                  # for multipler internet, is 1 if player 1 just scored, is 2 if player 2 just scored, else 0

# colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# score
font30 = pygame.font.Font("Prototype.ttf", 25)
font50 = pygame.font.Font("Prototype.ttf", 45)
player_score_text = font30.render(str(player_score), 1, WHITE) # (string, anti-aliasing, colour)
cpu_score_text = font30.render(str(cpu_score), 1, WHITE)
player2_score_text = font30.render(str(player2_score), 1, WHITE)
main_menu_title = font50.render("PONG", 1, WHITE)
main_menu_single_player = font30.render("Single player", 1, WHITE)
main_menu_multiplayer_local = font30.render("Multiplayer local", 1, WHITE)
main_menu_multiplayer_internet = font30.render("Multiplayer internet", 1, WHITE)



# dealing with angles
PI = 3.14159265


def rad_to_deg(rad):
    return (rad/PI)*180


def deg_to_rad(deg):
    return (deg/180)*PI





# paddle class
class Paddle:
    width = 16
    height = 64
    x_speed = 0
    y_speed = 10.24

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y  # may not actually be used

    def reset_paddle(self):
        self.x = self.initial_x
        self.y = (size[1]/2)-(self.height/2)

    def change_height(self, new_height):
        self.height = new_height
        self.y -= new_height/2

    def change_x_speed(self, new_speed):
        self.x_speed = new_speed

    def change_y_speed(self, new_speed):
        self.y_speed = new_speed

    def move_paddle_up(self):
        self.y -= self.y_speed
        if self.y < 0:
            self.y = 0

    def move_paddle_down(self):
        self.y += self.y_speed
        if self.y + self.height > size[1]:
            self.y = size[1]-self.height

    # may later implement ways to move left and right
    def move_paddle_left(self):
        self.x -= self.x_speed
        if self.x < 0:
            self.x = 0

    def move_paddle_right(self):
        self.x += self.x_speed
        if self.x + self.width > size[0]:
            self.x = size[0] - self.width


class Ball:
    # direction is in degrees, with 0 on the right and increases anticlockwise
    width = 8
    height = 8
    delay = 60

    def __init__(self, x=316, y=236, speed=3.2, direction=random.randrange(360)):
        self.speed = speed
        self.direction = direction
        self.x = x
        self.y = y

    def reset_ball(self):
        self.x = 316
        self.y = 236
        self.speed = 3.2
        self.direction = random.randrange(360)
        self.delay = 60

    def check_paddle_collision(self, paddle):
        # if any of the corners of the ball is inside the paddle, return True
        if ((paddle.x < self.x < paddle.x + paddle.width and paddle.y < self.y < paddle.y + paddle.height) or
           (paddle.x < self.x + self.width < paddle.x + paddle.width and paddle.y < self.y < paddle.y + paddle.height) or
           (paddle.x < self.x < paddle.x + paddle.width and paddle.y < self.y + self.height < paddle.y + paddle.height) or
           (paddle.x < self.x + self.width < paddle.x + paddle.width and paddle.y < self.y + self.height < paddle.y + paddle.height)):
            return True
        else:
            return False

    def update(self):
        # delay before ball moves
        if self.delay > 0:
            self.delay -= 1
        else:
            self.x += self.speed*(math.cos(deg_to_rad(self.direction)))
            self.y -= self.speed*(math.sin(deg_to_rad(self.direction)))

            # collision with paddle
            if (self.check_paddle_collision(player_paddle) or
                    self.check_paddle_collision(cpu_paddle) or
                    self.check_paddle_collision(player2_paddle)):
                self.direction += 2*(90 - self.direction)
                self.direction %= 360
                self.speed *= 1.1
            # exits left side of screen
            if self.x < 0:
                global cpu_score
                global player2_score
                global scored
                player2_score += 1
                cpu_score += 1
                scored = 2
                self.reset_ball()
                player_paddle.reset_paddle()
                cpu_paddle.reset_paddle()
            # exits right side of screen
            if self.x > 640:
                global player_score
                global scored
                player_score += 1
                scored = 1
                self.reset_ball()
                player_paddle.reset_paddle()
                cpu_paddle.reset_paddle()
            # rebound if at top or bottom of screen
            if self.y < 0 or self.y > size[1]-self.height:
                self.direction *= -1
            self.direction %= 360

# Each game mode is kept in its own game loop #

# Main menu loop (may make setting to go back to main menu later)
while not done and main_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True # quit game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 64 < mouse_pos[0] < 224 and 305 < mouse_pos[1] < 345:
                main_menu = 0
                single_player = 1
            elif 64 < mouse_pos[0] < 259 and 355 < mouse_pos[1] < 395:
                main_menu = 0
                multiplayer_local = 1
            elif 64 < mouse_pos[0] < 294 and 405 < mouse_pos[1] < 445:
                main_menu = 0
                multiplayer_internet = 1

    # get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # display main menu
    screen.fill(BLACK)
    screen.blit(main_menu_title, (300, 100))

    # hover buttons
    if 64 < mouse_pos[0] < 224 and 305 < mouse_pos[1] < 345:
        pygame.draw.rect(screen, RED, (64, 305, 160, 40), 1)
    else:
        pygame.draw.rect(screen, WHITE, (64, 305, 160, 40), 1)
    if 64 < mouse_pos[0] < 259 and 355 < mouse_pos[1] < 395:
        pygame.draw.rect(screen, RED, (64, 355, 195, 40), 1)
    else:
        pygame.draw.rect(screen, WHITE, (64, 355, 195, 40), 1)
    if 64 < mouse_pos[0] < 294 and 405 < mouse_pos[1] < 445:
        pygame.draw.rect(screen, RED, (64, 405, 230, 40), 1)
    else:
        pygame.draw.rect(screen, WHITE, (64,405, 230, 40), 1)

    screen.blit(main_menu_single_player, (74, 310))
    screen.blit(main_menu_multiplayer_local, (74, 360))
    screen.blit(main_menu_multiplayer_internet, (74, 410))

    # display
    pygame.display.flip()
    clock.tick(60)


# create instances of objects before starting the game
player_paddle = Paddle(32, 208)  # assuming default height = 64
main_ball = Ball()
ball_list.append(main_ball)
cpu_paddle = Paddle(608, 208)
cpu_paddle.change_y_speed(2.56)
player2_paddle = Paddle(608, 208)

# single player game loop
while not done and single_player:
    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_paddle.reset_paddle()
                cpu_paddle.reset_paddle()
                ball_list[0].reset_ball()

    # poll for keyboard input
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN]:
        player_paddle.move_paddle_down()
    elif pressed[pygame.K_UP]:
        player_paddle.move_paddle_up()
    if pressed[pygame.K_RIGHT]:
        player_paddle.move_paddle_right()
    elif pressed[pygame.K_LEFT]:
        player_paddle.move_paddle_left()

    # game logic
    for ball in ball_list:
        ball.update()

    # cpu AI
    if ball_list[0].y > cpu_paddle.y + cpu_paddle.height/2:
        cpu_paddle.move_paddle_down()
    elif ball_list[0].y < cpu_paddle.y + cpu_paddle.height/2:
        cpu_paddle.move_paddle_up()

    # drawing code
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [player_paddle.x, player_paddle.y, player_paddle.width, player_paddle.height])
    pygame.draw.rect(screen, WHITE, [cpu_paddle.x, cpu_paddle.y, cpu_paddle.width, cpu_paddle.height])
    for ball in ball_list:
        pygame.draw.rect(screen, WHITE, [ball.x, ball.y, ball.width, ball.height])
    cpu_score_text = font30.render(str(cpu_score), 1, WHITE)
    player_score_text = font30.render(str(player_score), 1, WHITE)
    screen.blit(player_score_text, (295, 64))
    screen.blit(cpu_score_text, (335, 64))
    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()


# multiplayer local game loop
while not done and multiplayer_local:
    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_paddle.reset_paddle()
                player2_paddle.reset_paddle()
                ball_list[0].reset_ball()

    # poll for keyboard input
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN]:
        player_paddle.move_paddle_down()
    elif pressed[pygame.K_UP]:
        player_paddle.move_paddle_up()
    if pressed[pygame.K_RIGHT]:
        player_paddle.move_paddle_right()
    elif pressed[pygame.K_LEFT]:
        player_paddle.move_paddle_left()
    # player 2 keyboard input
    if pressed[pygame.K_s]:
        player2_paddle.move_paddle_down()
    elif pressed[pygame.K_w]:
        player2_paddle.move_paddle_up()
    if pressed[pygame.K_d]:
        player2_paddle.move_paddle_right()
    elif pressed[pygame.K_a]:
        player2_paddle.move_paddle_left()

    # game logic
    for ball in ball_list:
        ball.update()

    # drawing code
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [player_paddle.x, player_paddle.y, player_paddle.width, player_paddle.height])
    pygame.draw.rect(screen, WHITE, [player2_paddle.x, player2_paddle.y, player2_paddle.width, player2_paddle.height])
    for ball in ball_list:
        pygame.draw.rect(screen, WHITE, [ball.x, ball.y, ball.width, ball.height])
    player_score_text = font30.render(str(player_score), 1, WHITE)
    player2_score_text = font30.render(str(player2_score), 1, WHITE)
    screen.blit(player_score_text, (295, 64))
    screen.blit(player2_score_text, (335, 64))
    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()

# multiplayer internet loop - multiple screens
# multiplayer only variables
multiplayer_menu_text = font30.render("Are you the     host     or the     client     ?", 1, WHITE)
host = 0 # 1 if person is play
client = 0
connecting = 0
connected = 0

# Deciding between host and client
while not done and multiplayer_internet:
    # decide whether or not the person wishes to be the host or the client
    mouse_pos = pygame.mouse.get_pos()

    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 260 < mouse_pos[0] < 325 and 215 < mouse_pos[1] < 255:
                multiplayer_internet = 0
                host = 1
                port_menu = 1
            elif 450 < mouse_pos[0] < 529 and 215 < mouse_pos[1] < 255:
                multiplayer_internet = 0
                client = 1
                port_menu = 1

    # drawing code
    screen.fill(BLACK)
    screen.blit(multiplayer_menu_text, (100, 220))

    # deciding between host and client
    if 260 < mouse_pos[0] < 325 and 215 < mouse_pos[1] < 255:
        pygame.draw.rect(screen, RED, (260, 215, 65, 40), 1)
    else:
        pygame.draw.rect(screen, WHITE, (260, 215, 65, 40), 1)
    if 450 < mouse_pos[0] < 529 and 215 < mouse_pos[1] < 255:
        pygame.draw.rect(screen, RED, (450, 215, 79, 40), 1)
    else:
        pygame.draw.rect(screen, WHITE, (450, 215, 79, 40), 1)

    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()


# Decide on port
port_menu_text = font30.render("Type port number and press return", 1, WHITE)
port_string = "7707"
# port_string = port in string format
# port_text = text to be displayed on screen

while not done and port_menu:
    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(port_string) > 0:
                    port_string = port_string[:-1]
            elif event.key == pygame.K_0:
                port_string += "0"
            elif event.key == pygame.K_1:
                port_string += "1"
            elif event.key == pygame.K_2:
                port_string += "2"
            elif event.key == pygame.K_3:
                port_string += "3"
            elif event.key == pygame.K_4:
                port_string += "4"
            elif event.key == pygame.K_5:
                port_string += "5"
            elif event.key == pygame.K_6:
                port_string += "6"
            elif event.key == pygame.K_7:
                port_string += "7"
            elif event.key == pygame.K_8:
                port_string += "8"
            elif event.key == pygame.K_9:
                port_string += "9"
            elif event.key == pygame.K_RETURN:
                port_menu = 0
                ip_menu = 1 # for client
                port = int(port_string)

    screen.fill(BLACK)
    #display text
    port_text = font30.render(port_string, 1, WHITE)
    screen.blit(port_menu_text, (100, 190))
    screen.blit(port_text, (200, 250))

    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()


# Client needs to input ip address
if client and ip_menu:
    ip_address = "192.168.0.3"
    ip_menu_text = font30.render("Type ip address to connect to", 1, WHITE)
while not done and client and ip_menu:
    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(ip_address) > 0:
                    ip_address = ip_address[:-1]
            elif event.key == pygame.K_0:
                ip_address += "0"
            elif event.key == pygame.K_1:
                ip_address += "1"
            elif event.key == pygame.K_2:
                ip_address += "2"
            elif event.key == pygame.K_3:
                ip_address += "3"
            elif event.key == pygame.K_4:
                ip_address += "4"
            elif event.key == pygame.K_5:
                ip_address += "5"
            elif event.key == pygame.K_6:
                ip_address += "6"
            elif event.key == pygame.K_7:
                ip_address += "7"
            elif event.key == pygame.K_8:
                ip_address += "8"
            elif event.key == pygame.K_9:
                ip_address += "9"
            elif event.key == pygame.K_PERIOD:
                ip_address += "."
            elif event.key == pygame.K_RETURN:
                ip_menu = 0

    screen.fill(BLACK)
    #display text
    ip_text = font30.render(ip_address, 1, WHITE)
    screen.blit(ip_menu_text, (100, 190))
    screen.blit(ip_text, (200, 250))

    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()


# Sockets!
# Using UDP sockets
# Server waits for client to send a message saying "Connecting"
# Server sends "Connecting" back to client
# Client sends "Connected" back to server and waits for next message
# Server begins game by sending "game string", a message saying what is going on
# "game string" tells client the direction of ball, p1x, p1y, p2x and p2y

# host
if host:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket
    server_socket.bind(("0.0.0.0", port)) # bind to port
    connecting_text = font30.render("Waiting for client", 1, WHITE)

while not done and host and not connected:
    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game
    # check if any message is received
    ready_to_read, ready_to_write, in_error = select.select([server_socket], [], [], 0)

    # if message received:
    if ready_to_read:
        last_message, last_message_address = server_socket.recvfrom(1024)
        last_message = last_message.decode()
        if last_message == "Connecting":
            server_socket.sendto("Connecting".encode(), last_message_address)
        elif last_message == "Connected":
            server_socket.sendto("Connected".encode(), last_message_address)
            connected = 1

    screen.fill(BLACK)
    #display text
    screen.blit(connecting_text, (200, 250))

    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()


# client
if client:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket
    #client_socket.bind(("192.168.0.3", 7708))
    connecting_text = font30.render("Connecting to server", 1, WHITE)

while not done and client and not connected:
    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game


    # check if any message is received
    ready_to_read = select.select([client_socket], [], [], 0)[0]

    # send a message to server
    client_socket.sendto("Connecting".encode(), (ip_address, port))

    # if message received:
    if ready_to_read:
        last_message, last_message_address = client_socket.recvfrom(1024)
        last_message = last_message.decode()
        if last_message == "Connecting":
            server_socket.sendto("Connected", last_message_address)
        elif last_message == "Connected":
            connected = 1

    screen.fill(BLACK)
    #display text
    screen.blit(connecting_text, (200, 250))

    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()


# starting the game: server
# server sends "p,player1.x,player1.y,player2.x,player2.y," where player1.x is the x pos of player_paddle
#   or server sends "s,who_scored,ball.speed,ball.dir" to get direction of ball after a goal is scored
# server receives "left,down,up,right," where left = 0 if left not pressed, and 1 if left is pressed etc.
while not done and host and connected:
    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game

    # poll for keyboard input
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN]:
        player_paddle.move_paddle_down()
    elif pressed[pygame.K_UP]:
        player_paddle.move_paddle_up()
    if pressed[pygame.K_RIGHT]:
        player_paddle.move_paddle_right()
    elif pressed[pygame.K_LEFT]:
        player_paddle.move_paddle_left()

    # check if any message is received
    ready_to_read = select.select([client_socket], [], [], 0)[0]

    # if message received translate it into game input
    ready_to_read, ready_to_write, in_error = select.select([server_socket], [], [], 0)
    if ready_to_read:
        # take the last packet
        while ready_to_read:
            last_message, last_message_address = client_socket.recvfrom(1024)
            ready_to_read, ready_to_write, in_error = select.select([server_socket], [], [], 0)
        last_message = last_message.decode()
        # handle client input
        for i in [player2_paddle.move_paddle_left, player2_paddle.move_paddle_down,
                  player2_paddle.move_paddle_up, player2_paddle.move_paddle_right]:
            if last_message[0] == "1":
                i()
            last_message = last_message[2:]



    # game logic
    for ball in ball_list:
        ball.update()

    # send client message if client scored
    if scored > 0:
        server_socket.sendto(("s," + scored + "," +
                              main_ball.speed + "," +
                              main_ball.direction + ",").encode(), last_message_address)
        scored = 0

    # send new positions
    server_socket.sendto(("p," + player_paddle.x + "," +
                          player_paddle.y + "," +
                          player2_paddle.x + "," +
                          player2_paddle.y + ",").encode(), last_message_address)

    # drawing code
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [player_paddle.x, player_paddle.y, player_paddle.width, player_paddle.height])
    pygame.draw.rect(screen, WHITE, [player2_paddle.x, player2_paddle.y, player2_paddle.width, player2_paddle.height])
    for ball in ball_list:
        pygame.draw.rect(screen, WHITE, [ball.x, ball.y, ball.width, ball.height])
    player_score_text = font30.render(str(player_score), 1, WHITE)
    player2_score_text = font30.render(str(player2_score), 1, WHITE)
    screen.blit(player_score_text, (295, 64))
    screen.blit(player2_score_text, (335, 64))
    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()


# starting the game: client
# server sided game, so all positions are received from the server
# may have lag issues
while not done and client and connected:
    # event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # quit game

    # send input to server
    input_string = ""
    for i in [pressed[pygame.K_LEFT], pressed[pygame.K_DOWN],
              pressed[pygame.K_UP], pressed[pygame.K_RIGHT]]:
        if i:
            input_string += "1,"
        else:
            input_string += "0,"
    client_socket.sendto(input_string.encode(), (ip_address, port))

    # check if any message is received
    ready_to_read = select.select([client_socket], [], [], 0)[0]

    # if message received translate it into game input
    ready_to_read, ready_to_write, in_error = select.select([server_socket], [], [], 0)
    if ready_to_read:
        # check if packet begins with p or s
        while ready_to_read:
            last_message, last_message_address = client_socket.recvfrom(1024)
            last_message = last_message.decode()
            # if it begins with s, evaluate message
            if last_message[0] == "s":
                # "s,p,spd,dir," where p is the num of player who scored
                main_ball.reset_ball()
                if last_message[2] == 1:
                    player_score += 1
                elif last_message[2] == 2:
                    player2_score += 1
                last_message = last_message[4:]
                comma_index = last_message.index(",")
                main_ball.speed = int(last_message[:comma_index])
                last_message = last_message[comma_index + 1:]
                comma_index = last_message.index(",")
                main_ball.direction = int(last_message[:comma_index])
            # if message does not begin with s, check if there's more messages and evaluate the last one
            ready_to_read, ready_to_write, in_error = select.select([server_socket], [], [], 0)

        # evaluate last message received
        if last_message[1] == "p":
            # "p,p1x,p1y,p2x,p2y," where p1x = player_paddle.x, p2y = player2_paddle.y etc.
            last_message = last_message[2:]
            comma_index = last_message.index(",")
            player_paddle.x = int(last_message[:comma_index])
            last_message = last_message[comma_index + 1:]
            comma_index = last_message.index(",")
            player_paddle.y = int(last_message[:comma_index])
            last_message = last_message[comma_index + 1:]
            comma_index = last_message.index(",")
            player2_paddle.x = int(last_message[:comma_index])
            last_message = last_message[comma_index + 1:]
            comma_index = last_message.index(",")
            player2_paddle.y = int(last_message[:comma_index])

        last_message = "d" # make sure not to read same message more than once

    # game logic
    for ball in ball_list:
        ball.update()

    # drawing code
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [player_paddle.x, player_paddle.y, player_paddle.width, player_paddle.height])
    pygame.draw.rect(screen, WHITE, [player2_paddle.x, player2_paddle.y, player2_paddle.width, player2_paddle.height])
    for ball in ball_list:
        pygame.draw.rect(screen, WHITE, [ball.x, ball.y, ball.width, ball.height])
    player_score_text = font30.render(str(player_score), 1, WHITE)
    player2_score_text = font30.render(str(player2_score), 1, WHITE)
    screen.blit(player_score_text, (295, 64))
    screen.blit(player2_score_text, (335, 64))
    # limit fps to 60
    clock.tick(60)

    # update screen
    pygame.display.flip()



pygame.quit()
