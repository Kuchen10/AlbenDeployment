import os
import pygame
import random

run = True
in_menu = True
game_mode = 1

pygame.init()
pygame.font.init()

screen_info = pygame.display.Info()
x = screen_info.current_w
y = screen_info.current_h

screen = pygame.display.set_mode([x, y], pygame.FULLSCREEN)

START_RACKET_WIDTH = int(x * 0.2)
START_RACKET_HEIGHT = int(y * 0.03)
START_BALL_RADIUS = int(min(x, y) * 0.03)

racketWidth = START_RACKET_WIDTH
racketHeight = START_RACKET_HEIGHT
ballRadius = START_BALL_RADIUS

racketX = (x // 2) - (racketWidth // 2)
racketY = int(y * 0.9)
speed = 0

racket2X = (x // 2) - (racketWidth // 2)
racket2Y = int(y * 0.07)
speed2 = 0

ballX = int(x / 2)
ballY = int(y / 2)
ballXSpeed = 3.5
ballYSpeed = -4.5

lives = 3
lives2 = 3
winner_text = ""
start_time = 0
life_lost_time_offset = 0
final_seconds = 0
is_highscore = False

items = []
item_spawn_timer = 0 

green_timer = 0
blue_timer = 0 

font = pygame.font.SysFont("Arial", int(y * 0.04))
large_font = pygame.font.SysFont("Arial", int(y * 0.06))


def get_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0


def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))


