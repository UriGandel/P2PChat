import threading
import socket
from mensajes import obtener_ip_local, PORT, enviar_mensajes, recibir_mensajes
from config import cargar_config

config = cargar_config()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', PORT))  

    ip_local = obtener_ip_local()

    print(f"Tu IP y puerto: {ip_local}")

    destinos = []
    while True:
        dest_ip = input("Introduce la dirección IP del compañero (o 'fin' para terminar): ")
        if dest_ip.lower() == 'fin':
            break
        destinos.append((dest_ip, PORT))

    if not destinos:
        print("No se ingresaron destinos. El programa terminará.")
    else:
        hilo_recibir = threading.Thread(target=recibir_mensajes, args=(sock,))
        hilo_enviar = threading.Thread(target=enviar_mensajes, args=(config["name"], sock, destinos))

        hilo_recibir.start()
        hilo_enviar.start()

        hilo_recibir.join()
        hilo_enviar.join()

if __name__ == "__main__":
    main()