import socket
import json
from time import sleep
from plyer import notification

PORT = 12345

def recibir_mensajes(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            data = json.loads(data.decode())
            nombre = data["name"]
            mensaje = data["msg"]
            notification.notify(
                title="Nuevo mensaje",
                message=f"Mensaje de {addr[0]}: {data.decode()}",
                app_name="Chat Grupal",
                timeout=5
            )
            # Simular ocultar la ventana
            sleep(1)
            print(f"\n{nombre}: {mensaje}")
        except Exception as e:
            print(f"Error recibiendo mensaje: {e}")

def enviar_mensajes(nombre, sock, destinos):
    while True:
        mensaje = input(f"{nombre}: ")
        mensaje_json = json.dumps({"msg": mensaje, "name": nombre})
        for dest_ip, dest_port in destinos:
            sock.sendto(mensaje_json.encode(), (dest_ip, dest_port))

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