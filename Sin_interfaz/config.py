from mensajes import obtener_ip_local

config = {
    "name": None,
}

def cargar_config(file="chat") -> dict:
    '''Carga la configuración, si no la encuentra utiliza la ip como nombre'''
    try:
        config_file = open(f"{file}.toml", "r")
    except FileNotFoundError:
        print(f"File {file}.toml not found, using defaults")
        config["name"] = obtener_ip_local()
        return config