import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from plyer import notification
PORT = 12345

def recibir_mensajes(sock, chat_box, root):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            data = data.decode().split(":", 1)
            nombre = data[0]
            mensaje = data[1]
            mensaje_formateado = f"\n{nombre}: {mensaje}"
            root.after(0, actualizar_chat_box, chat_box, mensaje_formateado, root, addr)
        except Exception as e:
            print(f"Error recibiendo mensaje: {e}")
            break

def actualizar_chat_box(chat_box, mensaje, root, addr):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, mensaje)
    chat_box.config(state=tk.DISABLED)
    notification.notify(
        title="Nuevo mensaje",
        message=f"Mensaje de {mensaje.split(':', 1)[0]}",
        app_name="Chat Grupal",
        timeout=5
    )
    root.deiconify()

def enviar_mensajes(sock, destinos, nombre, mensaje):
    mensaje_formateado = f"{nombre}:{mensaje}"
    for dest_ip, dest_port in destinos:
        try:
            sock.sendto(mensaje_formateado.encode(), (dest_ip, dest_port))
        except Exception as e:
            print(f"Error enviando mensaje a {dest_ip}: {e}")

def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def enviar(event=None):
    mensaje = mensaje_entry.get()
    if mensaje:
        enviar_mensajes(sock, destinos, nombre_usuario, mensaje)
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"\nTú: {mensaje}")
        chat_box.config(state=tk.DISABLED)
        mensaje_entry.delete(0, tk.END)

def ocultar_ventana():
    root.withdraw()

def iniciar_chat():
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(sock, chat_box, root))
    hilo_recibir.daemon = True
    hilo_recibir.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))

ip_local = obtener_ip_local()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.attributes('-topmost', True)
root.title("Chat Grupal")
root.geometry("400x520")



# Mostrar la IP local
ip_label = tk.Label(root, text=f"Tu IP: {ip_local}:{PORT}")
ip_label.pack(padx=10, pady=5)

chat_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

mensaje_frame = tk.Frame(root)
mensaje_frame.pack(padx=10, pady=10, fill=tk.X)

mensaje_entry = tk.Entry(mensaje_frame)
mensaje_entry.grid(row=0, column=0, sticky="ew")
mensaje_entry.bind("<Return>", enviar)

enviar_button = tk.Button(mensaje_frame, text="Enviar", command=enviar)
enviar_button.grid(row=0, column=1)

ocultar_button = tk.Button(root, text="Ocultar ventana", command=ocultar_ventana)
ocultar_button.pack(padx=10, pady=5, side=tk.BOTTOM)

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
    nombre_usuario = simpledialog.askstring("Nombre", "Introduce tu nombre:")
    if not nombre_usuario:
        messagebox.showinfo("Información", "No se ingresó nombre.Continuando como invitado.")
        nombre_usuario = f"Invitado({dest_ip})"
    iniciar_chat()
    root.mainloop()
