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

        # Obtener el tamaño de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Calcular las dimensiones y la posición de la ventana principal
        ancho_ventana = int(ancho_pantalla / 2)
        alto_ventana = int(alto_pantalla / 2)
        x_ventana = int((ancho_pantalla - ancho_ventana) / 2)
        y_ventana = int((alto_pantalla - alto_ventana) / 2)

        # Establecer las dimensiones y la posición de la ventana principal
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

        # Crear los botones
        estilo_botones = ttk.Style()
        estilo_botones.configure("TButton", font=tkfont.Font(family="Helvetica", size=14), background="#CCCCCC",
                                 foreground="#000000")
        estilo_botones.map("TButton",
                           background=[("active", "#AAAAAA")],
                           foreground=[("active", "#FFFFFF")])

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

        # Obtener las dimensiones y posición de la ventana principal
        ancho_ventana = parent.winfo_width()
        alto_ventana = parent.winfo_height()
        x_ventana = parent.winfo_x()
        y_ventana = parent.winfo_y()

        # Establecer las dimensiones y la posición de la ventana de registro
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

        # Establecer estilo para la ventana de registro
        estilo = ttk.Style()
        estilo.configure("TLabel", font=tkfont.Font(family="Helvetica", size=12), background="#CCCCCC", foreground="#000000")

        # Etiqueta y entrada para el nombre de usuario
        lbl_usuario = ttk.Label(self, text="Nombre de usuario:")
        lbl_usuario.pack()

        self.entry_usuario = ttk.Entry(self)
        self.entry_usuario.pack()

        # Botón para agregar imagen del usuario
        btn_agregar_imagen = ttk.Button(self, text="Agregar imagen", command=self.capturar_imagen, width=20)
        btn_agregar_imagen.pack(pady=10)

    def capturar_imagen(self):
        # Crear una instancia del objeto VideoCapture
        cap = cv2.VideoCapture(0)

        while True:
            # Leer un frame desde la cámara
            ret, frame = cap.read()

            # Mostrar el frame en una ventana
            cv2.imshow("Capturando imagen", frame)

            # Esperar 1 milisegundo y verificar si se ha presionado la tecla ESC
            if cv2.waitKey(1) == 27:
                # Guardar la imagen capturada
                cv2.imwrite("imagen_capturada.jpg", frame)
                break

        # Cerrar la ventana de captura y liberar la cámara
        cv2.destroyAllWindows()
        cap.release()

        # Llamar al método para registrar el usuario en la base de datos
        self.registrar_usuario()

    def registrar_usuario(self):
        # Obtener el nombre de usuario ingresado
        nombre_usuario = self.entry_usuario.get()

        # Leer la imagen capturada
        imagen_capturada = cv2.imread("imagen_capturada.jpg")

        # Verificar si la imagen se ha leído correctamente
        if imagen_capturada is not None:
            # Detectar caras en la imagen
            caras = detectar_caras(imagen_capturada)

            if len(caras) > 0:
                # Recortar la cara más grande encontrada en la imagen
                cara_recortada = recortar_cara(caras[0], imagen_capturada)

                # Redimensionar la cara recortada a 200x200
                cara_redimensionada = cv2.resize(cara_recortada, (200, 200))

                # Guardar la imagen recortada y redimensionada en la carpeta "imagenes"
                nombre_imagen = f"imagenes/{nombre_usuario}.jpg"
                cv2.imwrite(nombre_imagen, cara_redimensionada)

                # Conectar a la base de datos
                conexion = mysql.connector.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    password="sasa",
                    database="control_citas"
                )

                # Crear un objeto cursor
                cursor = conexion.cursor()

                try:
                    # Insertar el usuario en la base de datos
                    consulta = "INSERT INTO `empleado` (`nombre`, `apellido`, `email`, `rol`, `loggeado`) VALUES (%s, '', '', '', FALSE)"
                    valores = (nombre_usuario,)
                    cursor.execute(consulta, valores)

                    # Confirmar los cambios
                    conexion.commit()

                    print("Usuario registrado correctamente")

                except mysql.connector.Error as error:
                    print(f"Error al registrar el usuario: {error}")

                finally:
                    # Cerrar el cursor y la conexión a la base de datos
                    cursor.close()
                    conexion.close()
            else:
                print("Error: No se ha detectado ninguna cara en la imagen")
        else:
            print("Error: No se pudo leer la imagen capturada")

        # Eliminar la imagen capturada
        os.remove("imagen_capturada.jpg")

        # Cerrar la ventana de registro
        self.destroy()

class VentanaIniciarSesion(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Iniciar sesión")

        # Obtener las dimensiones y posición de la ventana principal
        ancho_ventana = parent.winfo_width()
        alto_ventana = parent.winfo_height()
        x_ventana = parent.winfo_x()
        y_ventana = parent.winfo_y()

        # Establecer las dimensiones y la posición de la ventana de inicio de sesión
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

        # Establecer estilo para la ventana de inicio de sesión
        estilo = ttk.Style()
        estilo.configure("TLabel", font=tkfont.Font(family="Helvetica", size=12), background="#CCCCCC", foreground="#000000")

        # Etiqueta y entrada para el nombre de usuario
        lbl_usuario = ttk.Label(self, text="Nombre de usuario:")
        lbl_usuario.pack()

        self.entry_usuario = ttk.Entry(self)
        self.entry_usuario.pack()

        # Botón para iniciar sesión
        btn_iniciar_sesion = ttk.Button(self, text="Iniciar sesión", command=self.iniciar_sesion, width=20)
        btn_iniciar_sesion.pack(pady=10)

    def iniciar_sesion(self):
        # Obtener el nombre de usuario ingresado
        nombre_usuario = self.entry_usuario.get()

        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sasa",
            database="control_citas"
        )

        # Crear un objeto cursor
        cursor = conexion.cursor()

        try:
            # Verificar si existe un usuario con el nombre ingresado en la tabla "empleado"
            consulta = "SELECT * FROM `empleado` WHERE `nombre` = %s"
            valores = (nombre_usuario,)
            cursor.execute(consulta, valores)

            resultado = cursor.fetchone()

            if resultado is not None:
                print("Inicio de sesión exitoso")
            else:
                print("Error: Usuario no encontrado")

        except mysql.connector.Error as error:
            print(f"Error al iniciar sesión: {error}")

        finally:
            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            conexion.close()

        # Cerrar la ventana de inicio de sesión
        self.destroy()

def detectar_caras(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Crear un clasificador de caras
    clasificador = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Detectar caras en la imagen
    caras = clasificador.detectMultiScale(imagen_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return caras

def recortar_cara(cara, imagen):
    # Obtener las coordenadas de la cara
    x, y, w, h = cara

    # Recortar la cara de la imagen original
    cara_recortada = imagen[y:y + h, x:x + w]

    return cara_recortada

if __name__ == "__main__":
    ventana_principal = VentanaPrincipal()
    ventana_principal.mainloop()
