####### AVISO #######
# El codigo presente no contiene signos diacríticos (excepto comentarios)
# debido a problemas con la codificación UTF-8 (Desconozco el motivo por el cual es incompatible, se supone que debería funcionar con normalidad)

import pymongo
from pymongo.errors import PyMongoError, OperationFailure, ServerSelectionTimeoutError 

# EJEMPLO DE URI: "mongodb+srv://<user>:<password>@tiendas.9i9e53f.mongodb.net/?appName=Tiendas"
MONGO_URI = "mongodb+srv://bmmostaceros_db_user:laboratorio6@tiendas.9i9e53f.mongodb.net/?appName=Tiendas" # URI de conexión a MongoDB Atlas
DATABASE_NAME = "Tienda"
COLECCIONES = ["empleados", "productos", "clientes", "ventas"] # Lista de colecciones creadas

class TiendaDB:
    def __init__(self, uri=MONGO_URI, db_name=DATABASE_NAME):
        self.client = None
        self.db = None
        try:
            # Intentar la conexión con un timeout de 5 segundos
            self.client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Forzar la verificación de la conexión con el comando 'ping'
            self.client.admin.command('ping') 
            print(f"Conexion a MongoDB exitosa. Base de datos: {db_name}")
            self.db = self.client[db_name]
        except ServerSelectionTimeoutError:
            # Captura si el servidor no responde dentro del timeout
            print(f"Error de conexion: Asegurate de que MongoDB este corriendo en {uri} y es accesible.")
            self.client = None
        except PyMongoError as e:
            # Captura errores generales de PyMongo
            print(f"Error de PyMongo (conexion): {e}")
            self.client = None
        except Exception as e:
            # Captura cualquier otro error durante la inicialización
            print(f"Ocurrio un error inesperado al conectar: {e}")
            self.client = None

    def _get_collection(self, coleccion_nombre):
        # Validación de seguridad: Comprueba que la colección esté en la lista permitida
        if coleccion_nombre not in COLECCIONES:
            raise ValueError(f"Coleccion invalida: {coleccion_nombre}. Debe ser una de: {COLECCIONES}")
        return self.db[coleccion_nombre]

    # Función: CREATE 
    def CREATE(self, coleccion_nombre, documento):
        try:
            coleccion = self._get_collection(coleccion_nombre)
            # Validación: El documento debe ser un diccionario no vacío
            if not isinstance(documento, dict) or not documento:
                print("Error: El documento debe ser un diccionario no vacio.")
                return None
            
            resultado = coleccion.insert_one(documento)
            print(f"+ Documento insertado en '{coleccion_nombre}' con ID: {resultado.inserted_id}")
            return resultado.inserted_id
        except ValueError as e:
            print(f"Error en la operacion CREATE: {e}") # Error de colección inválida
        except OperationFailure as e:
            print(f"Error de operacion en MongoDB (CREATE): {e}") # Por ejemplo, violación de índice único
        except PyMongoError as e:
            print(f"Error de PyMongo (CREATE): {e}")
        except Exception as e:
            print(f"Error inesperado (CREATE): {e}")
        return None

    # Función: READ
    def READ(self, coleccion_nombre, filtro=None, proyeccion=None):
        try:
            coleccion = self._get_collection(coleccion_nombre)
            # Validación: El filtro debe ser None o un diccionario
            if filtro is not None and not isinstance(filtro, dict):
                 print("Error: El filtro debe ser un diccionario.")
                 return []
            # Si el filtro es None, se usa {} para buscar todos los documentos
            filtro = filtro if filtro is not None else {}
            # "list()" ejecuta el cursor y devuelve los resultados
            documentos = list(coleccion.find(filtro, proyeccion))
            
            if documentos:
                print(f"- Encontrados {len(documentos)} documentos en '{coleccion_nombre}'.")
            else:
                print(f"- No se encontraron documentos en '{coleccion_nombre}' con el filtro: {filtro}")
                
            return documentos
            
        except ValueError as e:
            print(f"Error en la operacion READ: {e}")
        except PyMongoError as e:
            print(f"Error de PyMongo (READ): {e}")
        except Exception as e:
            print(f"Error inesperado (READ): {e}")
        return []

    # Función UPDATE
    def UPDATE(self, coleccion_nombre, filtro, actualizacion):
        try:
            coleccion = self._get_collection(coleccion_nombre)
            # Validación de seguridad: El filtro debe ser un diccionario no vacío
            if not isinstance(filtro, dict) or not filtro:
                print("Error: El filtro debe ser un diccionario no vacio.") # Previene update_one({})
                return 0
            # Validación: La actualización debe ser un diccionario no vacío
            if not isinstance(actualizacion, dict) or not actualizacion:
                print("Error: La actualizacion debe ser un diccionario no vacio.")
                return 0
            # BUENA PRÁCTICA: Si no hay operador de actualización ($set, $inc, etc.), usa $set por defecto
            if not any(key.startswith('$') for key in actualizacion):
                 print("! Advertencia: La actualizacion deberia usar operadores como $set.")
                 actualizacion = {"$set": actualizacion}

            # Actualiza solo el primer documento que coincida con el filtro
            resultado = coleccion.update_one(filtro, actualizacion)
            print(f"- Documentos modificados en '{coleccion_nombre}': {resultado.modified_count}")
            return resultado.modified_count
            
        except ValueError as e:
            print(f"Error en la operacion UPDATE: {e}")
        except OperationFailure as e:
            print(f"Error de operacion en MongoDB (UPDATE): {e}")
        except PyMongoError as e:
            print(f"Error de PyMongo (UPDATE): {e}")
        except Exception as e:
            print(f"Error inesperado (UPDATE): {e}")
        return 0

    # Función: DELETE
    def DELETE(self, coleccion_nombre, filtro):
        try:
            coleccion = self._get_collection(coleccion_nombre)
            # Validación de seguridad: El filtro debe ser un diccionario no vacío
            if not isinstance(filtro, dict) or not filtro:
                print("Error: El filtro debe ser un diccionario no vacio.") # Previene delete_one({})
                return 0
            # Elimina solo el primer documento que coincida con el filtro
            resultado = coleccion.delete_one(filtro)
            print(f"- Documentos eliminados en '{coleccion_nombre}': {resultado.deleted_count}")
            return resultado.deleted_count
            
        except ValueError as e:
            print(f"Error en la operacion DELETE: {e}")
        except PyMongoError as e:
            print(f"Error de PyMongo (DELETE): {e}")
        except Exception as e:
            print(f"Error inesperado (DELETE): {e}")
        return 0

