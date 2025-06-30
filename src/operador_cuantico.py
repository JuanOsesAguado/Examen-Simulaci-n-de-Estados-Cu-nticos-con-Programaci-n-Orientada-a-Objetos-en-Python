import cmath
from typing import List
from src.estado_cuantico import EstadoCuantico

class OperadorCuantico:
    """
    Modela un operador lineal cuántico (por ejemplo, una puerta lógica).

    Atributos:
        nombre (str): Identificador o etiqueta del operador (ej. "Hadamard", "X").
        matriz (List[List[complex]]): La matriz unitaria que implementa la transformación.
    """

    def __init__(self, nombre: str, matriz: List[List[complex]]):
        if not matriz or not all(matriz[i] for i in range(len(matriz))):
            raise ValueError("La matriz del operador no puede estar vacía.")
        num_rows = len(matriz)
        num_cols = len(matriz[0])
        if num_rows != num_cols:
            raise ValueError("La matriz del operador debe ser cuadrada.")
        self._nombre = nombre
        self._matriz = [[complex(val) for val in row] for row in matriz]
        self._dim = num_rows # Dimensión del operador

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def matriz(self) -> List[List[complex]]:
        return self._matriz

    @property
    def dim(self) -> int:
        return self._dim

    def aplicar(self, estado: EstadoCuantico) -> EstadoCuantico:
        """
        Aplica la transformación lineal del operador a un estado cuántico.
        Devuelve un nuevo objeto EstadoCuantico con el estado transformado.

        Args:
            estado (EstadoCuantico): El estado cuántico al que se aplicará el operador.

        Retorna:
            EstadoCuantico: Un nuevo estado cuántico transformado.

        Excepciones:
            ValueError: Si la dimensión del operador no coincide con la del estado.
        """
        if self.dim != len(estado.vector):
            raise ValueError(
                f"La dimensión del operador ({self.dim}) no coincide "
                f"con la dimensión del estado ({len(estado.vector)})."
            )

        nuevo_vector: List[complex] = []
        for i in range(self.dim):
            new_amplitude = sum(self._matriz[i][j] * estado.vector[j] for j in range(self.dim))
            nuevo_vector.append(new_amplitude)

        # Generar un nuevo ID para el estado transformado
        nuevo_id = f"{estado.id}_{self.nombre}"
        return EstadoCuantico(nuevo_id, nuevo_vector, estado.base)