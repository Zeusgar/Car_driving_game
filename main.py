import pygame
import random

pygame.init()
width, height = 600, 800
ekraan = pygame.display.set_mode([width, height])
pygame.display.set_caption("2D Car Driving Simulator")
clock = pygame.time.Clock()
ekraan.fill([255,255,255])
teksti_font = pygame.font.Font(None, 50)
main_menu = True
running = True
death = False
gaming = False
music = True


fps = 60

#Taustamuusika
song = pygame.mixer.Sound("Mortals.mp3")
soundON = pygame.image.load("SoundON.png")
soundON = pygame.transform.scale(soundON, (50, 50))
soundOFF = pygame.image.load("SoundOFF.png")
soundOFF = pygame.transform.scale(soundOFF, (50, 50))
if music == False:
    song.play()
    muusika = True
elif music == True:
    song.stop()
    muusika = False

# Pildid
taust = pygame.image.load("Highway.png")
taust = pygame.transform.scale(taust, (width, height))
tausty = 0
taust_speed = 8

car_img = pygame.image.load("Auto.png")
car_width, car_height = 80, 120
car_img = pygame.transform.scale(car_img, (car_width, car_height))

roadblock_img = pygame.image.load("Roadblock.png")
roadblock_width, roadblock_height = 150, 110
roadblock_img = pygame.transform.scale(roadblock_img, (roadblock_width, roadblock_height))

# Auto seaded
car_x, car_y = width // 2 - car_width // 2, height - car_height - 20
car_speed = 5

# Tee peal olevad takistused
obstacle_width, obstacle_height = roadblock_width, roadblock_height
obstacle_x = random.randint(width // 5, width // 5 * 4 - obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed = 8

while running:
    ekraan.fill([255, 255, 255])
    # Main menu

    if main_menu:

        # Start
        pygame.draw.rect(ekraan, [0, 0, 0], [225, 240, 150, 80], 2)
        tekst_pildina = teksti_font.render("Start", 1, [0, 0, 0])
        ekraan.blit(tekst_pildina,[(width / 2) - tekst_pildina.get_size()[0] / 2, (height / 2) - 100 - tekst_pildina.get_size()[1]])
        # Lõpeta programm
        pygame.draw.rect(ekraan, [0, 0, 0], [225, 340, 150, 80], 2)
        tekst_pildina2 = teksti_font.render("Close", 1, [0, 0, 0])
        ekraan.blit(tekst_pildina2,[(width / 2) - tekst_pildina2.get_size()[0] / 2, (height / 2) - tekst_pildina2.get_size()[1]])

    elif death:
        # Restart
        pygame.draw.rect(ekraan, [0, 0, 0], [225, 240, 150, 80], 2)
        tekst_pildina3 = teksti_font.render("Restart", 1, [0, 0, 0])
        ekraan.blit(tekst_pildina3,[(width / 2) - tekst_pildina3.get_size()[0] / 2, (height / 2) - 100 - tekst_pildina3.get_size()[1]])
        # Lõpeta programm
        pygame.draw.rect(ekraan, [0, 0, 0], [225, 340, 150, 80], 2)
        tekst_pildina4 = teksti_font.render("Close", 1, [0, 0, 0])
        ekraan.blit(tekst_pildina4,[(width / 2) - tekst_pildina4.get_size()[0] / 2, (height / 2) - tekst_pildina4.get_size()[1]])

    elif music:
        ekraan.blit(soundON, (0, 0))

    else:
        #paneb tausta liikuma
        ekraan.blit(taust, (0, tausty))
        ekraan.blit(taust, (0, tausty - height))
        tausty += taust_speed
        if tausty >= height:
            tausty = 0

        if gaming:
            # Mängu joonistamine
            ekraan.blit(car_img, (car_x, car_y))
            ekraan.blit(roadblock_img, (obstacle_x, obstacle_y))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and car_x > width // 5:
                car_x -= car_speed
            if keys[pygame.K_RIGHT] and car_x < width // 3.75 * 3 - car_width:
                car_x += car_speed

            obstacle_y += obstacle_speed

            if obstacle_y > height:
                obstacle_y = -obstacle_height
                obstacle_x = random.randint(width // 4, width // 4 * 3 - obstacle_width)

        # Kokkupõrke kontroll
        if (car_x < obstacle_x + obstacle_width-30 and car_x + car_width-20 > obstacle_x and car_y < obstacle_y + obstacle_height-20 and car_y + car_height-20 > obstacle_y):
            death = True
            gaming = False
            obstacle_speed = 8
            taust_speed = 8

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

        #Auto liigub kiiremini kui vajutad K_UP ja liigu aeglasemalt kui vajutad  K_DOWN
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_UP:
                obstacle_speed += 2
                taust_speed += 2
            elif i.key == pygame.K_DOWN:
                obstacle_speed -= 2
                taust_speed -= 2

        elif i.type == pygame.MOUSEBUTTONDOWN:
            hiir_x, hiir_y = i.pos
            if main_menu:
                if 225 < hiir_x < 375 and 240 < hiir_y < 420:
                    main_menu = False
                    gaming = True
                if 225 < hiir_x < 375 and 340 < hiir_y < 540:
                    running = False
            if death:
                if 225 < hiir_x < 375 and 240 < hiir_y < 420:
                    death = False
                    gaming = True
                    car_x, car_y = width // 2 - car_width // 2, height - car_height - 20
                    obstacle_x = random.randint(width // 5, width // 5 * 3 - obstacle_width)
                    obstacle_y = -obstacle_height
                if 225 < hiir_x < 375 and 340 < hiir_y < 540:
                    running = False

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()