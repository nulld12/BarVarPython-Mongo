
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import sys
import uuid


def menu():
    """
    Menu
    """
    print("Bar Var: Acceso Camarero"+"\n"+
    "1.Ver mesas"+"\n"+
    "2.Cambiar estado"+"\n"+
    "3.Reservar mesa"+ "\n"+ 
    "4.Consumiciones mesa"+"\n"+
    "5.Carta restaurante")

    print()
    dato = input("Por favor, Escoge la Opcion que seas: ")
    if dato == "1":
        return ver_mesas()
    elif dato == "2":
        return cambiar_estado()
    elif dato == "3":
        return reservar_mesa()
    elif dato == "4":
        return ver_menu_mesa()
    elif dato == "5":
        return  carta()
    else :
        return sys.exit("Vuelva Pronto")

def ver_mesas():
    # Guarda las mesas en la variable
    mesitas = mesas.find()
    for mesa in mesitas:
        # Muestra cada dato de la mesa por separado
        print("Número de Mesa:", mesa["numeroMesa"])
        print("Ubicación:", mesa["ubicacion"])
        print("Número de Comensales:", mesa["nComensales"])
        print("Estado:", mesa["estado"])
        print("Número de Reserva:", mesa["nReserva"])
        # Espacio entre las mesas a la hora de mostrarlas
        print()
    menu()


def cambiar_estado():
    # Muestra las mesas
    mesitas = mesas.find()
    for mesa in mesitas:
        # Muestra cada dato de la mesa por separado
        print("Número de Mesa:", mesa["numeroMesa"])
        print("Ubicación:", mesa["ubicacion"])
        print("Número de Comensales:", mesa["nComensales"])
        print("Estado:", mesa["estado"])
        print("Número de Reserva:", mesa["nReserva"])
        # Espacio entre las mesas a la hora de mostrarlas
        print()
    print()
    # Solicita el ID de la mesa
    id_mesa = int(input("Ingrese el ID de la mesa que desea actualizar: "))

    # Busca la mesa por su ID
    mesa = mesas.find_one({"numeroMesa": id_mesa})

    # Verifica si se encontró la mesa
    if mesa:
        # Solicitar el nuevo estado
        nuevo_estado = input("Ingrese el nuevo estado de la mesa (libre, ocupada, pagada, proceso, servida, bloqueada ): ").lower()

        # Verifica que el nuevo estado sea válido
        if nuevo_estado in ["libre", "ocupada", "bloqueada","pagada","proceso","servida"]:
            # Actualiza el estado de la mesa en la base de datos
            mesas.update_one({"numeroMesa": id_mesa}, {"$set": {"estado": nuevo_estado}})
            print("El estado de la mesa se ha actualizado correctamente.")
        else:
            print("Estado inválido. Los estados válidos son: libre, ocupada, pagada, servida, proceso o bloqueada.")
    else:
        print("No se encontró ninguna mesa con ese ID.")
    
    menu()  

#genera un nuevo uuid de 4 y coge
def generate_and_extract_prefix():
    reservation_id = str(uuid.uuid4())
    # Coge los caracteres antes del primer guion
    prefix = reservation_id.split('-')[0]
    return prefix
    
def reservar_mesa():
    # Solicita el número de personas
    n_personas = int(input("Ingrese el número de personas para la reserva: "))

    # Busca mesas disponibles para el número de personas ingresado y con estado "libre"
    mesas_disponibles = mesas.find({"estado": "libre", "nComensales": {"$gte": n_personas}})
    
    # Mostrar mesas disponibles para la reserva
    print("Mesas disponibles para la reserva:")
    for mesa in mesas_disponibles:
        print("ID de Mesa:", mesa["numeroMesa"])
        print("Ubicación:", mesa["ubicacion"])
        print("Número de Comensales:", mesa["nComensales"])
        print("Estado:", mesa["estado"])
        print()

    # Solicita el ID de la mesa para la reserva
    id_mesa = int(input("Ingrese el ID de la mesa que desea reservar: "))

    # Verifica si la mesa está disponible y su estado es "libre" para reservar
    mesa_reserva = mesas.find_one({"numeroMesa": id_mesa, "estado": "libre", "nComensales": {"$gte": n_personas}})
    if mesa_reserva:
        # Actualizar estado de la mesa a "reservada" y asignar un número de reserva
        mesas.update_one({"numeroMesa": id_mesa}, {"$set": {"estado": "reservada", "nReserva": generate_and_extract_prefix()}})
        print("La mesa se ha reservado correctamente.")
    else:
        print("La mesa no está disponible para la reserva.")
    menu()

