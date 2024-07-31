import socket
import threading

PORT = 12345        

def recibir_mensajes(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"\nMensaje recibido de {addr}: {data.decode()}")

def enviar_mensajes(sock, destinos):
    while True:
        mensaje = input()
        for dest_ip, dest_port in destinos:
            sock.sendto(mensaje.encode(), (dest_ip, dest_port))

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
    hilo_enviar = threading.Thread(target=enviar_mensajes, args=(sock, destinos))

    hilo_recibir.start()
    hilo_enviar.start()

    hilo_recibir.join()
    hilo_enviar.join()