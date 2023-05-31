import cv2
import math
import mediapipe as mp
import time

class manos():
    #Constructor por "defecto"
    def __init__(self, mode=False, nManos=2, deteccion = 0.5,seguimiento = 0.5):
        #Variables y parametros
        self.mode = mode
        self.nManos = nManos
        self.deteccion = deteccion
        self.seguimiento = seguimiento

        #Creamos los objetos necesarios
        self.mpmanos = mp.solutions.hands #Objeto encargado de detectar las manos
        self.manos = self.mpmanos.Hands(self.mode, self.nManos, self.deteccion, self.seguimiento) #Le introducimos los parametros para la detecciÃ³n
        self.mapa = mp.solutions.drawing_utils #Nos mapeara o dibujara el objeto
        self.tip = [4,8,12,16,20] #Vector que separa la mano por nodos y permite identificar los dedos y sus posiciones

    #Esta funcion es la encargada de buscar nuestras manos a cada momento
    def buscarManos(self, frame, dibujar = True):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultado = self.manos.process(frame_rgb)

        #Comprobamos si hemos encontrado las manos
        if self.resultado.multi_hand_landmarks:
            #print("mano encontrada")
            #Si hay algo usamos un for para trabajar con varias manos
            for mano in self.resultado.multi_hand_landmarks:
                if dibujar:
                    self.mapa.draw_landmarks(frame,mano,self.mpmanos.HAND_CONNECTIONS) #Mapeamos la mano con las conexiones y los puntos

        return frame #Devolvemos el momento

    #Esta funcion detectara la posicion de nuestras manos
    def posicionManos(self,frame,nMano = 0, dibujar = True):
        #Creamos una lista para guardar las posiciones en x e y de los puntos de nuestra mano
        xlista = []
        ylista = []
        rectanguloPos = []
        self.lista = []
        #Comprobamos si ha detectado la posicion
        if self.resultado.multi_hand_landmarks:
            #print("pos")
            mano = self.resultado.multi_hand_landmarks[nMano]
            for id, lm in enumerate(mano.landmark):
                alto, ancho, c = frame.shape #Recogemos el tamaÃ±o del frame que usamos
                coordX, coordY = int(lm.x * ancho), int(lm.y * alto)#El frame nos da % de tamaÃ±o, lo pasamos a pixeles
                #Guardamos las coordenadas en nuestras listas
                xlista.append(coordX)
                ylista.append(coordY)
                #Guardamos los puntos de la mano y su posiciÃ³n
                self.lista.append([id,coordX ,coordY])
                if dibujar:
                    cv2.circle(frame, (coordX, coordY), 5, (0,0,0), cv2.FILLED)#Dibujamos un circuloÂ¿?
            #Conseguimos los puntos maximos y minimos de la mano, para dibujar un rectangulo alrededor de ella
            xmin = min(xlista)
            xmax = max(xlista)
            ymin = min(ylista)
            ymax = max(ylista)
            rectanguloPos = xmin, ymin, xmax, ymax
            #Dibujamos el rectangulo con los parametros obtenidos
            if dibujar:
                cv2.rectangle(frame,(xmin - 20, ymin - 20),(xmax + 20, ymax + 20),(0,255,0), 2)
        return self.lista, rectanguloPos
    #Esta funciÃ³n detectara cuando tenemos un dedo levantado y lo dibuja
    def levantarDedo(self):
        dedos = []
        #Comprobamos si el dedo esta "levantado"
        if self.lista[self.tip[0]][1] > self.lista[self.tip[0]-1][1]:
            dedos.append(1)
        else:
            dedos.append(0)

        #Creamos un vector de 5 posiciones donde 0 es el dedo bajado y 1 el dedo levantado
        for id in range(1,5):
            #Comprobamos si bajamos el dedo
            if self.lista[self.tip[id]][2] < self.lista[self.tip[id] - 2][2]:
                dedos.append(1)
            else:
                dedos.append(0)
        return dedos

    #Gracias a esta funciÃ³n podemos medir cuanta distancia hay en los dedos
    def separacionDedos(self,n1, n2, frame, dibujar = True):#Pasamos 2 puntos de los dedos
        x1, y1 = self.lista[n1][1:]
        x2, y2 = self.lista[n2][1:]
        coordX, coordY = (x1 + x2) // 2, (y1 + y2) // 2
        if dibujar:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255),3)
            cv2.circle(frame,(x1, y1), 15, (0,0,225), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 15, (0, 0, 225), cv2.FILLED)
            cv2.circle(frame, (coordX, coordY), 15, (0, 0, 225), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return  length, frame, [x1, y1, x2, y2, coordX, coordY]

def main():
    #ptiempo = 0

    #Usamos la camara del ordenador
    cap = cv2.VideoCapture(0)
    #Nos creamos el objeto
    escaner = manos()

    #Escaneamos constantemente
    while True:
        ret, frame = cap.read()
        #Enviamos las imagenes/frames
        frame = escaner.buscarManos(frame)
        lista, cuadrado = escaner.posicionManos(frame)
        #Si la lista no esta vacia, imprimimos el ultimo punto, es decir la parte superior del dedo
        if len(lista) !=0:
            #print(lista[4])
            #FPS
            #ctiempo = time.time()
            #fps = 1 /(ctiempo - ptiempo)
            #ptiempo = ctiempo

            cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

            cv2.imshow("Mano", frame)
            k = cv2.waitKey(1)

            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__=="__main__":
    main()
