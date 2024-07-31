import threading
import socket
from mensajes import obtener_ip_local, PORT, enviar_mensajes, recibir_mensajes
from config import cargar_config

config = cargar_config()

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
            enviar_mensajes(config["name"], mensaje, sock, destinos)

if __name__ == "__main__":
    main()
