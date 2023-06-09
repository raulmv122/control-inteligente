from tkinter import *
import os
import cv2
import numpy as np
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN

def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()

    archivo = open(usuario_info, "w")
    archivo.write(usuario_info + "\n")
    archivo.write(contra_info)
    archivo.close()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    Label(pantallaRegistro, text="Registro Convencional Exitoso", fg="green", font=("Calibri", 11)).pack()

def registro_facial():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Registro Facial', frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_img = usuario.get()
    carpeta_imagenes = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes")
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)
    ruta_imagen = os.path.join(carpeta_imagenes, usuario_img + ".jpg")
    cv2.imwrite(ruta_imagen, frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    Label(pantallaRegistro, text="Registro Facial Exitoso", fg="green", font=("Calibri", 11)).pack()

    def reg_cara(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(carpeta_imagenes, usuario_img + ".jpg"), cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = os.path.join(carpeta_imagenes, usuario_img + ".jpg")
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_cara(img, caras)

def registro():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantallaRegistro
    pantallaRegistro = Toplevel(pantallaInicio)
    pantallaRegistro.title("Registro")
    pantallaRegistro.geometry("300x250")

    usuario = StringVar()
    contra = StringVar()

    Label(pantallaRegistro, text="Registro facial: debe de asignar un usuario:").pack()
    Label(pantallaRegistro, text="Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantallaRegistro, text="").pack()
    Label(pantallaRegistro, text="Usuario * ").pack()
    usuario_entrada = Entry(pantallaRegistro, textvariable=usuario)
    usuario_entrada.pack()
    Label(pantallaRegistro, text="Contraseña * ").pack()
    contra_entrada = Entry(pantallaRegistro, textvariable=contra)
    contra_entrada.pack()
    Label(pantallaRegistro, text="").pack()
    Button(pantallaRegistro, text="Registro Tradicional", width=15, height=1, command=registrar_usuario).pack()

    Label(pantallaRegistro, text="").pack()
    Button(pantallaRegistro, text="Registro Facial", width=15, height=1, command=registro_facial).pack()

def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir()
    if log_usuario in lista_archivos:
        archivo2 = open(log_usuario, "r")
        verificacion = archivo2.read().splitlines()
        if log_contra in verificacion:
            print("Inicio de sesion exitoso")
            Label(pantallaLogin, text="Inicio de Sesion Exitoso", fg="green", font=("Calibri", 11)).pack()
        else:
            print("Contraseña incorrecta, debe intentarlo de nuevo")
            Label(pantallaLogin, text="Contraseña Incorrecta", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantallaLogin, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()

def login_facial():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Login Facial', frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_login = verificacion_usuario.get()
    carpeta_imagenes = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes")
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)
    ruta_imagen_reg = os.path.join(carpeta_imagenes, usuario_login + ".jpg")
    ruta_imagen_log = os.path.join(carpeta_imagenes, usuario_login + "LOG.jpg")
    cv2.imwrite(ruta_imagen_reg, frame)
    cv2.imwrite(ruta_imagen_log, frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    def log_cara(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(carpeta_imagenes, usuario_login + "LOG.jpg"), cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = os.path.join(carpeta_imagenes, usuario_login + "LOG.jpg")
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_cara(img, caras)

    def orb_sim(img1, img2):
        orb = cv2.ORB_create()
        kpa, descr_a = orb.detectAndCompute(img1, None)
        kpb, descr_b = orb.detectAndCompute(img2, None)
        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = comp.match(descr_a, descr_b)
        regiones_similares = [i for i in matches if i.distance < 70]
        if len(matches) == 0:
            return 0
        return len(regiones_similares) / len(matches)

    im_archivos = os.listdir(carpeta_imagenes)
    if usuario_login + ".jpg" in im_archivos:
        rostro_reg = cv2.imread(os.path.join(carpeta_imagenes, usuario_login + ".jpg"), 0)
        rostro_log = cv2.imread(os.path.join(carpeta_imagenes, usuario_login + "LOG.jpg"), 0)
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.85:
            Label(pantallaLogin, text="Inicio de Sesion Exitoso", fg="green", font=("Calibri", 11)).pack()
            print("Bienvenido al sistema usuario:", usuario_login)
            print("Compatibilidad con la foto del registro:", similitud)
        else:
            print("Rostro incorrecto, Verifique su usuario")
            print("Igualdad con la foto del registro:", similitud)
            Label(pantallaLogin, text="No se encuentra el parecido de rostros", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantallaLogin, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()

def login():
    global pantallaLogin
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2

    pantallaLogin = Toplevel(pantallaInicio)
    pantallaLogin.title("Login")
    pantallaLogin.geometry("300x250")
    Label(pantallaLogin, text="Login facial: debe de asignar un usuario:").pack()
    Label(pantallaLogin, text="Login user - contraseña: debe asignar usuario y contraseña:").pack()
    Label(pantallaLogin, text="").pack()

    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()

    Label(pantallaLogin, text="Usuario * ").pack()
    usuario_entrada2 = Entry(pantallaLogin, textvariable=verificacion_usuario)
    usuario_entrada2.pack()
    Label(pantallaLogin, text="Contraseña * ").pack()
    contra_entrada2 = Entry(pantallaLogin, textvariable=verificacion_contra)
    contra_entrada2.pack()
    Label(pantallaLogin, text="").pack()
    Button(pantallaLogin, text="Inicio de Sesion User - Contraseña", width=20, height=1, command=verificacion_login).pack()

    Label(pantallaLogin, text="").pack()
    Button(pantallaLogin, text="Inicio de Sesion Facial", width=20, height=1, command=login_facial).pack()

def pantalla_principal():
    global pantallaInicio
    pantallaInicio = Tk()
    pantallaInicio.geometry("300x250")
    pantallaInicio.title("Inicio")
    Label(text="Login Inteligente", bg="gray", width="400", height="3", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Iniciar Sesión", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Registro", height="2", width="30", command=registro).pack()
    pantallaInicio.mainloop()

pantalla_principal()
