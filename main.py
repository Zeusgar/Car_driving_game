from operator import truediv

import pygame
import random


pygame.init()
width, height = 600, 800
ekraan = pygame.display.set_mode([width, height])
pygame.display.set_caption("Endless Car Driving Simulator")
clock = pygame.time.Clock()
ekraan.fill([255,255,255])
teksti_font = pygame.font.Font(None, 45)
teksti_font_versioon = pygame.font.Font(None, 30)
main_menu = True
running = True
death = False
gaming = False
music = False
musicKuva = True
slowmotion = False
infoekraan = False
settings = False
wasd = True
nooled = False
res1 = True
res2 = False
res3 = False

fps = 60

# Taustamuusika
song = pygame.mixer.Sound("TokyoDrift.mp3")
song.set_volume(0.02)
soundON = pygame.image.load("SoundON.png")
soundON = pygame.transform.scale(soundON, (50, 50))
soundOFF = pygame.image.load("SoundOFF.png")
soundOFF = pygame.transform.scale(soundOFF, (50, 50))

# Pildid
mainmenu_taust = pygame.image.load("Main_menu.png")
mainmenu_taust = pygame.transform.scale(mainmenu_taust, (width, height))
death_taust = pygame.image.load("Death_screen.png")
death_taust = pygame.transform.scale(death_taust, (width, height))
info_taust = pygame.image.load("Scroll.png")
info_taust = pygame.transform.scale(info_taust, (width, height))
settings_taust = pygame.image.load("Scroll.png")
settings_taust = pygame.transform.scale(settings_taust, (width, height))
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
lane_width = width // 3
lanes = [lane_width -120+ lane_width // 2 - obstacle_width // 2, # vasak rada
        lane_width + lane_width // 2 - obstacle_width // 2, # keskmine rada
         lane_width + 122 + lane_width // 2 - obstacle_width // 2] # parem rada
obstacle_x = random.choice(lanes)
obstacle_y = -obstacle_height
obstacle_speed = 8
saved_obstacle_speed = obstacle_speed

def muuda_resolutsioon(w, h):
    global width, height, ekraan
    global mainmenu_taust, death_taust, info_taust, settings_taust, taust

while running:
    ekraan.fill([255, 255, 255])
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Main menu
    if main_menu:
        ekraan.blit(mainmenu_taust, (0,0))
        # Start
        start_color = [0, 255, 0] if 225 < mouse_x < 375 and 280 < mouse_y < 360 else [0, 0, 0]
        pygame.draw.rect(ekraan, start_color, [225, 280, 150, 80], 5)
        tekst_pildina = teksti_font.render("Start", 1, start_color)
        ekraan.blit(tekst_pildina,[(width / 2) - tekst_pildina.get_size()[0] / 2, (height / 2) - 63 - tekst_pildina.get_size()[1]])
        # Settings
        settings_color = [0, 255, 0] if 225 < mouse_x < 375 and 380 < mouse_y < 460 else [0, 0, 0]
        pygame.draw.rect(ekraan, settings_color, [225, 380, 150, 80], 5)
        tekst_pildina3 = teksti_font.render("Settings", 1, settings_color)
        ekraan.blit(tekst_pildina3,[(width / 2) - tekst_pildina3.get_size()[0] / 2, (height / 2) + 37 - tekst_pildina3.get_size()[1]])
        # Lõpeta programm
        close_color = [255, 0, 0] if 225 < mouse_x < 375 and 480 < mouse_y < 560 else [0, 0, 0]
        pygame.draw.rect(ekraan, close_color, [225, 480, 150, 80], 5)
        tekst_pildina2 = teksti_font.render("Close", 1, close_color)
        ekraan.blit(tekst_pildina2,[(width / 2) - tekst_pildina2.get_size()[0] / 2, (height / 2) + 137 - tekst_pildina2.get_size()[1]])
        # Info
        info_color = [0, 255, 0] if 550 < mouse_x < 600 and 0 < mouse_y < 50 else [0, 0, 0]
        info = pygame.draw.rect(ekraan, info_color, [550, 0, 50, 50], 2)
        info_kiri = teksti_font.render("!", 1, info_color)
        ekraan.blit(info_kiri, [568, 10])

    elif infoekraan:
        ekraan.blit(info_taust, (0,0))
        back_main_color = [0, 255, 0] if 550 < mouse_x < 600 and 0 < mouse_y < 50 else [0, 0, 0]
        back_main = pygame.draw.rect(ekraan, back_main_color, [550, 0, 50, 50], 2)
        back_main_kiri = teksti_font.render("X", 1, back_main_color)
        ekraan.blit(back_main_kiri, [564, 10])

    elif settings:
        ekraan.blit(settings_taust, (0, 0))
        back_main_color = [0, 255, 0] if 550 < mouse_x < 600 and 0 < mouse_y < 50 else [0, 0, 0]
        back_main = pygame.draw.rect(ekraan, back_main_color, [550, 0, 50, 50], 2)
        back_main_kiri = teksti_font.render("X", 1, back_main_color)
        ekraan.blit(back_main_kiri, [564, 10])
        # WASD või NOOLED
        liikumisklahvid = teksti_font.render("Liikumine:", 1, [0,0,0])
        ekraan.blit(liikumisklahvid, [100, 200])
        if wasd:
            wasd_kast = pygame.draw.rect(ekraan, [0,0,0],[260, 190, 150, 50], 2)
            wasd_kiri = teksti_font.render("W,A,S,D", 1, [0,0,0])
            ekraan.blit(wasd_kiri, [(width / 2) + 35 - wasd_kiri.get_size()[0] / 2, (height / 2) - 168 - wasd_kiri.get_size()[1]])
        if nooled:
            nooled_kast = pygame.draw.rect(ekraan, [0,0,0],[260, 190, 150, 50], 2)
            nooled_kiri = teksti_font.render("NOOLED", 1, [0, 0, 0])
            ekraan.blit(nooled_kiri, [(width / 2) + 35 - nooled_kiri.get_size()[0] / 2, (height / 2) - 168 - nooled_kiri.get_size()[1]])
        # Resolutsioon
        resolutsioon = teksti_font.render("Resolutsioon:", 1, [0,0,0])
        ekraan.blit(resolutsioon, [100, 270])
        if res1:
            width, height = 600, 800
            muuda_resolutsioon(600, 800)
            res1_kast = pygame.draw.rect(ekraan, [0, 0, 0], [312, 260, 150, 50], 2)
            res1_kiri = teksti_font.render("600x800", 1, [0, 0, 0])
            ekraan.blit(res1_kiri,[(width / 2) + 88 - res1_kiri.get_size()[0] / 2, (height / 2) - 98 - res1_kiri.get_size()[1]])
        if res2:
            width, height = 800, 1000
            muuda_resolutsioon(800, 1000)
            res2_kast = pygame.draw.rect(ekraan, [0, 0, 0], [312, 260, 150, 50], 2)
            res2_kiri = teksti_font.render("800x1000", 1, [0, 0, 0])
            ekraan.blit(res2_kiri,[(width / 2) + 90 - res2_kiri.get_size()[0] / 2, (height / 2) - 98 - res2_kiri.get_size()[1]])
        if res3:
            width, height = 1000, 1200

    elif death:
        ekraan.blit(death_taust, (0, 0))
        # Restart
        restart_color = [0, 255, 0] if 210 < mouse_x < 390 and 390 < mouse_y < 470 else [0, 0, 0]
        pygame.draw.rect(ekraan, restart_color, [210, 390, 180, 80], 5)
        tekst_pildina3 = teksti_font.render("Restart", 1, restart_color)
        ekraan.blit(tekst_pildina3,[(width / 2) - tekst_pildina3.get_size()[0] / 2, (height / 2) + 50 - tekst_pildina3.get_size()[1]])
        # Main menu
        close_color = [0, 255, 0] if 210 < mouse_x < 390 and 490 < mouse_y < 570 else [0, 0, 0]
        pygame.draw.rect(ekraan, close_color, [210, 490, 180, 80], 5)
        tekst_pildina4 = teksti_font.render("Main Menu", 1, close_color)
        ekraan.blit(tekst_pildina4,[(width / 2) - tekst_pildina4.get_size()[0] / 2, (height / 2) + 150 - tekst_pildina4.get_size()[1]])


    else:
        # Paneb tausta liikuma
        ekraan.blit(taust, (0, tausty))
        ekraan.blit(taust, (0, tausty - height))
        tausty += taust_speed
        if tausty >= height:
            tausty = 0

        if gaming:
            # Mängu joonistamine
            ekraan.blit(car_img, (car_x, car_y))
            ekraan.blit(roadblock_img, (obstacle_x, obstacle_y))

            if nooled:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and car_x > width // 5:
                    car_x -= car_speed
                if keys[pygame.K_RIGHT] and car_x < width // 3.75 * 3 - car_width:
                    car_x += car_speed

            if wasd:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and car_x > width // 5:
                    car_x -= car_speed
                if keys[pygame.K_d] and car_x < width // 3.75 * 3 - car_width:
                    car_x += car_speed

            obstacle_y += obstacle_speed

            if obstacle_y > height:
                obstacle_y = -obstacle_height
                obstacle_x = random.choice(lanes)

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

    music_color = [0, 255, 0] if 0 < mouse_x < 50 and 0 < mouse_y < 50 else [0, 0, 0]
    pygame.draw.rect(ekraan, music_color, [0, 0, 50, 50], 2)
    if music == True:
        ekraan.blit(soundON, (0, 0))
    elif music == False:
        ekraan.blit(soundOFF, (0, 0))

    # Versioon
    versioon = teksti_font_versioon.render("v0.01", 1, [50, 0, 255])
    ekraan.blit(versioon, (2, 780))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

        # Auto liigub kiiremini kui vajutad K_UP ja liigu aeglasemalt kui vajutad  K_DOWN, spacebar paneb tööle aekluubi
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
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

            if infoekraan:
                if 550 < hiir_x < 600 and 0 < hiir_y < 50:
                    infoekraan = False
                    main_menu = True

            elif settings:
                if 550 < hiir_x < 600 and 0 < hiir_y < 50:
                    settings = False
                    main_menu = True

                elif wasd:
                    if 260 < hiir_x < 410 and 190 < hiir_y < 240:
                        wasd = False
                        nooled = True
                elif nooled:
                    if 260 < hiir_x < 410 and 190 < hiir_y < 240:
                        wasd = True
                        nooled = False

                elif res1:
                    if 312 < hiir_x < 462 and 260 < hiir_y < 310:
                        res1 = False
                        res2 = True
                        muuda_resolutsioon(800, 1000)

            elif main_menu:
                if 225 < hiir_x < 375 and 280 < hiir_y < 360:
                    main_menu = False
                    gaming = True
                if 225 < hiir_x < 375 and 380 < hiir_y < 460:
                    settings = True
                    main_menu = False
                if 225 < hiir_x < 375 and 480 < hiir_y < 560:
                    running = False
                if 550 < hiir_x < 600 and 0 < hiir_y < 50:
                    infoekraan = True
                    main_menu = False

            elif death:
                if 210 < hiir_x < 375 and 390 < hiir_y < 470:
                    death = False
                    gaming = True
                    car_x, car_y = width // 2 - car_width // 2, height - car_height - 20
                    obstacle_x = random.randint(width // 5, width // 5 * 3 - obstacle_width)
                    obstacle_y = -obstacle_height
                if 210 < hiir_x < 375 and 490 < hiir_y < 570:
                    main_menu = True
                    death = False
                    car_x, car_y = width // 2 - car_width // 2, height - car_height - 20
                    obstacle_x = random.randint(width // 5, width // 5 * 3 - obstacle_width)
                    obstacle_y = -obstacle_height

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