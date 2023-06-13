import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import cv2
import numpy as np
import mysql.connector
import os

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login con Inteligencia Artificial")

        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        ancho_ventana = int(ancho_pantalla / 2)
        alto_ventana = int(alto_pantalla / 2)
        x_ventana = int((ancho_pantalla - ancho_ventana) / 2)
        y_ventana = int((alto_pantalla - alto_ventana) / 2)

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

        estilo_botones = ttk.Style()
        estilo_botones.configure("TButton", font=tkfont.Font(family="Helvetica", size=14), background="#f6c19c", foreground="#000000")
        estilo_botones.map("TButton", background=[("active", "#AAAAAA")], foreground=[("active", "#FFFFFF")])

        btn_iniciar_sesion = ttk.Button(self, text="Iniciar sesión", command=self.abrir_ventana_iniciar_sesion, width=20)
        btn_iniciar_sesion.pack(pady=50)
        btn_iniciar_sesion.place(relx=0.5, rely=0.5, anchor="center")

        btn_registrarse = ttk.Button(self, text="Registrarse", command=self.abrir_ventana_registro, width=20)
        btn_registrarse.pack(pady=20)
        btn_registrarse.place(relx=0.5, rely=0.6, anchor="center")

    def abrir_ventana_iniciar_sesion(self):
        ventana_iniciar_sesion = VentanaIniciarSesion(self)
        ventana_iniciar_sesion.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_x()}+{self.winfo_y()}")
        ventana_iniciar_sesion.mainloop()

    def abrir_ventana_registro(self):
        ventana_registro = VentanaRegistro(self)
        ventana_registro.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_x()}+{self.winfo_y()}")
        ventana_registro.mainloop()