def verificar_funciones():
    db_manager = TiendaDB()
    
    # Comprobación de que la conexión fue exitosa antes de continuar
    if not db_manager.client:
        print("\n--- Las pruebas CRUD no se ejecutaran debido a la falla de conexion.")
        return

    COL_PRUEBA = "empleados"
    
    print("\n=========================")
    print("\n== 1. OPERACIONES CRUD ==")
    print("\n=========================")

    print("\n1.1 READ")
    empleados = db_manager.READ(COL_PRUEBA) # Lectura total
    empleados_activos = db_manager.READ(COL_PRUEBA, {"activo": True}) # Lectura filtrada
    print(f"Empleados activos encontrados: {len(empleados_activos)}")

    print("\n1.2 CREATE")
    nuevo_empleado = {"nombre": "Test User", "puesto": "Practicante", "activo": True}
    nuevo_id = db_manager.CREATE(COL_PRUEBA, nuevo_empleado) # Almacena el ID generado
    
    print("\n1.3 UPDATE")
    if nuevo_id:
        filtro_update = {"_id": nuevo_id}
        actualizacion = {"puesto": "Supervisor", "activo": False} # No usa operador $set, la clase lo añade
        db_manager.UPDATE(COL_PRUEBA, filtro_update, actualizacion)
        
        print("Documento actualizado (leido):", db_manager.READ(COL_PRUEBA, filtro_update)) # Lee el documento modificado

    print("\n1.4 DELETE")
    if nuevo_id:
        eliminados = db_manager.DELETE(COL_PRUEBA, {"_id": nuevo_id}) # Elimina por ID
        print(f"Documentos eliminados: {eliminados}")

    print("\n========================================")
    print("\n== 2. PRUEBAS DE ERRORES Y VALIDACION ==")
    print("\n========================================")

    print("\n2.1 Prueba de error: Documento nulo ---")
    db_manager.CREATE(COL_PRUEBA, None) # Prueba la validación de diccionario no vacío

    print("\n2.2 Prueba de error: Filtro vacio en UPDATE ---")
    db_manager.UPDATE(COL_PRUEBA, {}, {"$set": {"salario": 0}}) # Prueba la validación de filtro no vacío

    print("\n2.3 Prueba de error: Coleccion invalida en DELETE ---")
    db_manager.DELETE("coleccion_fantasma", {"nombre": "cualquiera"}) # Prueba la validación de colección permitida

    print("\n///FINAL DE PRUEBAS///")
    
if __name__ == "__main__":
    verificar_funciones()
