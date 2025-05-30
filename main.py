from operator import truediv
import math
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
info_screen = False
settings = False
wasd = True
nooled = False

fps = 60

# Taustamuusika
song = pygame.mixer.Sound("TokyoDrift.mp3")
explosion_sound = pygame.mixer.Sound("explosion2.mp3")
soundON = pygame.image.load("SoundON.png")
soundON = pygame.transform.scale(soundON, (50, 50))
soundOFF = pygame.image.load("SoundOFF.png")
soundOFF = pygame.transform.scale(soundOFF, (50, 50))

music_volume = 0.02
sfx_volume = 1.0
song.set_volume(music_volume)
explosion_sound.set_volume(sfx_volume)

slider_rect = pygame.Rect(150, 300, 300, 10)
handle_rect = pygame.Rect(150 + 300 * song.get_volume(), 290, 10, 30)
dragging_slider = False

# Pildid
mainmenu_taust = pygame.image.load("Main_menu.png")
mainmenu_taust = pygame.transform.scale(mainmenu_taust, (width, height))
death_taust = pygame.image.load("Death_screen.png")
death_taust = pygame.transform.scale(death_taust, (width, height))
info_taust = pygame.image.load("Scroll_info.png")
info_taust = pygame.transform.scale(info_taust, (width, height))
settings_background = pygame.image.load("Scroll.png")
settings_background = pygame.transform.scale(settings_background, (width, height))
background = pygame.image.load("Highway.png")
background = pygame.transform.scale(background, (width, height))
tausty = 0
background_speed = 8
saved_background_speed = background_speed

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

coin_img = pygame.image.load("Coin.png")
coin_img = pygame.transform.scale(coin_img, (175, 175))

coin_lane = random.choice([i for i in range(len(lanes)) if lanes[i] != obstacle_x])
coin_x = lanes[coin_lane]
coin_base_y = obstacle_y - 100
coin_y = coin_base_y
coin_amplitude = 10
coin_phase = 0
coin_counter = 0

score = 0