def ver_menu_mesa(): 
    numero_mesa = input("Ingrese el número de mesa: ")
    numero_mesa = int(numero_mesa)
    print(numero_mesa)
    pedidos_mesa = pedidos.find({'nMesa': numero_mesa})
    # Mostrar los pedidos encontrados
    print("Pedidos encontrados para la mesa", numero_mesa, ":")
    print("------------------------------------------------------------")
    for pedido in pedidos_mesa:
        print("Pedido ID:", pedido['_id'])
        print("Fecha:", pedido['fecha'])
        print("Importe:", pedido['importe'])
        print("Número de Mesa:", pedido['nMesa'])
        print("Detalles del pedido:")
        for detalle_pedido in pedido['pedido']:
            print("  Nombre:", detalle_pedido['nombre'])
            print("  Precio:", detalle_pedido['precio'])
            print("  Cantidad:", detalle_pedido['cantidad'])
            print("  ID:", detalle_pedido['_id'])
            print("------------------------------------------------------------")
    print("\n")  
    menu()


def carta():
    print()
    """
    Carta de restaurante
    """
    print("Bar Var: Carta Restaurante"+"\n"+
    "1.Ver Consumiciones"+"\n"+
    "2.Agregar consumición a la carta"+"\n"+
    "3.Salir al menu de camarero")
    print()
    dato = input("Por favor, Escoge la Opcion que seas:")
    if dato == "1":
        return ver_consumiciones()
    elif dato == "2":
        return agregar_consumicion()
    elif dato == "3":
        return menu()
    else :
        return sys.exit("Vuelva Pronto")

def ver_consumiciones():
    menusito = menuse.find_one()
    if menusito is not None:
        # Iterar sobre las secciones del menú y sus elementos
        for seccion, elementos in menusito.items():  # Iterar sobre claves y valores
            # Ignorar el campo "_id"
            if seccion != "_id":
                # Capitalizar la primera letra del nombre de la sección si es una cadena para mostrarla como titulo
                if isinstance(seccion, str):
                    seccion_capitalizada = seccion[0].upper() + seccion[1:]
                    print(f"--- {seccion_capitalizada} ---")
                    for elemento in elementos:
                        print("ID:", elemento["id"])
                        print("Nombre:", elemento["nombre"])
                        print("Precio: ${}".format(elemento["precio"]))
                        print("Imagen:", elemento["imagen"])
                        print()
    else:
        print("No se encontró ningún menú en la base de datos.")
    carta()

def agregar_consumicion():

    tipo_elemento = input("¿Qué tipo de elemento desea agregar (bebida, comida o postre)? ").lower()
    
    # Solicitar los datos del nuevo elemento
    id_elemento = int(input("Ingrese el id del nuevo elemento: ").strip())
    nombre = input("Ingrese el nombre del nuevo elemento: ").strip()
    precio = float(input("Ingrese el precio del nuevo elemento: ").strip())
    imagen = input("Ingrese la URL de la imagen del nuevo elemento: ").strip()
    
    # Verificar si el ID ya existe en alguna de las subcolecciones
    if tipo_elemento == "bebida":
        if menuse.find_one({"bebidas.id": id_elemento}):
            print("Ya existe un elemento en las bebidas con el mismo ID.")
            return
    elif tipo_elemento == "comida":
        if menuse.find_one({"comidas.id": id_elemento}):
            print("Ya existe un elemento en las comidas con el mismo ID.")
            return
    elif tipo_elemento == "postre":
        if menuse.find_one({"postres.id": id_elemento}):
            print("Ya existe un elemento en los postres con el mismo ID.")
            return
    else:
        print("Tipo de elemento inválido. Los tipos válidos son: bebida, comida o postre.")
        return
    
    # Crear el nuevo objeto
    nuevo_elemento = {
        "id": id_elemento,
        "nombre": nombre,
        "precio": precio,
        "imagen": imagen
    }
    
    # Determinar la colección correspondiente y agregar el nuevo elemento
    if tipo_elemento == "bebida":
        menuse.update_one({}, {"$push": {"bebidas": nuevo_elemento}})
        print("Elemento añadido correctamente a las bebidas.")
    elif tipo_elemento == "comida":
        menuse.update_one({}, {"$push": {"comidas": nuevo_elemento}})
        print("Elemento añadido correctamente a las comidas.")
    elif tipo_elemento == "postre":
        menuse.update_one({}, {"$push": {"postres": nuevo_elemento}})
        print("Elemento añadido correctamente a los postres.")
    else:
        print("Tipo de elemento inválido. Los tipos válidos son: bebida, comida o postre.")
    carta()



uri = "mongodb+srv://david:Q123321q@cluster0.nmh0cmf.mongodb.net/?retryWrites=true&w=majority"
# Crea un nuevo cliente para conectarse  
client = MongoClient(uri,ssl=True,tlsAllowInvalidCertificates=True)
database: Database= client.get_database("BarVar")
mesas:Collection = database.get_collection("mesas")
menuse:Collection = database.get_collection("menu")
pedidos:Collection = database.get_collection("pedidos")
tickets:Collection = database.get_collection("tickets")
# Hace un ping para comprobar el estado
try:
    client.admin.command('ping')
    print("Conexion Correcta")
    print()
except Exception as e:
    print(e)

menu()