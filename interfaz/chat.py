import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

PORT = 12345        

def recibir_mensajes(sock, chat_box):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            mensaje = f"\n{addr[0]}: {data.decode()}"
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, mensaje)
            chat_box.config(state=tk.DISABLED)
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

def enviar(event=None):
    mensaje = mensaje_entry.get()
    if mensaje:
        enviar_mensajes(sock, destinos, mensaje)
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"\nTú: {mensaje}")
        chat_box.config(state=tk.DISABLED)
        mensaje_entry.delete(0, tk.END)

def iniciar_chat():
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(sock, chat_box))
    hilo_recibir.daemon = True
    hilo_recibir.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))  

ip_local = obtener_ip_local()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Chat Grupal")
root.geometry("400x485")

# Mostrar la IP local
ip_label = tk.Label(root, text=f"Tu IP: {ip_local}:{PORT}")
ip_label.pack(padx=10, pady=5)

chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

mensaje_frame = tk.Frame(root)
mensaje_frame.pack(padx=10, pady=10, fill=tk.X)

mensaje_entry = tk.Entry(mensaje_frame)
mensaje_entry.pack(fill=tk.X)
mensaje_entry.grid(row=0, column=0, sticky="ew")
mensaje_entry.bind("<Return>", enviar)

enviar_button = tk.Button(mensaje_frame, text="Enviar", command=enviar)
enviar_button.grid(row=0, column=1)
root.attributes('-topmost', True)

mensaje_frame.columnconfigure(0, weight=1)

destinos = []
while True:
    dest_ip = simpledialog.askstring("Dirección IP", "Introduce la dirección IP del compañero (o 'fin' para terminar):")
    if not dest_ip or dest_ip.lower() == 'fin':
        break
    destinos.append((dest_ip, PORT))

if not destinos:
    messagebox.showinfo("Información", "No se ingresaron destinos. El programa terminará.")
    root.destroy()
else:
    iniciar_chat()
    root.mainloop()
