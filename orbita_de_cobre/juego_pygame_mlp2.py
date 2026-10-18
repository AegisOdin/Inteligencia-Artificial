"""Juego de salto con un árbol de decisión; recursos originales de Órbita de cobre."""
import csv
import os
import random
from pathlib import Path

import pygame
from sklearn.model_selection import GroupShuffleSplit
from sklearn.tree import DecisionTreeClassifier

BASE = Path(__file__).resolve().parent
ANCHO, ALTO = 1080, 720


def entrenar(muestras):
    """Filas: velocidad, distancia, acción de salto, número de ronda."""
    if len(muestras) < 80:
        raise ValueError("Reúne al menos 80 decisiones manuales.")
    if len({m[2] for m in muestras}) < 2:
        raise ValueError("Faltan ejemplos de salto o de espera.")
    grupos = [m[3] for m in muestras]
    if len(set(grupos)) < 3:
        raise ValueError("Juega al menos tres rondas para separar prueba y entrenamiento.")
    x = [[m[0],m[1]] for m in muestras]
    y = [m[2] for m in muestras]
    separador = GroupShuffleSplit(n_splits=1, test_size=.25, random_state=42)
    indices, prueba = next(separador.split(x,y,grupos))
    if len({y[i] for i in indices}) < 2:
        raise ValueError("El grupo de entrenamiento no tiene ambas acciones; juega más rondas.")
    modelo = DecisionTreeClassifier(max_depth=5, min_samples_leaf=2,
                                   class_weight="balanced", random_state=42)
    modelo.fit([x[i] for i in indices], [y[i] for i in indices])
    acierto = modelo.score([x[i] for i in prueba], [y[i] for i in prueba])
    return modelo, acierto


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO,ALTO))
        pygame.display.set_caption("Órbita de cobre | árbol de decisión")
        self.lienzo = pygame.Surface((ANCHO,ALTO))
        self.fuente = pygame.font.SysFont("Segoe UI",24)
        self.pequena = pygame.font.SysFont("Segoe UI",18)
        self.frames = [self.imagen(f"sprites/robot_carrera_{n}.png",(35,52)) for n in range(1,5)]
        self.orbe = self.imagen("sprites/orbe_energia.png",(17,17))
        self.dron = self.imagen("game/dron_enemigo.png",(70,70))
        # El fondo tiene plataforma a ~81%; se encuadra para alinearla con los pies a y=662.
        self.fondo = self.imagen("game/desierto_observatorio.png",(ANCHO,815))
        self.fondo_invertido = pygame.transform.flip(self.fondo,True,False)
        self.datos = []
        self.modelo = None
        self.auto = False
        self.menu = True
        self.activo = True
        self.completa = False
        self.mensaje = "M: comenzar una sesión manual"
        self.ronda = 0
        self.tiempo = 0
        self.desplazamiento = 0
        self.reiniciar()

    def imagen(self,ruta,tamano):
        archivo = BASE/"assets"/ruta
        try:
            return pygame.transform.smoothscale(pygame.image.load(str(archivo)).convert_alpha(),tamano)
        except (pygame.error,OSError) as exc:
            raise RuntimeError(f"No se pudo cargar el recurso {archivo}") from exc

    def reiniciar(self):
        self.jugador = pygame.Rect(55,610,35,52)
        self.bala = pygame.Rect(1025,621,17,17)
        self.y = 610.0
        self.vy = 0.0
        self.suelo = True
        self.velocidad = int(random.randint(-12,-6)*1.1)
        self.ronda += 1

    def saltar(self):
        if self.suelo:
            self.vy = -16.5
            self.suelo = False

    def avanzar(self,accion=False):
        if self.suelo:
            distancia = float(abs(self.bala.x-self.jugador.x))
            if self.auto and self.modelo is not None:
                accion = bool(self.modelo.predict([[self.velocidad,distancia]])[0])
            elif not self.auto:
                # Etiqueta la acción antes de cambiar el estado; estar en el aire no es otra orden de salto.
                self.datos.append((float(self.velocidad),distancia,int(accion),self.ronda))
            if accion:
                self.saltar()
        if not self.suelo:
            self.y += self.vy
            self.vy += 1.1
            if self.y >= 610:
                self.y,self.vy,self.suelo = 610.0,0.0,True
            self.jugador.y = round(self.y)
        self.bala.x += self.velocidad
        if self.jugador.colliderect(self.bala):
            self.reiniciar()
        elif self.bala.right < 0:
            self.bala.x = 1025
            self.velocidad = int(random.randint(-12,-6)*1.1)
            self.ronda += 1
        self.tiempo += 1
        self.desplazamiento = (self.desplazamiento+2)%(2*ANCHO)

    def exportar(self):
        ruta = BASE/"datos_salto.csv"
        try:
            with ruta.open("w",newline="",encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["velocidad","distancia","salto","ronda"])
                escritor.writerows(self.datos)
            self.mensaje = f"Guardadas {len(self.datos)} decisiones en {ruta.name}"
        except OSError as exc:
            self.mensaje = f"No se pudo guardar: {exc}"

    def graficar(self,dimension):
        if not self.datos:
            self.mensaje = "Primero registra decisiones."
            return
        try:
            import matplotlib.pyplot as plt
            fig = plt.figure()
            ax = fig.add_subplot(111,projection="3d" if dimension == 3 else None)
            x,y = [m[1] for m in self.datos],[m[0] for m in self.datos]
            color = ["#d87037" if m[2] else "#19a5a7" for m in self.datos]
            if dimension == 3:
                ax.scatter(x,y,range(len(x)),c=color,s=8)
                ax.set_zlabel("Índice de decisión")
            else:
                ax.scatter(x,y,c=color,s=8)
            ax.set(xlabel="Distancia (px)",ylabel="Velocidad (px/frame)",
                   title="Decisiones: naranja = salto, turquesa = espera")
            plt.show(block=False)
            plt.pause(.01)
        except (ImportError,RuntimeError) as exc:
            self.mensaje = f"No se pudo abrir la gráfica: {exc}"

    def tecla(self,tecla):
        if tecla == pygame.K_q:
            self.activo = False
        elif tecla == pygame.K_f:
            self.completa = not self.completa
            self.pantalla = pygame.display.set_mode((0,0),pygame.FULLSCREEN) if self.completa else pygame.display.set_mode((ANCHO,ALTO))
        elif tecla in (pygame.K_ESCAPE,pygame.K_p):
            self.menu = True
        elif self.menu:
            if tecla == pygame.K_m:
                self.datos.clear()
                self.modelo = None
                self.auto,self.menu = False,False
                self.reiniciar()
            elif tecla == pygame.K_a:
                if self.modelo is None:
                    self.mensaje = "Entrena primero con T."
                else:
                    self.auto,self.menu = True,False
                    self.reiniciar()
            elif tecla == pygame.K_t:
                try:
                    self.modelo,acierto = entrenar(self.datos)
                    self.mensaje = f"Acierto en rondas reservadas: {acierto:.1%}. No garantiza supervivencia."
                except ValueError as exc:
                    self.mensaje = str(exc)
            elif tecla == pygame.K_c:
                self.exportar()
            elif tecla in (pygame.K_2,pygame.K_3):
                self.graficar(2 if tecla == pygame.K_2 else 3)

    def dibujar(self):
        if self.menu:
            self.lienzo.fill((16,23,43))
            lineas = [
                "ÓRBITA DE COBRE", "Aprender cuándo saltar",
                "", "M · Manual nuevo (borra datos y modelo)", "A · Piloto automático",
                "T · Entrenar árbol", "C · Exportar CSV", "2 / 3 · Gráficas",
                "F · Pantalla completa", "Q · Salir", "",
                f"Decisiones: {len(self.datos)}  |  Rondas: {self.ronda}",
                self.mensaje,
            ]
            for n,linea in enumerate(lineas):
                fuente = self.pequena if n >= 11 else self.fuente
                color = (238,163,92) if n in (0,12) else (212,231,237)
                self.lienzo.blit(fuente.render(linea,True,color),(60,50+n*42))
        else:
            tramo, avance = divmod(self.desplazamiento,ANCHO)
            for i in (0,1):
                fondo = self.fondo if (tramo+i)%2 == 0 else self.fondo_invertido
                self.lienzo.blit(fondo,(i*ANCHO-avance,0))
            self.lienzo.blit(self.frames[(self.tiempo//10)%4],self.jugador)
            self.lienzo.blit(self.dron,(970,592))
            self.lienzo.blit(self.orbe,self.bala)
            pygame.draw.rect(self.lienzo,(16,23,43),(0,0,ANCHO,40))
            texto = f"{'AUTO' if self.auto else 'MANUAL'} · Espacio: saltar · P: menú · Ronda {self.ronda}"
            self.lienzo.blit(self.pequena.render(texto,True,(230,240,245)),(18,10))
        pygame.transform.smoothscale(self.lienzo,self.pantalla.get_size(),self.pantalla)
        pygame.display.flip()

    def ejecutar(self):
        reloj = pygame.time.Clock()
        try:
            while self.activo:
                salto = False
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.activo = False
                    elif evento.type == pygame.KEYDOWN:
                        salto |= evento.key == pygame.K_SPACE and not self.menu and not self.auto
                        self.tecla(evento.key)
                if not self.menu and self.activo:
                    self.avanzar(salto)
                self.dibujar()
                reloj.tick(45)
        finally:
            pygame.quit()

if __name__ == "__main__":
    Juego().ejecutar()
