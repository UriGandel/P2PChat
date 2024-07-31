import socket

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