class VentanaRegistro(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro")

        ancho_ventana = parent.winfo_width()
        alto_ventana = parent.winfo_height()
        x_ventana = parent.winfo_x()
        y_ventana = parent.winfo_y()

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

        estilo = ttk.Style()
        estilo.configure("TLabel", font=tkfont.Font(family="Helvetica", size=12), background="#f6c19c",
                         foreground="#000000")

        lbl_usuario = ttk.Label(self, text="Nombre de usuario:")
        lbl_usuario.pack()

        self.entry_usuario = ttk.Entry(self)
        self.entry_usuario.pack()

        btn_agregar_imagen = ttk.Button(self, text="Agregar imagen", command=self.capturar_imagen, width=20)
        btn_agregar_imagen.pack(pady=10)

    def capturar_imagen(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            cv2.imshow("Capturando imagen", frame)

            if cv2.waitKey(1) == 27:
                nombre_empleado = self.entry_usuario.get()
                nombre_imagen = f"imagenes-login/{nombre_empleado}+INICIO.jpg"
                cv2.imwrite(nombre_imagen, frame)
                break

        cv2.destroyAllWindows()
        cap.release()

        self.registrar_usuario()

    def registrar_usuario(self):
        nombre_usuario = self.entry_usuario.get()
        nombre_imagen = f"imagenes-login/{nombre_usuario}+INICIO.jpg"
        imagen_capturada = cv2.imread(nombre_imagen)

        if imagen_capturada is not None:
            caras = detectar_caras(imagen_capturada)

            if len(caras) > 0:
                cara_recortada = recortar_cara(caras[0], imagen_capturada)
                cara_redimensionada = cv2.resize(cara_recortada, (200, 200))

                nombre_imagen_recortada = f"imagenes/{nombre_usuario}.jpg"
                cv2.imwrite(nombre_imagen_recortada, cara_redimensionada)

                conexion = mysql.connector.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    password="sasa",
                    database="control_citas"
                )

                cursor = conexion.cursor()

                try:
                    consulta = "INSERT INTO `empleado` (`nombre`, `apellido`, `email`, `rol`, `loggeado`) VALUES (%s, '', '', '', FALSE)"
                    valores = (nombre_usuario,)
                    cursor.execute(consulta, valores)

                    conexion.commit()

                    print("Usuario registrado correctamente")

                except mysql.connector.Error as error:
                    print(f"Error al registrar el usuario: {error}")

                finally:
                    cursor.close()
                    conexion.close()
            else:
                print("Error: No se ha detectado ninguna cara en la imagen")
        else:
            print("Error: No se pudo leer la imagen capturada")

        os.remove(nombre_imagen)

        self.destroy()


class VentanaIniciarSesion(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Iniciar sesión")

        ancho_ventana = parent.winfo_width()
        alto_ventana = parent.winfo_height()
        x_ventana = parent.winfo_x()
        y_ventana = parent.winfo_y()

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

        estilo = ttk.Style()
        estilo.configure("TLabel", font=tkfont.Font(family="Helvetica", size=12), background="#f6c19c", foreground="#000000")

        lbl_usuario = ttk.Label(self, text="Nombre de usuario:")
        lbl_usuario.pack()

        self.entry_usuario = ttk.Entry(self)
        self.entry_usuario.pack()

        btn_iniciar_sesion = ttk.Button(self, text="Iniciar sesión", command=self.iniciar_sesion, width=20)
        btn_iniciar_sesion.pack(pady=10)

    def iniciar_sesion(self):
        nombre_usuario = self.entry_usuario.get()

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            nombre_imagen = f"imagenes-login/{nombre_usuario}_INICIO.jpg"
            cv2.imwrite(nombre_imagen, frame)

            imagen_capturada = cv2.imread(nombre_imagen)

            if imagen_capturada is not None:
                caras = detectar_caras(imagen_capturada)

                if len(caras) > 0:
                    cara_recortada = recortar_cara(caras[0], imagen_capturada)
                    cara_redimensionada = cv2.resize(cara_recortada, (200, 200))

                    nombre_imagen_recortada = f"imagenes-login/{nombre_usuario}_INICIO.jpg"
                    cv2.imwrite(nombre_imagen_recortada, cara_redimensionada)

                    conexion = mysql.connector.connect(
                        host="localhost",
                        port=3306,
                        user="root",
                        password="sasa",
                        database="control_citas"
                    )

                    cursor = conexion.cursor()

                    try:
                        consulta = "SELECT * FROM `empleado` WHERE `nombre` = %s"
                        valores = (nombre_usuario,)
                        cursor.execute(consulta, valores)

                        resultado = cursor.fetchone()

                        if resultado is not None:
                            ruta_imagen_empleado = f"imagenes/{nombre_usuario}.jpg"

                            if os.path.isfile(ruta_imagen_empleado):
                                imagen_empleado = cv2.imread(ruta_imagen_empleado)

                                if imagen_empleado is not None:
                                    caras_empleado = detectar_caras(imagen_empleado)

                                    if len(caras_empleado) > 0:
                                        cara_recortada_empleado = recortar_cara(caras_empleado[0], imagen_empleado)
                                        cara_redimensionada_empleado = cv2.resize(cara_recortada_empleado, (200, 200))

                                        porcentaje_similitud = calcular_similitud_caras(cara_redimensionada,
                                                                                        cara_redimensionada_empleado)

                                        if porcentaje_similitud >= 40:
                                            print("Inicio de sesión exitoso")

                                            consulta_actualizar = "UPDATE `empleado` SET `loggeado` = TRUE WHERE `nombre` = %s"
                                            valores_actualizar = (nombre_usuario,)
                                            cursor.execute(consulta_actualizar, valores_actualizar)
                                            conexion.commit()

                                        else:
                                            print("Error: No se ha reconocido correctamente al usuario")
                                    else:
                                        print("Error: No se ha detectado ninguna cara en la imagen del empleado")
                                else:
                                    print("Error: No se pudo leer la imagen del empleado")
                            else:
                                print("Error: No se encontró la imagen del empleado")
                        else:
                            print("Error: Usuario no encontrado")

                    except mysql.connector.Error as error:
                        print(f"Error al iniciar sesión: {error}")

                    finally:
                        cursor.close()
                        conexion.close()

                else:
                    print("Error: No se ha detectado ninguna cara en la imagen capturada")
            else:
                print("Error: No se pudo leer la imagen capturada")

            os.remove(nombre_imagen)

        else:
            print("Error al capturar la imagen")

        self.destroy()


def detectar_caras(imagen):
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    clasificador = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    caras = clasificador.detectMultiScale(imagen_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return caras


def recortar_cara(cara, imagen):
    x, y, w, h = cara
    cara_recortada = imagen[y:y+h, x:x+w]

    return cara_recortada


def calcular_similitud_caras(cara1, cara2):
    cara1_gris = cv2.cvtColor(cara1, cv2.COLOR_BGR2GRAY)
    cara2_gris = cv2.cvtColor(cara2, cv2.COLOR_BGR2GRAY)

    detector_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    reconocimiento_facial = cv2.face.LBPHFaceRecognizer_create()

    rostros1 = detector_rostros.detectMultiScale(cara1_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    rostros2 = detector_rostros.detectMultiScale(cara2_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(rostros1) == 0 or len(rostros2) == 0:
        print("No se detectaron rostros en una o ambas imágenes.")
        return 0

    (x1, y1, w1, h1) = rostros1[0]
    (x2, y2, w2, h2) = rostros2[0]

    cara1_roi = cara1_gris[y1:y1 + h1, x1:x1 + w1]
    cara2_roi = cara2_gris[y2:y2 + h2, x2:x2 + w2]

    reconocimiento_facial.train([cara1_roi], np.array([1]))

    etiqueta, confianza = reconocimiento_facial.predict(cara2_roi)

    porcentaje_similitud = 100 - confianza

    print(f"Porcentaje de similitud: {porcentaje_similitud}")
    return porcentaje_similitud


if __name__ == "__main__":
    ventana_principal = VentanaPrincipal()
    ventana_principal.mainloop()
