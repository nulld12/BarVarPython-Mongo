
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import sys


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
    #Guarda las mesas en la variable
    mesitas = mesas.find()
    for mesa in mesitas:
        #muestra cada dato de la mesa por separado
        print("Número de Mesa:", mesa["numeroMesa"])
        print("Ubicación:", mesa["ubicacion"])
        print("Número de Comensales:", mesa["nComensales"])
        print("Estado:", mesa["estado"])
        print("Número de Reserva:", mesa["nReserva"])
        #espacio entre las mesas a la hora de mostrarlas
        print()


def cambiar_estado():
    #muestra las mesas
    ver_mesas()
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
            print("Estado inválido. Los estados válidos son: libre, ocupada, pagada, servida, proceso o bloqueada .")
    else:
        print("No se encontró ninguna mesa con ese ID.")


def reservar_mesa():
    # Solicita el número de personas
    n_personas = int(input("Ingrese el número de personas para la reserva: "))

    # busca mesas disponibles para el número de personas ingresado
    mesas_disponibles = mesas.find({"$or": [{"estado": "libre"}, {"estado": "ocupada"}], "nComensales": {"$gte": n_personas}})
    
    # Mostrar mesas disponibles
    print("Mesas disponibles para la reserva:")
    for mesa in mesas_disponibles:
        print("ID de Mesa:", mesa["numeroMesa"])
        print("Ubicación:", mesa["ubicacion"])
        print("Número de Comensales:", mesa["nComensales"])
        print("Estado:", mesa["estado"])
        print()

    # Solicita el ID de la mesa para la reserva
    id_mesa = int(input("Ingrese el ID de la mesa que desea reservar: "))

    # Verifica si la mesa está disponible y actualizar su estado a reservada
    mesa_reserva = mesas.find_one({"numeroMesa": id_mesa, "$or": [{"estado": "libre"}, {"estado": "ocupada"}], "nComensales": {"$gte": n_personas}})
    if mesa_reserva:
        mesas.update_one({"numeroMesa": id_mesa}, {"$set": {"estado": "reservada", "nReserva": "ID_RESERVA"}})
        print("La mesa se ha reservado correctamente.")
    else:
        print("La mesa no está disponible para la reserva.")

def ver_menu_mesa():
    return "hola"

def carta():
    print()
    """
    Carta de restaurante
    """
    print("Bar Var: Menu Restaurante"+"\n"+
    "1.Ver Consumiciones"+"\n"+
    "2.Agregar consumición a la carta"+"\n"+
    "3.Eliminar consumición"+ "\n"+ 
    "4.Salir al menu de camarero")
    print()
    dato = input("Por favor, Escoge la Opcion que seas:")
    if dato == "1":
        return ver_consumiciones()
    elif dato == "2":
        return agregar_consumicion()
    elif dato == "3":
        return eliminar_consumicion()
    elif dato == "4":
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

def agregar_consumicion():
    
    # tipo_alimento = input("¿Qué tipo de alimento quieres añadir (postre, bebida o comida)? ").lower()
    # # Verificar si el tipo de alimento es válido
    # if tipo_alimento not in ["postre", "bebida", "comida"]:
    #     print("Tipo de alimento no válido.")
    #     return
    
    # # Solicitar los datos del alimento
    # nuevo_alimento = {}
    # nuevo_alimento["id"] = int(input("ID del alimento: "))
    # nuevo_alimento["nombre"] = input("Nombre del alimento: ")
    # nuevo_alimento["precio"] = float(input("Precio del alimento: "))
    # nuevo_alimento["imagen"] = input("URI de la imagen del alimento: ")
    
    # # Verificar si ya existe un alimento con el mismo ID
    # for alimento_tipo in menuse[0][tipo_alimento + "s"]:
    #     if alimento_tipo["id"] == nuevo_alimento["id"]:
    #         print("Ya existe un alimento con ese ID.")
    #         return
    
    # # Añadir el nuevo alimento al tipo correspondiente en la colección
    #     menuse[0][tipo_alimento + "s"].insertOne(nuevo_alimento)
    # print("Alimento añadido correctamente.")
    return "hola"

def eliminar_consumicion():
    return "hola"





uri = "mongodb+srv://david:Q123321q@cluster0.nmh0cmf.mongodb.net/?retryWrites=true&w=majority"
#Crea un nuevo cliente para conectarse       
client = MongoClient(uri,ssl=True,tlsAllowInvalidCertificates=True)
database: Database= client.get_database("BarVar")
mesas:Collection = database.get_collection("mesas")
menuse:Collection = database.get_collection("menu")
pedidos:Collection = database.get_collection("pedidos")
tickets:Collection = database.get_collection("tickets")
#Hace un ping para comprobar el estado
try:
    client.admin.command('ping')
    print("Conexion Correcta")
    print()
except Exception as e:
    print(e)

menu()