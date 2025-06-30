# Examen-Simulaci-n-de-Estados-Cu-nticos-con-Programaci-n-Orientada-a-Objetos-en-Python

https://github.com/JuanOsesAguado/Examen-Simulaci-n-de-Estados-Cu-nticos-con-Programaci-n-Orientada-a-Objetos-en-Python.git

Explicación de las Opciones de Diseño y Características:


Clase EstadoCuantico
Atributos: _id (cadena), _vector (lista de números complejos), _base (cadena). Estos atributos se hacen privados con guiones bajos iniciales, y se proporcionan captadores de propiedades públicos para acceso de solo lectura, lo que facilita la encapsulación.

Tipo de vector: El vector se almacena explícitamente como List[complex]. Esto gestiona componentes reales e imaginarios sin problemas. El constructor garantiza que todas las amplitudes de entrada se conviertan a números complejos.

Normalización: Se llama al método auxiliar privado _normalizar_vector en __init__ para garantizar que el vector de estado cuántico siempre esté normalizado (la suma de las magnitudes al cuadrado es igual a 1). Esto es crucial para las probabilidades.

Método medir(): Calcula las probabilidades tomando el cuadrado absoluto de cada amplitud. Devuelve un diccionario que asigna los índices de cadena ("0", "1", etc.) a sus respectivas probabilidades, un formato claro y flexible. No modifica el estado, como se solicita.

__str__ y __repr__: Proporcionan representaciones de cadena intuitivas e inequívocas del estado cuántico, lo que facilita la depuración y la visualización.

Clase OperadorCuantico
Atributos: _nombre (cadena) y _matriz (lista de listas de números complejos).

Tipo Matriz: Similar a EstadoCuantico, los elementos de la matriz se almacenan como complejos para admitir operaciones cuánticas generales.

Método aplicar(): Implementa la multiplicación matriz-vector manualmente, iterando por filas y columnas. Esto evita dependencias externas como NumPy, como se especifica como opción. Si se prefiriera NumPy, np.dot(self.matriz, estado.vector) simplificaría esto.

Inmutabilidad del Estado: El método aplicar() devuelve un nuevo objeto EstadoCuantico con el vector transformado, en lugar de modificar el estado original. Esta es una buena práctica, ya que evita efectos secundarios no deseados y permite el seguimiento de la evolución de los estados.

Generación de ID: Genera automáticamente un nuevo ID para el estado transformado (p. ej., "q0_H") para su trazabilidad, a menos que se proporcione explícitamente un nuevo_id.

Validación de Dimensión: Comprueba si la dimensión del operador coincide con la longitud del vector del estado antes de la aplicación, lo que evita errores comunes.

Clase RepositorioDeEstados
Estructura Interna: Utiliza un diccionario _estados (Dict[str, EstadoCuantico]) para el almacenamiento y la recuperación eficientes de estados por su ID único. Esto gestiona de forma natural el requisito de unicidad.

listar_estados(): Devuelve una lista de representaciones de cadena de todos los estados almacenados, lo que facilita su visualización.

agregar_estado(): Valida si hay ID duplicados antes de agregar un nuevo estado. Convierte el vector de entrada (que puede contener números de coma flotante) en números complejos antes de crear el objeto EstadoCuantico.

obtener_estado(): Proporciona acceso seguro a los objetos EstadoCuantico por ID, devolviendo None si no se encuentran.

aplicar_operador(): Orquesta la aplicación de operadores. Recupera el estado objetivo, llama al método OperadorCuantico.aplicar() y almacena el nuevo estado resultante en el repositorio. Ofrece flexibilidad para nuevo_id.

medir_estado(): Recupera un estado por ID y llama a su método medir(); luego, formatea e imprime las probabilidades de forma intuitiva.

Persistencia (guardar y cargar):

Formato JSON: Se elige por su legibilidad y facilidad para manejar datos estructurados como listas de números complejos.

Manejo de números complejos: Dado que JSON no admite números complejos de forma nativa, el vector complejo [a + bi, c + di] se serializa en [[a, b], [c, d]] (lista de listas de partes reales/imaginarias) antes de guardarse y se reconstruye al cargar. Esta es una solución alternativa común.

Manejo de errores: Incluye bloques try-except para IOError, json.JSONDecodeError y KeyError para manejar problemas comunes de archivos y análisis.

Comportamiento de cargar(): Borra los estados existentes antes de cargar los nuevos desde el archivo para garantizar un estado actualizado mediante persistencia, evitando fusiones accidentales o duplicados, a menos que se desee explícitamente lo contrario para una estrategia de fusión más compleja.

main.py
Proporciona una interfaz de línea de comandos sencilla para la interacción del usuario.

Predefine operadores cuánticos comunes (X, H, Z) para facilitar las pruebas.

Incluye la función obtener_vector_complejo_del_usuario() para guiar al usuario en la introducción de números complejos y gestionar posibles errores ValueError durante la conversión.

Intenta cargar datos desde estados.json al inicio para una persistencia básica entre sesiones.

Pruebas unitarias (tests/test_quantum_simulator.py)
Utiliza el framework unittest estándar.

Casos de prueba: Abarca todas las funcionalidades principales:

EstadoCuantico: Creación, normalización, mediciones básicas y de superposición, representación de cadenas y gestión de errores para vectores vacíos.

Operador Cuántico: Creación, aplicación de puertas X y H (incluida la aplicación de doble H para restablecer el estado original) y errores de desajuste de dimensiones.

Repositorio de Estados: Listado de repositorios vacíos y llenos, adición de estados (incluida la comprobación de duplicados), recuperación de estados, aplicación de operadores (con y sin nuevo_id), medición de estados y pruebas de persistencia exhaustivas (guardado, carga y gestión de inexistentes).
