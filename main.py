import pygame

pygame.init()
ekraan = pygame.display.set_mode([800, 600])
pygame.display.set_caption("2D Car Driving Simulator")
ekraan.fill([255,255,255])
main_menu = True
running = True
teksti_font = pygame.font.Font(None, 50)

while running:
    ekraan.fill([255, 255, 255])
    # Main menu
    if main_menu:

        # Start
        pygame.draw.rect(ekraan, [0, 0, 0], [325, 240, 150, 80], 2)
        tekst_pildina = teksti_font.render("START", 1, [0, 0, 0])
        ekraan.blit(tekst_pildina,[(800 / 2) - tekst_pildina.get_size()[0] / 2, (600 / 2) - tekst_pildina.get_size()[1]])
        # Lõpeta programm
        pygame.draw.rect(ekraan, [0, 0, 0], [325, 340, 150, 80], 2)
        tekst_pildina2 = teksti_font.render("LÕPP", 1, [0, 0, 0])
        ekraan.blit(tekst_pildina2,[(800 / 2) - tekst_pildina2.get_size()[0] / 2, (600 / 2) + 100 - tekst_pildina2.get_size()[1]])




    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        elif i.type == pygame.MOUSEBUTTONDOWN:
            hiir_x, hiir_y = i.pos
            if 325 < hiir_x < 475 and 240 < hiir_y < 320:
                main_menu = False
            if 325 < hiir_x < 475 and 340 < hiir_y < 420:
                running = False

    pygame.display.flip()
pygame.quit()