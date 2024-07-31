import threading
import time
from plyer import notification
import os
import platform
<<<<<<< HEAD
import socket
from mensajes import obtener_ip_local, PORT, enviar_mensajes, recibir_mensajes
=======

PORT = 12345

def recibir_mensajes(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            mensaje = f"\n{addr[0]}: {data.decode()}"
            print(mensaje)  # Mostrar el mensaje en la consola
            # Mostrar notificación
            notification.notify(
                title="Nuevo mensaje",
                message=f"Mensaje de {addr[0]}: {data.decode()}",
                app_name="Chat Grupal",
                timeout=5
            )
            # Simular ocultar la ventana
            if platform.system() == "Windows":
                os.system("powershell -command \"& { $wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('% {TAB}'); }\"")
            time.sleep(1)  # Pausa para evitar sobrecargar el sistema
        except Exception as e:
            print(f"Error recibiendo mensaje: {e}")
            break

def enviar_mensajes(sock, destinos, mensaje):
    for dest_ip, dest_port in destinos:
        try:
            sock.sendto(mensaje.encode(), (dest_ip, dest_port))
        except Exception as e:
            print(f"Error enviando mensaje a {dest_ip}: {e}")

def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', 80))  # Usar una IP pública para determinar la IP local
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
>>>>>>> f5d52aeca9546b9d6c16caecf3a48486bf3fe353

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', PORT))  

    ip_local = obtener_ip_local()
    print(f"Tu IP y puerto: {ip_local}:{PORT}")

    destinos = []
    while True:
        dest_ip = input("Introduce la dirección IP del compañero (o 'fin' para terminar): ")
        if not dest_ip or dest_ip.lower() == 'fin':
            break
        destinos.append((dest_ip, PORT))

    if not destinos:
        print("No se ingresaron destinos. El programa terminará.")
        return

    # Iniciar hilo para recibir mensajes
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(sock,))
    hilo_recibir.daemon = True
    hilo_recibir.start()

    while True:
        mensaje = input()
        if mensaje.lower() == 'exit':
            break
        if mensaje:
            enviar_mensajes(sock, destinos, mensaje)

if __name__ == "__main__":
    main()
