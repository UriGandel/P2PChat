import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from tkinter import ttk
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
            sock.sendto(mensaje_formateado.encode(), (dest_ip, int(dest_port)))
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

def cargar_contactos():
    contactos = []
    try:
        with open("contactos.txt", "r") as f:
            for linea in f:
                nombre, ip = linea.strip().split(":")
                contactos.append((nombre, ip))
    except FileNotFoundError:
        print("Archivo de contactos no encontrado.")
    return contactos

def guardar_contacto(nombre, ip):
    with open("contactos.txt", "a") as f:
        f.write(f"{nombre}:{ip}\n")

def agregar_contacto():
    nombre = simpledialog.askstring("Nombre del contacto", "Introduce el nombre del contacto:", parent=root)
    if not nombre:
        return None, None
    ip = simpledialog.askstring("IP del contacto", "Introduce la dirección IP del contacto:", parent=root)
    if nombre and ip:
        guardar_contacto(nombre, ip)
        return (nombre, ip)
    else:
        messagebox.showwarning("Advertencia", "El nombre y la IP no pueden estar vacíos.", parent=root)
        return None, None

def seleccionar_contactos(contactos, ip_local):
    seleccionados = []

    def agregar_nuevo_contacto():
        nuevo_contacto = agregar_contacto()
        if nuevo_contacto[0] and nuevo_contacto[1]:
            contactos.append(nuevo_contacto)
            contactos_listbox.insert(tk.END, f"{nuevo_contacto[0]} ({nuevo_contacto[1]})")

    def seleccionar():
        nonlocal seleccionados
        for idx in contactos_listbox.curselection():
            seleccionados.append(contactos[idx])
        seleccion_contactos_win.destroy()

    seleccion_contactos_win = tk.Toplevel(root)
    seleccion_contactos_win.title("Seleccionar contactos")
    seleccion_contactos_win.geometry("300x350")
    seleccion_contactos_win.transient(root)
    seleccion_contactos_win.grab_set()
    root.eval(f'tk::PlaceWindow {str(seleccion_contactos_win)} center')
    
    ip_label = tk.Label(seleccion_contactos_win, text=f"Tu IP: {ip_local}:{PORT}")
    ip_label.pack(padx=10, pady=5)
    
    contactos_listbox = tk.Listbox(seleccion_contactos_win, selectmode=tk.MULTIPLE)
    for contacto in contactos:
        contactos_listbox.insert(tk.END, f"{contacto[0]} ({contacto[1]})")
    contactos_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    botones_frame = tk.Frame(seleccion_contactos_win)
    botones_frame.pack(pady=10)
    
    seleccionar_button = tk.Button(botones_frame, text="Seleccionar", command=seleccionar)
    seleccionar_button.grid(row=0, column=0, padx=5)
    
    agregar_button = tk.Button(botones_frame, text="Agregar Contacto", command=agregar_nuevo_contacto)
    agregar_button.grid(row=0, column=1, padx=5)
    
    seleccion_contactos_win.grab_set()
    root.wait_window(seleccion_contactos_win)

    return seleccionados

def abrir_ventana_seleccion_contactos():
    global destinos
    contactos = cargar_contactos()
    destinos = seleccionar_contactos(contactos, ip_local)
    if not destinos:
        messagebox.showinfo("Información", "No se seleccionaron destinos. Continuando con los contactos actuales.", parent=root)
    else:
        # Convertir contactos seleccionados en formato (IP, PORT)
        destinos = [(ip, PORT) for nombre, ip in destinos]

# Configuración del socket
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

seleccionar_contactos_button = tk.Button(root, text="Seleccionar Contactos", command=abrir_ventana_seleccion_contactos)
seleccionar_contactos_button.pack(padx=10, pady=5, side=tk.BOTTOM)

ocultar_button = tk.Button(root, text="Ocultar ventana", command=ocultar_ventana)
ocultar_button.pack(padx=10, pady=5, side=tk.BOTTOM)

mensaje_frame.columnconfigure(0, weight=1)

# Cargar contactos y seleccionar destinos
contactos = cargar_contactos()
if not contactos:
    if messagebox.askyesno("Sin contactos", "No se encontraron contactos. ¿Quieres añadir uno?", parent=root):
        nuevo_contacto = agregar_contacto()
        if nuevo_contacto[0] and nuevo_contacto[1]:
            contactos.append(nuevo_contacto)
            messagebox.showinfo("Contacto agregado", f"Contacto {nuevo_contacto[0]} agregado con éxito.", parent=root)
    else:
        root.destroy()

if not contactos:
    messagebox.showinfo("Información", "No se encontraron o añadieron contactos. El programa terminará.", parent=root)
    root.destroy()
else:
    destinos = seleccionar_contactos(contactos, ip_local)
    if not destinos:
        messagebox.showinfo("Información", "No se seleccionaron destinos. El programa terminará.", parent=root)
        root.destroy()
    else:
        # Convertir contactos seleccionados en formato (IP, PORT)
        destinos = [(ip, PORT) for nombre, ip in destinos]
        
        nombre_usuario = simpledialog.askstring("Nombre", "Introduce tu nombre:", parent=root)
        if not nombre_usuario:
            messagebox.showinfo("Información", "No se ingresó nombre. Continuando como invitado.", parent=root)
            nombre_usuario = f"Invitado({ip_local})"
        iniciar_chat()
        root.mainloop()
