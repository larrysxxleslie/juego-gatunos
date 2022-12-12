import pygame
import os
pygame.font.init()
pygame.mixer.init()

""" git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/larrysxxleslie/juego-gatunos.git
git push -u origin main """

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Primer juego chavales")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 3, HEIGHT)

HAIR_BALL_HIT_SOUND = pygame.mixer.Sound('Assets/hit_sound.mp3')
HAIR_BALL_SHOOT_SOUND = pygame.mixer.Sound('Assets/hair_ball_sound.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)

FPS = 60
VEL = 5
HAIR_BALL_VEL = 7
MAX_HAIR_BALL = 5
GATO_WIDTH, GATO_HEIGHT = 110, 80
MAX_SCORE = 0

LARRY_HIT = pygame.USEREVENT + 1
BURRITA_HIT = pygame.USEREVENT + 2

GATO_LARRY_IMAGE = pygame.image.load(
    os.path.join('Assets', 'larry.png'))
GATO_LARRY = pygame.transform.scale(
    GATO_LARRY_IMAGE, (GATO_WIDTH, GATO_HEIGHT))

GATO_BURRITA_IMAGE = pygame.image.load(
    os.path.join('Assets', 'burrita.png'))

GATO_BURRITA = pygame.transform.scale(
    GATO_BURRITA_IMAGE, (GATO_WIDTH, GATO_HEIGHT))

PATIO = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'patio.jpg')), (WIDTH, HEIGHT))


def draw_window(burrita, larry, burrita_hair_balls, larry_hair_balls, burrita_health, larry_health):
    WIN.blit(PATIO, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    burrita_health_text = HEALTH_FONT.render(
        "Vida: " + str(burrita_health), 1, BLACK)
    larry_health_text = HEALTH_FONT.render(
        "Vida: " + str(larry_health), 1, BLACK)
    max_score_text = HEALTH_FONT.render(
        "Max score: " + str(MAX_SCORE), 1, BLACK)
    WIN.blit(burrita_health_text, (WIDTH - burrita_health_text.get_width() - 10, 10))
    WIN.blit(larry_health_text, (10, 10))
    WIN.blit(max_score_text, (WIDTH/2- (max_score_text.get_width()/2), 10))

    WIN.blit(GATO_LARRY, (larry.x, larry.y))
    WIN.blit(GATO_BURRITA, (burrita.x, burrita.y))

    for hair_ball in burrita_hair_balls:
        pygame.draw.rect(WIN, RED, hair_ball)

    for hair_ball in larry_hair_balls:
        pygame.draw.rect(WIN, YELLOW, hair_ball)

    pygame.display.update()

""" Esta funcion controla el movimiento de la nave amarrilla """
def larry_handle_movement(keys_pressed, larry):
    if keys_pressed[pygame.K_a] and larry.x - VEL > 0:  # LEFT
        larry.x -= VEL
    if keys_pressed[pygame.K_d] and larry.x + VEL + larry.width < BORDER.x:  # RIGHT
        larry.x += VEL
    if keys_pressed[pygame.K_w] and larry.y - VEL > 0:  # UP
        larry.y -= VEL
    if keys_pressed[pygame.K_s] and larry.y + VEL + larry.height < HEIGHT - 15:  # DOWN
        larry.y += VEL


def burrita_handle_movement(keys_pressed, burrita):
    if keys_pressed[pygame.K_LEFT] and burrita.x - VEL > BORDER.x + BORDER.width:  # LEFT
        burrita.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and burrita.x + VEL + burrita.width < WIDTH:  # RIGHT
        burrita.x += VEL
    if keys_pressed[pygame.K_UP] and burrita.y - VEL > 0:  # UP
        burrita.y -= VEL
    if keys_pressed[pygame.K_DOWN] and burrita.y + VEL + burrita.height < HEIGHT - 15:  # DOWN
        burrita.y += VEL


def handle_hair_ball(larry_hair_balls, burrita_hair_balls, larry, burrita):
    for hair_ball in larry_hair_balls:
        hair_ball.x += HAIR_BALL_VEL
        if burrita.colliderect(hair_ball):
            pygame.event.post(pygame.event.Event(BURRITA_HIT))
            larry_hair_balls.remove(hair_ball)
        elif hair_ball.x > WIDTH:
            larry_hair_balls.remove(hair_ball)

    for hair_ball in burrita_hair_balls:
        hair_ball.x -= HAIR_BALL_VEL
        if larry.colliderect(hair_ball):
            pygame.event.post(pygame.event.Event(LARRY_HIT))
            burrita_hair_balls.remove(hair_ball)
        elif hair_ball.x < 0:
            burrita_hair_balls.remove(hair_ball)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    global MAX_SCORE
    burrita = pygame.Rect(700, 300, GATO_WIDTH, GATO_HEIGHT)
    larry = pygame.Rect(100, 300, GATO_WIDTH, GATO_HEIGHT)

    burrita_hair_balls = []
    larry_hair_balls = []

    burrita_health = 10
    larry_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(larry_hair_balls) < MAX_HAIR_BALL:
                    hair_ball = pygame.Rect(
                        larry.x + larry.width, larry.y + larry.height//2 - 2, 10, 5)
                    larry_hair_balls.append(hair_ball)
                    HAIR_BALL_SHOOT_SOUND.play()

                if event.key == pygame.K_RCTRL and len(burrita_hair_balls) < MAX_HAIR_BALL:
                    hair_ball = pygame.Rect(
                        burrita.x, burrita.y + burrita.height//2 - 2, 10, 5)
                    burrita_hair_balls.append(hair_ball)
                    HAIR_BALL_SHOOT_SOUND.play()

            if event.type == BURRITA_HIT:
                burrita_health -= 1
                HAIR_BALL_HIT_SOUND.play()

            if event.type == LARRY_HIT:
                larry_health -= 1
                HAIR_BALL_HIT_SOUND.play()

        winner_text = ""
        if burrita_health <= 0:
            winner_text = "Larry Gana.Puntuación" + str(larry_health)
            if larry_health > MAX_SCORE:
                MAX_SCORE = larry_health

        if larry_health <= 0:
            winner_text = "Burrita Gana. Puntuación:"+ str(burrita_health)
            if burrita_health > MAX_SCORE:
                MAX_SCORE = burrita_health

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        larry_handle_movement(keys_pressed, larry)
        burrita_handle_movement(keys_pressed, burrita)

        handle_hair_ball(larry_hair_balls, burrita_hair_balls, larry, burrita)

        draw_window(burrita, larry, burrita_hair_balls, larry_hair_balls,
                    burrita_health, larry_health)

    main()


if __name__ == "__main__":
    main()