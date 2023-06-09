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
        estilo_botones.configure("TButton", font=tkfont.Font(family="Helvetica", size=14), background="#CCCCCC", foreground="#000000")
        estilo_botones.map("TButton",
                           background=[("active", "#AAAAAA")],
                           foreground=[("active", "#FFFFFF")])

        btn_iniciar_sesion = ttk.Button(self, text="Iniciar sesión", command=self.iniciar_sesion, width=20)
        btn_iniciar_sesion.pack(pady=50)
        btn_iniciar_sesion.place(relx=0.5, rely=0.5, anchor="center")

        btn_registrarse = ttk.Button(self, text="Registrarse", command=self.abrir_ventana_registro, width=20)
        btn_registrarse.pack(pady=20)
        btn_registrarse.place(relx=0.5, rely=0.6, anchor="center")

    def iniciar_sesion(self):
        # Aquí puedes agregar el código para la funcionalidad del botón "Iniciar sesión"
        pass

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
        btn_agregar_imagen = ttk.Button(self, text="Agregar imagen del usuario", command=self.capturar_imagen, width=20)
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

        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sasa",
            database="agency"
        )

        # Crear un objeto cursor
        cursor = conexion.cursor()

        try:
            # Convertir la imagen a formato de bytes
            imagen_bytes = cv2.imencode('.jpg', imagen_capturada)[1].tobytes()

            # Insertar el usuario en la base de datos
            consulta = "INSERT INTO `user` (`name`, `photo`) VALUES (%s, %s)"
            valores = (nombre_usuario, imagen_bytes)
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

        # Eliminar la imagen capturada después de registrar al usuario
        os.remove("imagen_capturada.jpg")

if __name__ == "__main__":
    ventana_principal = VentanaPrincipal()
    ventana_principal.mainloop()
