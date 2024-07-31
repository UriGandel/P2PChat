from mensajes import obtener_ip_local

config = {}

def parse_toml(file: str) -> dict:
    toml = open(f"{file}.toml", "r")
    config = {}
    keyword: str;
    value: any;
    for line in toml:
        line = line.split(" ")
        keyword = line[0]
        value = line[2]
        config[keyword] = value
    print(config)
    return config
                

def cargar_config(file="chat") -> dict:
    '''Carga la configuración, si no la encuentra utiliza la ip como nombre'''
    try:
        print(f"reading {file}.toml")
        return parse_toml(file)
    except FileNotFoundError as e:
        print(f"File {file}.toml not found, using defaults")
        config["name"] = obtener_ip_local()
        return config