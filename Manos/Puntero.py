import cv2
import numpy as np
import Mano #Clase con los movimientos de las manos
import pyautogui,autopy #Clase para controlar el raton
import os

#Camara
camarax = 640
camaray = 480
rectangulo = 100
ancho, alto= autopy.screen.size()#Dimensiones de la pantalla
filtro = 5
camx = 0
camy = 0
recx, recy = 0,0

camara = cv2.VideoCapture(0)
camara.set(3,640)
camara.set(4,640)

scanner = Mano.manos(nManos=1)

teclado = False

while True:
    ret, frame = camara.read()

    frame = scanner.buscarManos(frame)
    lista, rectanguloPos = scanner.posicionManos(frame)

    cv2.rectangle(frame, (rectangulo, rectangulo), (camarax - rectangulo, camaray - rectangulo), (0, 0, 255), 2)
    if len(lista) !=0:
        x1, y1 = lista[8][1:] #Dedo anular
        x2, y2 = lista[12][1:] #Dedo indice
        dedos = scanner.levantarDedo()#Dedo este levantado
        cv2.rectangle(frame, (rectangulo, rectangulo),(camarax - rectangulo, camaray - rectangulo),(0,0,255),2)#Dibujamos un rectangulo
        #para saber el area en el que trabajamos

        if dedos[1]==1 and dedos[2]==0 and dedos[3] == 0 and dedos[4] == 0:#Si el dedo indice esta arriba y el corazon abajo
            x3 = np.interp(x1,(rectangulo, camarax - rectangulo), (0, ancho))#interp se encarga de convertir los pixeles
            # de la pantalla a los de la camara
            y3 = np.interp(y1,(rectangulo,camaray - rectangulo),(0, alto))
            recx = camx + (x3 - camx)/filtro #Ubicacion - anterior + x3
            recy = camy + (y3 - camy)/filtro #Ubicacion - anterior + y3

            #Movimiento
            autopy.mouse.move(ancho-recx,recy)#Enviamos las cordenadas
            cv2.circle(frame,(x1,y1),10,(0,0,0),cv2.FILLED)
            camx, camy = recx, recy

        if dedos[1]==1 and dedos[2]==1 and dedos[3] == 0 and dedos[4] == 0: #Dos dedos estan levantados
            longitud, frame, linea = scanner.separacionDedos(8,12,frame)#Comprobamos cuanto espacio hay entre los dedos
            print(longitud)
            if longitud <10:#Se estan tocando
                cv2.circle(frame,(linea[4],linea[5]),10,(255,0,0),cv2.FILLED)
                autopy.mouse.click()#Click

        if dedos[1] == 1 and dedos[2] == 1 and dedos[3] == 1 and dedos[4] == 0:
            pyautogui.scroll(300)

        if dedos[1] == 1 and dedos[2] == 1 and dedos[3] == 1 and dedos[4] == 1  and dedos[0] == 0:
            pyautogui.scroll(-300)

        if dedos[1] == 1 and dedos[2] == 1 and dedos[3] == 1 and dedos[4] == 1 and dedos[0] == 1:
            print("teclado")
    cv2.imshow("Puntero",frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
camara.release()
cv2.destroyAllWindows()