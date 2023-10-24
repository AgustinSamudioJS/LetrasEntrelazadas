import pygame
from pygame.locals import *
from configuracion import *
pygame.init()
pygame.font.init() #Inicializar las fuentes
def dameLetraApretada(key):
    if key == K_a:
        return("a")
    elif key == K_b:
        return("b")
    elif key == K_c:
        return("c")
    elif key == K_d:
        return("d")
    elif key == K_e:
        return("e")
    elif key == K_f:
        return("f")
    elif key == K_g:
        return("g")
    elif key == K_h:
        return("h")
    elif key == K_i:
        return("i")
    elif key == K_j:
        return("j")
    elif key == K_k:
        return("k")
    elif key == K_l:
        return("l")
    elif key == K_m:
        return("m")
    elif key == K_n:
        return("n")
    elif key == 241:
        return("ñ")
    elif key == K_o:
        return("o")
    elif key == K_p:
        return("p")
    elif key == K_q:
        return("q")
    elif key == K_r:
        return("r")
    elif key == K_s:
        return("s")
    elif key == K_t:
        return("t")
    elif key == K_u:
        return("u")
    elif key == K_v:
        return("v")
    elif key == K_w:
        return("w")
    elif key == K_x:
        return("x")
    elif key == K_y:
        return("y")
    elif key == K_z:
        return("z")
    elif key == K_SPACE:
       return(" ")
    else:
        return("")

def dibujar(screen, letraPrincipal, letrasEnPantalla, candidata, puntos, segundos):
    fondo = pygame.image.load("juego.png").convert()
    screen.blit(fondo, (0, 0))
    #FUENTES
    showcard=pygame.font.SysFont("Showcard Gothic",60)
    fuente2=pygame.font.SysFont("Copperplate Gothic",20)
    Fcandidata=pygame.font.SysFont("Copperplate Gothic",40)
    #Linea del piso
    pygame.draw.line(screen, (255,36,71), (0, ALTO-70) , (ANCHO, ALTO-70), 5)

    ren1 = fuente2.render(candidata, 1, blanco)
    ren2 = fuente2.render("Puntos: " + str(puntos), 1, blanco)
    
    if(segundos<10):
        ren3 = fuente2.render("Tiempo: " + str(int(segundos)), 1, COLOR_TIEMPO_FINAL)
    else:
        ren3 = fuente2.render("Tiempo: " + str(int(segundos)), 1, blanco)
    #escribe grande la palabra (letra por letra) y la letra principal de otro color
    pos = 130
    for i in range(len(letrasEnPantalla)):
        if letrasEnPantalla[i] == letraPrincipal:
            screen.blit(showcard.render(letrasEnPantalla[i], 1, COLOR_TIEMPO_FINAL), (pos, 100))
        else:
            screen.blit(showcard.render(letrasEnPantalla[i], 1, COLOR_LETRAS), (pos, 100))
        pos = pos + TAMANNO_LETRA_GRANDE

    screen.blit(ren1, (300, 500))
    screen.blit(ren2, (680, 10))
    screen.blit(ren3, (10, 10))