coin_collected = False
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

    elif info_screen:
        #infoekraan
        ekraan.blit(info_taust, (0,0))
        back_main_color = [0, 255, 0] if 550 < mouse_x < 600 and 0 < mouse_y < 50 else [0, 0, 0]
        back_main = pygame.draw.rect(ekraan, back_main_color, [550, 0, 50, 50], 2)
        back_main_kiri = teksti_font.render("X", 1, back_main_color)
        ekraan.blit(back_main_kiri, [564, 10])

    elif settings:
        ekraan.blit(settings_background, (0, 0))
        # Muusika heli muutmine
        music_text = teksti_font.render("Music Volume", 1, [0, 0, 0])
        ekraan.blit(music_text, [100, 300])
        pygame.draw.rect(ekraan, [100, 100, 100], [300, 310, 200, 10])
        pygame.draw.rect(ekraan, [0, 255, 0], [300, 310, int(music_volume * 200), 10])
        pygame.draw.circle(ekraan, [0, 0, 0], [300 + int(music_volume * 200), 315], 8)

        # SFX heli muutmine
        sfx_text = teksti_font.render("SFX Volume", 1, [0, 0, 0])
        ekraan.blit(sfx_text, [100, 350])
        pygame.draw.rect(ekraan, [100, 100, 100], [300, 360, 200, 10])
        pygame.draw.rect(ekraan, [255, 0, 0], [300, 360, int(sfx_volume * 200), 10])
        pygame.draw.circle(ekraan, [0, 0, 0], [300 + int(sfx_volume * 200), 365], 8)
        # tagasi main menüü
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
        # Näitab lõpliku score
        score_text = teksti_font.render(f"Score: {score}", 1, [0, 0, 0])
        ekraan.blit(score_text, (width // 2 - score_text.get_width() // 2, 300))
        # Näitab palju coine said
        coin_text = teksti_font.render(f"Coins: {coin_counter}", 1, [0, 0, 0])
        ekraan.blit(coin_text, (width // 2 - coin_text.get_width() // 2, 340))


    else:
        # Paneb tausta liikuma
        ekraan.blit(background, (0, tausty))
        ekraan.blit(background, (0, tausty - height))
        tausty += background_speed
        if tausty >= height:
            tausty = 0

        if gaming:
            # Mängu joonistamine
            ekraan.blit(car_img, (car_x, car_y))
            ekraan.blit(roadblock_img, (obstacle_x, obstacle_y))

            # kas sätetest on valitud nooled
            if nooled:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and car_x > width // 5:
                    car_x -= car_speed
                if keys[pygame.K_RIGHT] and car_x < width // 3.75 * 3 - car_width:
                    car_x += car_speed
            # kas sätetest on valitud wasd nupud
            if wasd:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and car_x > width // 5:
                    car_x -= car_speed
                if keys[pygame.K_d] and car_x < width // 3.75 * 3 - car_width:
                    car_x += car_speed

            obstacle_y += obstacle_speed
            coin_base_y += obstacle_speed

            #kontrollib kas coin on collectitud
            if not coin_collected:
                coin_phase += 0.1
                coin_y = coin_base_y + math.sin(coin_phase) * 10

                coin_rect = pygame.Rect(coin_x + (obstacle_width - 50) // 2, coin_y + 125, 50, 50)
                car_rect = pygame.Rect(car_x, car_y, car_width, car_height)

                if car_rect.colliderect(coin_rect):
                    coin_counter += 1
                    score += 50
                    coin_collected = True
                else:
                    ekraan.blit(coin_img, (coin_x + (obstacle_width - 170) // 2, coin_y + 50))

            # teeb auto kiiremaks kui tõkkest mööda läheb
            if obstacle_y > height:
                obstacle_y = -obstacle_height
                obstacle_x = random.choice(lanes)
                obstacle_speed += 0.2
                car_speed += 0.1
                background_speed += 0.2
                score += 10

                obstacle_lane = lanes.index(obstacle_x)
                coin_lane = random.choice([i for i in range(len(lanes)) if i != obstacle_lane])
                coin_x = lanes[coin_lane]
                coin_base_y = obstacle_y - 100
                coin_y = coin_base_y
                coin_collected = False
                coin_phase = 0

            score_text = teksti_font.render(f"Score: {score}", 1, [0, 0, 0])
            ekraan.blit(score_text, (55, 5))

        # Kokkupõrke kontroll
        if (car_x < obstacle_x + obstacle_width-30 and car_x + car_width-20 > obstacle_x and car_y < obstacle_y + obstacle_height-20 and car_y + car_height-20 > obstacle_y):
            explosion_sound.play()
            death = True
            gaming = False
            slowmotion = False
            obstacle_speed = 8
            background_speed = 8
            car_speed = 5

        # kui slowmotion on aktiivne
        if slowmotion:
            background_speed = 2
            obstacle_speed = 2

    #paneb muusike käima ja kinni
    music_color = [0, 255, 0] if 0 < mouse_x < 50 and 0 < mouse_y < 50 else [0, 0, 0]
    pygame.draw.rect(ekraan, music_color, [0, 0, 50, 50], 2)
    if music == True:
        ekraan.blit(soundON, (0, 0))
    elif music == False:
        ekraan.blit(soundOFF, (0, 0))

    # Versioon
    version = teksti_font_versioon.render("v0.01", 1, [50, 0, 255])
    ekraan.blit(version, (2, 780))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

        # Spacebar paneb tööle aekluubi
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                slowmotion = not slowmotion
                if slowmotion:
                    #Salvestab kiiruse enne aekluubi
                    saved_background_speed = background_speed
                    saved_obstacle_speed = obstacle_speed
                    saved_car_speed = car_speed

                    background_speed = max(1, background_speed // 4)
                    obstacle_speed = max(1, obstacle_speed // 4)
                    car_speed = max(1, 5)
                else:
                    background_speed = saved_background_speed
                    obstacle_speed = saved_obstacle_speed
                    car_speed = saved_car_speed

        elif i.type == pygame.MOUSEBUTTONDOWN:
            hiir_x, hiir_y = i.pos

            if info_screen:
                if 550 < hiir_x < 600 and 0 < hiir_y < 50:
                    info_screen = False
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

                if 300 <= hiir_x <= 500 and 310 - 10 <= hiir_y <= 310 + 10:
                    music_volume = (hiir_x - 300) / 200
                    song.set_volume(music_volume)

                if 300 <= hiir_x <= 500 and 360 - 10 <= hiir_y <= 360 + 10:
                    sfx_volume = (hiir_x - 300) / 200
                    explosion_sound.set_volume(sfx_volume)



            elif main_menu:
                if 225 < hiir_x < 375 and 280 < hiir_y < 360:
                    main_menu = False
                    gaming = True
                    coin_counter = 0
                    score = 0
                if 225 < hiir_x < 375 and 380 < hiir_y < 460:
                    settings = True
                    main_menu = False
                if 225 < hiir_x < 375 and 480 < hiir_y < 560:
                    running = False
                if 550 < hiir_x < 600 and 0 < hiir_y < 50:
                    info_screen = True
                    main_menu = False

            elif death:
                if 210 < hiir_x < 375 and 390 < hiir_y < 470:
                    death = False
                    gaming = True
                    car_x, car_y = width // 2 - car_width // 2, height - car_height - 20
                    obstacle_x = random.choice(lanes)
                    obstacle_y = -obstacle_height
                    coin_base_x = random.choice(lanes)
                    coin_counter = 0
                    score = 0

                if 210 < hiir_x < 375 and 490 < hiir_y < 570:
                    main_menu = True
                    death = False
                    car_x, car_y = width // 2 - car_width // 2, height - car_height - 20
                    obstacle_x = random.choice(lanes)
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