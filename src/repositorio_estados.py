import json
import os
from typing import Dict, List, Optional, Union
from src.estado_cuantico import EstadoCuantico
from src.operador_cuantico import OperadorCuantico

class RepositorioDeEstados:
    """
    Gestiona el conjunto de estados cuánticos registrados.

    Almacena los estados en un diccionario, donde la clave es el identificador (id)
    y el valor es el objeto EstadoCuantico correspondiente.
    """

    def __init__(self):
        self._estados: Dict[str, EstadoCuantico] = {}

    def listar_estados(self) -> List[str]:
        """
        Retorna una lista de descripciones legibles de todos los estados almacenados.

        Retorna:
            List[str]: Una lista de cadenas que describen cada estado.
        """
        if not self._estados:
            return ["No hay estados cuánticos registrados."]
        return [str(estado) for estado in self._estados.values()]

    def agregar_estado(self, id: str, vector: List[Union[float, complex]], base: str) -> bool:
        """
        Crea y añade un nuevo estado cuántico al repositorio.

        Args:
            id (str): Identificador único del estado.
            vector (List[Union[float, complex]]): Vector de amplitudes.
            base (str): Base asociada al estado.

        Retorna:
            bool: True si el estado fue agregado, False si el ID ya existe.
        """
        if id in self._estados:
            print(f"Error: Ya existe un estado con el identificador '{id}'.")
            return False
        try:
            # Convertir el vector a List[complex] si contiene floats
            complex_vector = [complex(amp) for amp in vector]
            nuevo_estado = EstadoCuantico(id, complex_vector, base)
            self._estados[id] = nuevo_estado
            print(f"Estado '{id}' agregado exitosamente.")
            return True
        except ValueError as e:
            print(f"Error al agregar estado: {e}")
            return False

    def obtener_estado(self, id: str) -> Optional[EstadoCuantico]:
        """
        Busca y retorna el objeto EstadoCuantico con el identificador dado.

        Args:
            id (str): El identificador del estado a buscar.

        Retorna:
            Optional[EstadoCuantico]: El objeto EstadoCuantico si se encuentra,
                                     None en caso contrario.
        """
        estado = self._estados.get(id)
        if estado is None:
            print(f"Error: No se encontró un estado con el identificador '{id}'.")
        return estado

    def aplicar_operador(self, id_estado: str, operador: OperadorCuantico, nuevo_id: Optional[str] = None) -> bool:
        """
        Toma un estado existente, le aplica un operador cuántico y registra el resultado.

        Args:
            id_estado (str): El identificador del estado al que se aplicará el operador.
            operador (OperadorCuantico): El operador a aplicar.
            nuevo_id (Optional[str]): El identificador para el nuevo estado resultante.
                                      Si es None, se generará uno derivado.

        Retorna:
            bool: True si el operador se aplicó y el estado se registró, False en caso contrario.
        """
        estado = self.obtener_estado(id_estado)
        if estado is None:
            return False

        try:
            estado_transformado = operador.aplicar(estado)
            final_id = nuevo_id if nuevo_id is not None else f"{id_estado}_{operador.nombre}"

            if final_id in self._estados and final_id != id_estado:
                print(f"Advertencia: El nuevo ID '{final_id}' ya existe. Sobrescribiendo.")
            
            # Actualizar el ID del estado transformado si se proporcionó un nuevo_id
            # o si se generó uno nuevo y no es el original.
            estado_transformado._id = final_id 
            self._estados[final_id] = estado_transformado
            print(f"Operador '{operador.nombre}' aplicado a '{id_estado}'. "
                  f"Nuevo estado registrado como '{final_id}'.")
            return True
        except ValueError as e:
            print(f"Error al aplicar operador: {e}")
            return False

    def medir_estado(self, id: str) -> bool:
        """
        Mide un estado cuántico registrado y muestra sus probabilidades.

        Args:
            id (str): El identificador del estado a medir.

        Retorna:
            bool: True si el estado fue medido y las probabilidades mostradas, False si no se encontró.
        """
        estado = self.obtener_estado(id)
        if estado is None:
            return False

        probabilities = estado.medir()
        print(f"\nMedición del estado '{estado.id}' (base {estado.base}):")
        for outcome, prob in probabilities.items():
            print(f"  - Estado base |{outcome}⟩: {prob:.4f} ({prob*100:.2f}%)")
        return True

    def guardar(self, archivo: str) -> bool:
        """
        Guarda la colección de estados cuánticos a un archivo JSON.

        Args:
            archivo (str): La ruta del archivo donde se guardarán los estados.

        Retorna:
            bool: True si los estados se guardaron exitosamente, False en caso contrario.
        """
        try:
            list_of_states_data = []
            for estado in self._estados.values():
                # JSON no soporta números complejos directamente.
                # Convertimos cada parte compleja a un diccionario {real, imag}.
                # O si estamos asumiendo solo floats, se puede dejar tal cual.
                # Para simplificar y mantener la flexibilidad, convertimos a string.
                # Una alternativa robusta sería una serialización personalizada con __json__ o similar.
                serializable_vector = [[amp.real, amp.imag] for amp in estado.vector]

                list_of_states_data.append({
                    "id": estado.id,
                    "base": estado.base,
                    "vector": serializable_vector
                })

            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(list_of_states_data, f, indent=4)
            print(f"Estados guardados exitosamente en '{archivo}'. ({len(self._estados)} estados)")
            return True
        except IOError as e:
            print(f"Error al guardar los estados en '{archivo}': {e}")
            return False
        except Exception as e:
            print(f"Ocurrió un error inesperado al guardar: {e}")
            return False

    def cargar(self, archivo: str) -> bool:
        """
        Carga estados cuánticos desde un archivo JSON, sobrescribiendo los estados actuales.

        Args:
            archivo (str): La ruta del archivo desde donde se cargarán los estados.

        Retorna:
            bool: True si los estados se cargaron exitosamente, False en caso contrario.
        """
        if not os.path.exists(archivo):
            print(f"Error: El archivo '{archivo}' no existe.")
            return False
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                list_of_states_data = json.load(f)

            self._estados.clear() # Limpiar estados actuales antes de cargar
            for state_data in list_of_states_data:
                id_ = state_data["id"]
                base = state_data["base"]
                # Convertir el vector de nuevo a List[complex]
                vector_raw = state_data["vector"]
                vector = [complex(amp[0], amp[1]) for amp in vector_raw]

                # Usamos el método interno para evitar mensajes de "ya existe" durante la carga masiva
                self._estados[id_] = EstadoCuantico(id_, vector, base)
            print(f"Estados cargados exitosamente desde '{archivo}'. ({len(self._estados)} estados)")
            return True
        except json.JSONDecodeError as e:
            print(f"Error de formato JSON al cargar desde '{archivo}': {e}")
            return False
        except KeyError as e:
            print(f"Error: Datos faltantes en el archivo JSON (clave '{e}' no encontrada).")
            return False
        except Exception as e:
            print(f"Ocurrió un error inesperado al cargar: {e}")
            return False