def format_time(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def reset():
    global ballYSpeed, ballXSpeed, ballX, ballY, racketX, racketY, racket2X, racket2Y, speed, speed2, lives, lives2, run, winner_text, final_seconds, is_highscore
    global racketWidth, racketHeight, ballRadius, items, green_timer, blue_timer, life_lost_time_offset, item_spawn_timer

    if game_mode == 1:
        lives -= 1
        if lives == 0:
            final_seconds = (pygame.time.get_ticks() - start_time) // 1000
            current_highscore = get_highscore()
            if final_seconds > current_highscore:
                save_highscore(final_seconds)
                is_highscore = True
                winner_text = f"Neuer Highscore! Zeit: {format_time(final_seconds)}"
            else:
                winner_text = f"Game Over! Zeit: {format_time(final_seconds)}"
            return
        else:
            life_lost_time_offset = pygame.time.get_ticks() - start_time
    else:
        if ballY < y // 2:
            lives2 -= 1
        else:
            lives -= 1

        if lives == 0:
            winner_text = "P2 (Blau) Gewinnt!"
            return
        elif lives2 == 0:
            winner_text = "P1 (Rot) Gewinnt!"
            return

    racketWidth = START_RACKET_WIDTH
    racketHeight = START_RACKET_HEIGHT
    ballRadius = START_BALL_RADIUS

    racketX = (x // 2) - (racketWidth // 2)
    racketY = int(y * 0.9)
    racket2X = (x // 2) - (racketWidth // 2)
    racket2Y = int(y * 0.07)
    ballX = int(x / 2)
    ballY = int(y / 2)
    speed = 0
    speed2 = 0

    items = []
    green_timer = 0
    blue_timer = 0
    
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 0), (int(ballX), int(ballY)), ballRadius, 0)
    pygame.draw.rect(
        screen, (255, 40, 0), (racketX, racketY, racketWidth, racketHeight), 0
    )
    if game_mode == 2:
        pygame.draw.rect(
            screen,
            (0, 40, 255),
            (racket2X, racket2Y, racketWidth, racketHeight),
            0,
        )
    pygame.display.flip()
    
    pygame.time.wait(1000)
    item_spawn_timer = pygame.time.get_ticks() 

    if game_mode == 1:
        ballXSpeed = random.choice([-3.5, 3.5])
        ballYSpeed = -4.5
    else:
        ballXSpeed = random.choice([-2, 2])
        ballYSpeed = random.choice([-3, 3])


def racketBlock():
    global speed, racketX
    if racketX < 0:
        racketX = 0
        speed = 0
    elif racketX > x - racketWidth:
        racketX = x - racketWidth
        speed = 0


def racket2Block():
    global speed2, racket2X
    if racket2X < 0:
        racket2X = 0
        speed2 = 0
    elif racket2X > x - racketWidth:
        racket2X = x - racketWidth
        speed2 = 0


def moveBall():
    global ballX, ballY
    ballX += ballXSpeed
    ballY += ballYSpeed


def ballBlock():
    global ballYSpeed, ballXSpeed
    
    speed_multiplier = 1.005 if game_mode == 1 else 1.025

    if game_mode == 1:
        if ballY - ballRadius <= 0:
            ballYSpeed *= -1
            ballYSpeed *= speed_multiplier
            ballXSpeed *= speed_multiplier
    else:
        if ballY - ballRadius <= racket2Y + racketHeight and ballY + ballRadius >= racket2Y:
            if ballX >= racket2X and ballX <= racket2X + racketWidth:
                ballYSpeed = abs(ballYSpeed) * speed_multiplier
                ballXSpeed *= speed_multiplier
                return

    if ballX - ballRadius <= 0:
        ballXSpeed = abs(ballXSpeed) * speed_multiplier
        ballYSpeed *= speed_multiplier

    if ballX + ballRadius >= x:
        ballXSpeed = -abs(ballXSpeed) * speed_multiplier
        ballYSpeed *= speed_multiplier

    if ballY + ballRadius >= racketY and ballY <= racketY + racketHeight:
        if ballX >= racketX and ballX <= racketX + racketWidth:
            ballYSpeed = -abs(ballYSpeed) * speed_multiplier
            ballXSpeed *= speed_multiplier
            return 

    if game_mode == 1:
        if ballY - ballRadius > racketY + racketHeight:
            reset()
    else:
        if ballY - ballRadius > racketY + racketHeight or ballY + ballRadius < racket2Y:
            reset()


def moveRacket():
    global racketX
    racketX += speed


def moveRacket2():
    global racket2X
    racket2X += speed2


while in_menu and run:
    screen.fill((0, 0, 0))

    highscore_val = get_highscore()
    title = large_font.render("Wähle Modus:", True, (255, 255, 255))
    p1_option = font.render("Drücke 1 für 1P", True, (255, 40, 0))
    p2_option = font.render("Drücke 2 für 2P", True, (0, 40, 255))
    hs_text = font.render(f"Highscore: {format_time(highscore_val)}", True, (255, 255, 0))

    screen.blit(title, (x // 2 - title.get_width() // 2, int(y * 0.2)))
    screen.blit(p1_option, (x // 2 - p1_option.get_width() // 2, int(y * 0.4)))
    screen.blit(p2_option, (x // 2 - p2_option.get_width() // 2, int(y * 0.5)))
    screen.blit(hs_text, (x // 2 - hs_text.get_width() // 2, int(y * 0.65)))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            in_menu = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                in_menu = False
            if event.key == pygame.K_1:
                game_mode = 1
                in_menu = False
                ballXSpeed = 3.5
                ballYSpeed = -4.5
                start_time = pygame.time.get_ticks()
                item_spawn_timer = pygame.time.get_ticks() 
                life_lost_time_offset = 0
            if event.key == pygame.K_2:
                game_mode = 2
                in_menu = False
                ballXSpeed = random.choice([-2, 2])
                ballYSpeed = random.choice([-3, 3])

while run:
    current_ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_LEFT:
                speed = -8
            if event.key == pygame.K_RIGHT:
                speed = 8
            if game_mode == 2:
                if event.key == pygame.K_a:
                    speed2 = -8
                if event.key == pygame.K_d:
                    speed2 = 8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                speed = 0
            if game_mode == 2:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    speed2 = 0

    if winner_text != "":
        break

    screen.fill((0, 0, 0))

    if game_mode == 1:
        seconds = (current_ticks - start_time) // 1000
        seconds_since_reset = (current_ticks - start_time - life_lost_time_offset) // 1000
        
        intervals = max(0, seconds_since_reset // 20)
        shrink_factor = max(0.5, 1.0 - (intervals * 0.05))
        
        if green_timer > current_ticks:
            racketWidth = int((START_RACKET_WIDTH * shrink_factor) * 2)
        else:
            racketWidth = int(START_RACKET_WIDTH * shrink_factor)
            
        racketHeight = int(START_RACKET_HEIGHT * shrink_factor)
        
        if blue_timer > current_ticks:
            ballRadius = int((START_BALL_RADIUS * shrink_factor) * 2)
        else:
            ballRadius = int(START_BALL_RADIUS * shrink_factor)

        if current_ticks - item_spawn_timer >= 20000:
            item_spawn_timer = current_ticks 
            
            item_x = random.randint(30, x - 30)
            rand_percent = random.randint(1, 100)
            
            if rand_percent <= 40:        
                item_type = "green"
            elif rand_percent <= 70:      
                item_type = "blue"
            else:                                         
                item_type = "red"
                
            items.append({"x": item_x, "y": 0, "type": item_type})

        for item in items[:]:
            item["y"] += 3
            
            if item["type"] == "green":
                color = (0, 255, 0)
            elif item["type"] == "red":
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)
                
            pygame.draw.circle(screen, color, (item["x"], item["y"]), 15)

            if item["y"] + 15 >= racketY and item["y"] - 15 <= racketY + racketHeight:
                if item["x"] >= racketX and item["x"] <= racketX + racketWidth:
                    if item["type"] == "green":
                        green_timer = current_ticks + 5000
                    elif item["type"] == "red":
                        lives += 1
                    elif item["type"] == "blue":
                        blue_timer = current_ticks + 5000 
                    items.remove(item)
                    continue

            if item["y"] > y:
                items.remove(item)

        time_text = font.render(f"Zeit: {format_time(seconds)}", True, (255, 255, 255))
        p1_lives_text = font.render(f"Leben: {lives}", True, (255, 40, 0))
        screen.blit(time_text, (20, 20))
        screen.blit(p1_lives_text, (20, y - p1_lives_text.get_height() - 20))
    else:
        p1_lives_text = font.render(f"P1 (Rot): {lives}", True, (255, 40, 0))
        p2_lives_text = font.render(f"P2 (Blau): {lives2}", True, (0, 40, 255))
        screen.blit(p1_lives_text, (20, y - p1_lives_text.get_height() - 20))
        screen.blit(p2_lives_text, (20, 20))

    moveRacket()
    racketBlock()
    pygame.draw.rect(
        screen, (255, 40, 0), (racketX, racketY, racketWidth, racketHeight), 0
    )

    if game_mode == 2:
        moveRacket2()
        racket2Block()
        pygame.draw.rect(
            screen,
            (0, 40, 255),
            (racket2X, racket2Y, racketWidth, racketHeight),
            0,
        )

    moveBall()
    ballBlock()
    pygame.draw.circle(screen, (255, 255, 0), (int(ballX), int(ballY)), ballRadius, 0)
    pygame.display.flip()
    pygame.time.wait(5)

if winner_text != "" and run:
    screen.fill((0, 0, 0))
    end_text = large_font.render(winner_text, True, (255, 255, 255))
    screen.blit(end_text, (x // 2 - end_text.get_width() // 2, y // 2 - end_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(5000)

pygame.quit()