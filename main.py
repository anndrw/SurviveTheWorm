import pygame
import time
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600 # Dimensiunile ferestrei
FPS = 60 # Frame rate
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # Creaza fereastra
pygame.display.set_caption("Survive the worm!")
BG = pygame.image.load('bg.jpg')

PL_IMG = pygame.image.load('player.png').convert_alpha() # Incarca imaginea jucatorului
EN_IMG = pygame.image.load('enemy.png')         # Incarca imaginea inamicului
HT_IMG = pygame.image.load('heart.png')         # Incarca imaginea inimii
# Pictograma
ICON = pygame.image.load('logo.png')
pygame.display.set_icon(ICON)

attack_sound = pygame.mixer.Sound('attack.mp3')  # Sunetul pentru coliziune
regen_sound = pygame.mixer.Sound('regen.mp3')   # Sunetul pentru regenerare
game_sound = pygame.mixer.Sound('7. Strange.wav')     # Sunetul pentru joc
game_sound.set_volume(0.1)
attack_sound.set_volume(0.5)
regen_sound.set_volume(0.5)

HP = 30

PL_WIDTH, PL_HEIGHT = 40, 40    # Dimensiunile jucatorului
EN_WIDTH, EN_HEIGHT = 25, 25    # Dimensiunile inamicului
HT_WIDTH, HT_HEIGHT = 25, 25    # Dimensiunile inimii

FONT = pygame.font.Font('FFFFORWA.TTF', 12) # Fontul pentru text

def draw_menu():
    WINDOW.blit(BG, (0, 0))

    title_text = FONT.render("Survive the worm!", 1, "yellow")
    WINDOW.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 3))

    info_text = FONT.render("Selectati dificultatea! Imediat ce apasati o sa inceapa jocul.", 1, "white")
    WINDOW.blit(info_text, (WIDTH / 2 - info_text.get_width() / 2, HEIGHT / 2 - 50))

    easy_text = FONT.render("Apasati E pentru Easy", 1, "white")
    WINDOW.blit(easy_text, (WIDTH / 2 - easy_text.get_width() / 2, HEIGHT / 2 - 20))

    hard_text = FONT.render("Apasati H pentru Hard", 1, "white")
    WINDOW.blit(hard_text, (WIDTH / 2 - hard_text.get_width() / 2, HEIGHT / 2 + 20))

    warning_text = FONT.render("Atentie! Dupa secunda 30 apar mai multi inamici indiferent de dificultate!", 1, "yellow")
    WINDOW.blit(warning_text, (WIDTH / 2 - warning_text.get_width() / 2, HEIGHT / 2 + 60))

    pygame.display.update()

def draw(player, elapsed_time, enemies, hearts):
    WINDOW.blit(BG, (0, 0))

    time_text = FONT.render(f"Timp: {round(elapsed_time)}s", 1, "green")
    WINDOW.blit(time_text, (25, 25))
    WINDOW.blit(PL_IMG, (player.x, player.y)) # Deseneaza jucatorul
    for enemy in enemies:
        WINDOW.blit(EN_IMG, (enemy.x, enemy.y)) # Deseneaza inamicul
    for heart in hearts:
        WINDOW.blit(HT_IMG, (heart.x, heart.y))
    draw_hp_bar()

    pygame.display.update() # Actualizeaza ecranul

def draw_hp_bar():
    pygame.draw.rect(WINDOW, (255, 0, 0), (680, 25, HP * 3, 20)) # Deseneaza bara rosie pentru viata

def main():
    draw_menu()  # Afiseaza meniul de start
    game_sound.play(-1)  # Porneste muzica de fundal
    enemies_add_increment = 0
    hearts_add_increment = 0
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Easy mode
                    waiting = False
                    enemies_add_increment = 1200
                elif event.key == pygame.K_h:  # Hard mode
                    waiting = False
                    enemies_add_increment = 700

    run = True

    player = pygame.Rect(50, 50, PL_WIDTH, PL_HEIGHT)
    clock = pygame.time.Clock() # Ceasul pentru FPS

    start_time = time.time()
    elapsed_time = 0

    enemies_count = 0
    enemies = []
    hit = False

    hearts_count = 0
    hearts = []
    hit = False

    while run:
        enemies_count += clock.tick(FPS)
        elapsed_time = time.time() - start_time

        if enemies_count > enemies_add_increment:
            for _ in range(random.randint(1, 3)):
                enemy = pygame.Rect(random.randint(0, WIDTH - EN_WIDTH), random.randint(0, HEIGHT - EN_HEIGHT), EN_WIDTH, EN_HEIGHT)
                enemies.append(enemy)

            enemies_add_increment = max(1000, enemies_add_increment - 100)
            enemies_count = 0

        # Adauga inima si incrementare generare inimi
        hearts_count += clock.tick(FPS)
        if hearts_count > hearts_add_increment:
            for _ in range(random.randint(1, 2)):
                heart = pygame.Rect(random.randint(0, WIDTH - HT_WIDTH), random.randint(0, HEIGHT - HT_HEIGHT), HT_WIDTH, HT_HEIGHT)
                hearts.append(heart)

            hearts_add_increment = max(4000, hearts_add_increment - 100)
            hearts_count = 0



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x > 0:
            player.x -= 3
        if keys[pygame.K_d] and player.x < WIDTH - PL_WIDTH:
            player.x += 3
        if keys[pygame.K_w] and player.y > 0:
            player.y -= 3
        if keys[pygame.K_s] and player.y < HEIGHT - PL_HEIGHT:
            player.y += 3

        for enemy in enemies[:]:
            enemy.y += 1
            if player.colliderect(enemy):
                hit = True
                enemies.remove(enemy)
                if hit:
                    global HP
                    HP -= 10
                    hit = False
                    attack_sound.play()
                else:
                    if HP < 30:
                        HP += 1
                if HP > 30:
                    HP = 30
                if HP <= 0:
                    lost_text = FONT.render("Ai pierdut!", 1, "white")
                    WINDOW.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
                    pygame.display.update()
                    pygame.time.delay(3000)
                    run = False
            if enemy.y > HEIGHT:
                enemies.remove(enemy)

        # Verifica daca jucatorul a colectat inima si ii creste HP-ul cu 5 unitati
        for heart in hearts[:]:
            heart.y += 1
            if player.colliderect(heart):
                hearts.remove(heart)
                HP += 5
                regen_sound.play()
                if HP > 30:
                    HP = 30
            if heart.y > HEIGHT:
                hearts.remove(heart)


        if time.time() - start_time > 60:
            win_text = FONT.render("Ai castigat!", 1, "green")
            WINDOW.blit(win_text, (WIDTH / 2 - win_text.get_width() / 2, HEIGHT / 2 - win_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False



        if time.time() - start_time > 30:
            enemies_add_increment = 400

        draw(player, elapsed_time, enemies, hearts)

    pygame.quit()


if __name__ == "__main__":
    main()
