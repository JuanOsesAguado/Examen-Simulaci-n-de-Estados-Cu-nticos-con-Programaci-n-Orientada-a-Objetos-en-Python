import cmath
from typing import List, Dict

class EstadoCuantico:
    """
    Representa un estado cuántico individual.

    Atributos:
        id (str): Identificador único del estado.
        vector (List[complex]): Vector de amplitudes del estado.
        base (str): Base en la que está expresado el vector (ej. "computacional").
    """

    def __init__(self, id: str, vector: List[complex], base: str):
        if not vector:
            raise ValueError("El vector de estado no puede estar vacío.")
        self._id = id
        # Asegurarse de que todas las componentes son complejas
        self._vector = [complex(amp) for amp in vector]
        self._base = base
        self._normalizar_vector()

    @property
    def id(self) -> str:
        return self._id

    @property
    def vector(self) -> List[complex]:
        return self._vector

    @property
    def base(self) -> str:
        return self._base

    def _normalizar_vector(self, tolerance: float = 1e-9):
        """Normaliza el vector de estado para que la suma de los módulos al cuadrado sea 1."""
        norm_squared = sum(abs(amp)**2 for amp in self._vector)
        if abs(norm_squared - 1.0) > tolerance:
            norm = cmath.sqrt(norm_squared)
            self._vector = [amp / norm for amp in self._vector]

    def medir(self) -> Dict[str, float]:
        """
        Calcula las probabilidades de obtener cada estado base al medir.
        No modifica el estado original.

        Retorna:
            Dict[str, float]: Un diccionario mapeando el índice del estado base
                              (como string) a su probabilidad.
        """
        probabilities = {}
        for i, amplitude in enumerate(self._vector):
            # La probabilidad es el cuadrado del módulo de la amplitud
            prob = abs(amplitude)**2
            probabilities[str(i)] = prob
        return probabilities

    def __str__(self) -> str:
        """
        Retorna una representación legible del estado cuántico.
        """
        return f"{self.id}: vector={self.vector} en base {self.base}"

    def __repr__(self) -> str:
        """
        Retorna una representación oficial del estado cuántico.
        """
        return f"EstadoCuantico(id='{self.id}', vector={self.vector}, base='{self.base}')"