#! /usr/bin/env python
from fileinput import close
import os
import sys
import pygame
from pygame.locals import *
from configuracion import *
from funcionesRESUELTO import *
from extras import *
# Funcion principal
def main():

    # Centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.mixer.init()

    # Preparar la ventana
    pygame.display.set_caption("Armar palabras con...")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    # Fondos del juego
    fondo_inicio = pygame.image.load("fondo2.png").convert()
    fondo_reglas = pygame.image.load("Reglas.png").convert()
    fondo_ranking = pygame.image.load("fondo1.png").convert()

    # Colores
    BLANCO = (255, 255, 255)
    AZUL = (0, 0, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)

    # Fuente
    fuente = pygame.font.SysFont("Showcard Gothic", 30)

    # Opciones del menú
    opciones_menu = ["INICIO", "REGLAS", "RANKING"]
    opcion_seleccionada = 0

    # Varible que guarda el nombre del usuario
    nombre_usuario = ""

    # Esta función dibuja el menú
    def dibujar_menu():
        screen.blit(fondo_inicio, (0, 0))

        for indice, opcion in enumerate(opciones_menu):
            texto = fuente.render(
                opcion, True, ROJO if indice == opcion_seleccionada else blanco)
            rectangulo_texto = texto.get_rect(
                center=(ANCHO // 2, ALTO // 2 + indice * 50))
            screen.blit(texto, rectangulo_texto)

        pygame.display.flip()

    # Esta funcion dibuja la pantalla de reglas del juego
    def mostrar_reglas():

        screen.blit(fondo_reglas, (0, 0))

        pygame.display.flip()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    # Al tocar ENTER vuelve la menu principal
                    if evento.key == pygame.K_RETURN:
                        return

    # Pantalla para escribir el nombre de usuario
    def ingresar_nombre():
        nonlocal nombre_usuario
        nombre_ingresado = ""

        texto_ingresar = fuente.render(
            "Ingresa tu nombre (máximo 10 letras):", True, AZUL)
        rectangulo_texto = texto_ingresar.get_rect(
            center=(ANCHO // 2, ALTO // 2 - 50))
        screen.blit(texto_ingresar, rectangulo_texto)
        pygame.display.flip()

        while True:
            for evento in pygame.event.get():
                contador_dos = pygame.time.get_ticks()/1000
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if len(nombre_ingresado) > 0 and len(nombre_ingresado) <= 10:
                            nombre_usuario = nombre_ingresado
                            return  # Regresar al menú principal
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre_ingresado = nombre_ingresado[:-1]
                    else:
                        if len(nombre_ingresado) < 10:
                            nombre_ingresado += evento.unicode

            screen.fill(BLANCO)
            texto_ingresar = fuente.render(
                "Ingresa tu nombre (máximo 10 letras):", True, AZUL)
            rectangulo_texto = texto_ingresar.get_rect(
                center=(ANCHO // 2, ALTO // 2 - 50))
            screen.blit(texto_ingresar, rectangulo_texto)

            texto_nombre = fuente.render(nombre_ingresado, True, AZUL)
            rectangulo_texto = texto_nombre.get_rect(
                center=(ANCHO // 2, ALTO // 2 + 50))
            screen.blit(texto_nombre, rectangulo_texto)

            pygame.display.flip()

    def mostrar_ranking():
        # Obtener los mejores jugadores
        mejores_jugadores = obtener_mejores_jugadores()

        screen.blit(fondo_ranking, (0, 0))

        # Título del ranking
        texto_ranking = fuente.render("RANKING", True, AZUL)
        rectangulo_texto = texto_ranking.get_rect(
            center=(ANCHO // 2, ALTO // 2 - 150))
        screen.blit(texto_ranking, rectangulo_texto)

        # Mostrar los nombres de usuario y puntajes de los mejores jugadores
        y = ALTO // 2 - 50
        for i, jugador in enumerate(mejores_jugadores):
            nombre, puntaje = jugador
            texto_jugador = fuente.render(f"{nombre}: {puntaje}", True, NEGRO)
            rectangulo_texto = texto_jugador.get_rect(
                center=(ANCHO // 2, y + i * 50))
            screen.blit(texto_jugador, rectangulo_texto)

        pygame.display.flip()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        return  # Regresar al menú principal

    def obtener_mejores_jugadores():
        mejores_jugadores = []

        with open("ranking.txt", "r") as archivo:
            lineas = archivo.readlines()

            # Obtener los nombres de usuario y puntajes de cada línea
            for linea in lineas:
                nombre, puntaje = linea.strip().split(",")
                puntaje = int(puntaje)
                mejores_jugadores.append((nombre, puntaje))

        # Ordenar los jugadores por puntaje en orden descendente
        mejores_jugadores.sort(key=lambda jugador: jugador[1], reverse=True)

        # Tomar los primeros 5 jugadores (o menos si hay menos de 5)
        mejores_jugadores = mejores_jugadores[:5]

        return mejores_jugadores

    # Esta función controla las opciones del menu
    def manejar_evento_teclado(evento):
        nonlocal opcion_seleccionada

        if evento.key == pygame.K_UP:
            opcion_seleccionada = (
                opcion_seleccionada - 1) % len(opciones_menu)
        elif evento.key == pygame.K_DOWN:
            opcion_seleccionada = (
                opcion_seleccionada + 1) % len(opciones_menu)
        elif evento.key == pygame.K_RETURN:
            if opcion_seleccionada == 0:

                # INICIO = comienza el juego

                # tiempo total del juego
                gameClock = pygame.time.Clock()
                totaltime = 0
                segundos = TIEMPO_MAX
                fps = FPS_inicial
                puntos = 0
                candidata = ""
                diccionario = []
                palabrasAcertadas = []

                # lee el diccionario
                lectura(diccionario)

                # elige las 7 letras al azar y una de ellas como principal
                letrasEnPantalla = dame7Letras()
                letraPrincipal = dameLetra(letrasEnPantalla)

                # se queda con 7 letras que permitan armar muchas palabras, evita que el juego sea aburrido
                while (len(dameAlgunasCorrectas(letraPrincipal, letrasEnPantalla, diccionario)) < MINIMO):
                    letrasEnPantalla = dame7Letras()
                    letraPrincipal = dameLetra(letrasEnPantalla)

                pygame.init()

                # Dibuja la pantalla la primera vez
                dibujar(screen, letraPrincipal, letrasEnPantalla,
                        candidata, puntos, segundos)

                # Inicia la musica
                pygame.mixer.music.load("musica.mp3")
                pygame.mixer.music.play()
                # Activar sonido
                pygame.mixer.music.set_volume(1.0)

                while segundos > fps/1000:

                    # 1 frame cada 1/fps segundos
                    gameClock.tick(fps)
                    totaltime += gameClock.get_time()

                    if True:
                        fps = 3

                    # Buscar la tecla apretada del modulo de eventos de pygame
                    for e in pygame.event.get():

                        # QUIT es apretar la X en la ventana
                        if e.type == QUIT:
                            pygame.quit()
                            return ()

                        # Ver si fue apretada alguna tecla
                        if e.type == KEYDOWN:
                            letra = dameLetraApretada(e.key)
                            candidata += letra   # Va concatenando las letras que escribe
                            if e.key == K_BACKSPACE:
                                # Borra la ultima
                                candidata = candidata[0:len(candidata)-1]
                            if e.key == K_RETURN:  # Presionó enter
                                if candidata not in palabrasAcertadas:
                                    palabrasAcertadas.append(candidata)
                                    puntos += procesar(letraPrincipal,
                                                       letrasEnPantalla, candidata, diccionario)
                                candidata = ""

                    segundos = (
                        TIEMPO_MAX - pygame.time.get_ticks()/1000) + contador

                    # Limpiar pantalla anterior
                    screen.fill(COLOR_FONDO)

                    # Dibujar de nuevo todo
                    dibujar(screen, letraPrincipal, letrasEnPantalla,
                            candidata, puntos, segundos)

                    pygame.display.flip()

                if segundos <= 0:
                    # Termina la musica
                    # Desactivar sonido
                    pygame.mixer.music.set_volume(0.0)

                    ingresar_nombre()
                    guardar_puntaje(nombre_usuario, puntos)
                    mostrar_ranking()

            elif opcion_seleccionada == 1:
                # REGLAS = Muestra las reglas del juego
                mostrar_reglas()
            elif opcion_seleccionada == 2:
                # RANKING = Muestra el ranking
                mostrar_ranking()

    def guardar_puntaje(nombre, puntaje):
        with open("ranking.txt", "a") as archivo:
            archivo.write(f"{nombre},{puntaje}\n")

    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            pygame.mixer.music.set_volume(0.0)
            contador = pygame.time.get_ticks()/1000
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif evento.type == pygame.KEYDOWN:
                manejar_evento_teclado(evento)

        dibujar_menu()
# Programa Principal ejecuta Main
if __name__ == "__main__":
    main()
