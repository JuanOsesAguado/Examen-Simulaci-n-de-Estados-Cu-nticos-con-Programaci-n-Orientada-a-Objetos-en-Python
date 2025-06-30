import cmath
from src.estado_cuantico import EstadoCuantico
from src.operador_cuantico import OperadorCuantico
from src.repositorio_estados import RepositorioDeEstados

def obtener_vector_complejo_del_usuario() -> List[complex]:
    """Solicita al usuario componentes complejas para el vector."""
    vector_str = input("Introduce las amplitudes del vector (ej. '0.707+0j, 0.707+0j'): ")
    components_str = [comp.strip() for comp in vector_str.split(',')]
    vector = []
    for comp_str in components_str:
        try:
            # Evaluar la cadena para obtener el número complejo
            vector.append(complex(comp_str))
        except ValueError:
            print(f"Advertencia: '{comp_str}' no es un número complejo válido. Intentando como float.")
            try:
                vector.append(complex(float(comp_str)))
            except ValueError:
                print(f"Error: '{comp_str}' no es un número válido. Se omitirá.")
    return vector

def menu():
    """Muestra el menú de opciones al usuario."""
    print("\n--- Simulador de Estados Cuánticos ---")
    print("1. Listar estados cuánticos")
    print("2. Registrar nuevo estado cuántico")
    print("3. Aplicar operador cuántico a un estado")
    print("4. Medir un estado cuántico")
    print("5. Guardar estados a archivo")
    print("6. Cargar estados desde archivo")
    print("0. Salir")
    print("--------------------------------------")

def main():
    repo = RepositorioDeEstados()
    
    # Operadores cuánticos predefinidos para facilitar la prueba
    # Puerta X (NOT cuántico)
    op_x = OperadorCuantico("X", [[0, 1], [1, 0]])
    # Puerta Hadamard
    op_h = OperadorCuantico("H", [[1/cmath.sqrt(2), 1/cmath.sqrt(2)], [1/cmath.sqrt(2), -1/cmath.sqrt(2)]])
    # Puerta Z
    op_z = OperadorCuantico("Z", [[1, 0], [0, -1]])

    # Diccionario de operadores disponibles
    operadores_disponibles = {
        "X": op_x,
        "H": op_h,
        "Z": op_z
    }

    # Intentar cargar estados al inicio si el archivo existe
    repo.cargar("estados.json")

    while True:
        menu()
        choice = input("Selecciona una opción: ")

        if choice == '1':
            print("\n--- Estados Cuánticos Registrados ---")
            for estado_str in repo.listar_estados():
                print(estado_str)
        
        elif choice == '2':
            print("\n--- Registrar Nuevo Estado Cuántico ---")
            id_estado = input("Introduce el ID del nuevo estado: ")
            vector = obtener_vector_complejo_del_usuario()
            base = input("Introduce la base del estado (ej. 'computacional'): ")
            if vector: # Asegurarse de que el vector no esté vacío
                repo.agregar_estado(id_estado, vector, base)

        elif choice == '3':
            print("\n--- Aplicar Operador Cuántico ---")
            id_estado = input("Introduce el ID del estado al que aplicar el operador: ")
            
            print("Operadores disponibles:")
            for op_name in operadores_disponibles:
                print(f"- {op_name}")
            
            op_nombre = input("Introduce el nombre del operador a aplicar (ej. 'H' o 'X'): ").upper()
            operador = operadores_disponibles.get(op_nombre)

            if operador:
                nuevo_id_opcion = input(f"Introduce un nuevo ID para el estado transformado (dejar vacío para '{id_estado}_{operador.nombre}'): ")
                repo.aplicar_operador(id_estado, operador, nuevo_id_opcion if nuevo_id_opcion else None)
            else:
                print(f"Error: Operador '{op_nombre}' no reconocido.")

        elif choice == '4':
            print("\n--- Medir Estado Cuántico ---")
            id_estado = input("Introduce el ID del estado a medir: ")
            repo.medir_estado(id_estado)

        elif choice == '5':
            filename = input("Introduce el nombre del archivo para guardar (ej. 'estados.json'): ")
            repo.guardar(filename)

        elif choice == '6':
            filename = input("Introduce el nombre del archivo para cargar (ej. 'estados.json'): ")
            repo.cargar(filename)

        elif choice == '0':
            print("Saliendo del simulador. ¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()