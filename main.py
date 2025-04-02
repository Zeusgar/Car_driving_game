import pygame
import random

pygame.init()
width, height = 600, 800
ekraan = pygame.display.set_mode([width, height])
pygame.display.set_caption("Endless Car Driving Simulator")
clock = pygame.time.Clock()
ekraan.fill([255,255,255])
teksti_font = pygame.font.Font(None, 50)
teksti_font_versioon = pygame.font.Font(None, 30)
main_menu = True
running = True
death = False
gaming = False
music = False
musicKuva = True
slowmotion = False

fps = 60

#Taustamuusika
song = pygame.mixer.Sound("Mortals.mp3")
soundON = pygame.image.load("SoundON.png")
soundON = pygame.transform.scale(soundON, (50, 50))
soundOFF = pygame.image.load("SoundOFF.png")
soundOFF = pygame.transform.scale(soundOFF, (50, 50))

# Pildid
mainmenu_taust = pygame.image.load("Taust_mainmenu.jpg")
mainmenu_taust = pygame.transform.scale(mainmenu_taust, (width, height))
taust = pygame.image.load("Highway.png")
taust = pygame.transform.scale(taust, (width, height))
tausty = 0
taust_speed = 8
saved_taust_speed = taust_speed

car_img = pygame.image.load("Auto.png")
car_width, car_height = 80, 120
car_img = pygame.transform.scale(car_img, (car_width, car_height))

roadblock_img = pygame.image.load("Roadblock.png")
roadblock_width, roadblock_height = 150, 110
roadblock_img = pygame.transform.scale(roadblock_img, (roadblock_width, roadblock_height))

# Auto seaded
car_x, car_y = width // 2 - car_width // 2, height - car_height - 20
car_speed = 5
saved_car_speed = car_speed

# Tee peal olevad takistused
obstacle_width, obstacle_height = roadblock_width, roadblock_height
obstacle_x = random.randint(width // 5, width // 5 * 4 - obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed = 8
saved_obstacle_speed = obstacle_speed

while running:
    ekraan.fill([255, 255, 255])
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Main menu
    if main_menu:
        ekraan.blit(mainmenu_taust, (0,0))
        # Start
        start_color = [0, 255, 0] if 225 < mouse_x < 375 and 240 < mouse_y < 320 else [0, 0, 0]
        pygame.draw.rect(ekraan, start_color, [225, 240, 150, 80], 5)
        tekst_pildina = teksti_font.render("Start", 1, start_color)
        ekraan.blit(tekst_pildina,[(width / 2) - tekst_pildina.get_size()[0] / 2, (height / 2) - 100 - tekst_pildina.get_size()[1]])
        # Lõpeta programm
        close_color = [0, 255, 0] if 225 < mouse_x < 375 and 340 < mouse_y < 420 else [0, 0, 0]
        pygame.draw.rect(ekraan, close_color, [225, 340, 150, 80], 5)
        tekst_pildina2 = teksti_font.render("Close", 1, close_color)
        ekraan.blit(tekst_pildina2,[(width / 2) - tekst_pildina2.get_size()[0] / 2, (height / 2) - tekst_pildina2.get_size()[1]])
        #Versioon
        versioon = teksti_font_versioon.render("v1.0", 1, [50,0,255])
        ekraan.blit(versioon, (2, 780))

    elif death:
        ekraan.blit(mainmenu_taust, (0, 0))
        # Restart
        restart_color = [0, 255, 0] if 225 < mouse_x < 375 and 240 < mouse_y < 320 else [0, 0, 0]
        pygame.draw.rect(ekraan, restart_color, [225, 240, 150, 80], 5)
        tekst_pildina3 = teksti_font.render("Restart", 1, restart_color)
        ekraan.blit(tekst_pildina3,[(width / 2) - tekst_pildina3.get_size()[0] / 2, (height / 2) - 100 - tekst_pildina3.get_size()[1]])
        # Lõpeta programm
        close_color = [0, 255, 0] if 225 < mouse_x < 375 and 340 < mouse_y < 420 else [0, 0, 0]
        pygame.draw.rect(ekraan, close_color, [225, 340, 150, 80], 5)
        tekst_pildina4 = teksti_font.render("Close", 1, close_color)
        ekraan.blit(tekst_pildina4,[(width / 2) - tekst_pildina4.get_size()[0] / 2, (height / 2) - tekst_pildina4.get_size()[1]])


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
            slowmotion = False
            obstacle_speed = 8
            taust_speed = 8
            car_speed = 5


        if slowmotion:
            taust_speed = 2
            obstacle_speed = 2

    pygame.draw.rect(ekraan, [0, 0, 0], [0, 0, 50, 50], 2)
    if music == True:
        ekraan.blit(soundON, (0, 0))
    elif music == False:
        ekraan.blit(soundOFF, (0, 0))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

        #Auto liigub kiiremini kui vajutad K_UP ja liigu aeglasemalt kui vajutad  K_DOWN, spacebar paneb tööle aekluubi
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_UP:
                obstacle_speed += 2
                taust_speed += 2
                car_speed += 0.5
            elif i.key == pygame.K_DOWN:
                if obstacle_speed == 0:
                    pass
                else:
                    obstacle_speed -= 2
                    taust_speed -= 2
                    car_speed -= 0.5
            elif i.key == pygame.K_SPACE:
                slowmotion = not slowmotion
                if slowmotion:
                    #Salvestab kiiruse enne aekluubi
                    saved_taust_speed = taust_speed
                    saved_obstacle_speed = obstacle_speed
                    saved_car_speed = car_speed

                    taust_speed = max(1, taust_speed // 4)
                    obstacle_speed = max(1, obstacle_speed // 4)
                    car_speed = max(1, 5)
                else:
                    taust_speed = saved_taust_speed
                    obstacle_speed = saved_obstacle_speed
                    car_speed = saved_car_speed

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

            if musicKuva:
                if hiir_x > 0 and hiir_x < 50 and hiir_y > 0 and hiir_y < 50:
                    if music == False:
                        song.play()
                        music = True
                    elif music == True:
                        song.stop()
                        music = False
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()