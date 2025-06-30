import unittest
import os
import cmath
import json
from src.estado_cuantico import EstadoCuantico
from src.operador_cuantico import OperadorCuantico
from src.repositorio_estados import RepositorioDeEstados

class TestEstadoCuantico(unittest.TestCase):
    def test_creacion_estado_valido(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        self.assertEqual(estado.id, "q0")
        self.assertEqual(estado.vector, [complex(1), complex(0)])
        self.assertEqual(estado.base, "computacional")

    def test_normalizacion(self):
        # Estado no normalizado, debería normalizarse a |+>
        estado = EstadoCuantico("q_norm", [1, 1], "computacional")
        sqrt2_inv = 1 / cmath.sqrt(2)
        self.assertAlmostEqual(abs(estado.vector[0]), sqrt2_inv)
        self.assertAlmostEqual(abs(estado.vector[1]), sqrt2_inv)
        self.assertAlmostEqual(sum(abs(amp)**2 for amp in estado.vector), 1.0)

    def test_medicion_estado_base(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        probs = estado.medir()
        self.assertAlmostEqual(probs['0'], 1.0)
        self.assertAlmostEqual(probs['1'], 0.0)

        estado_one = EstadoCuantico("q1", [0, 1], "computacional")
        probs_one = estado_one.medir()
        self.assertAlmostEqual(probs_one['0'], 0.0)
        self.assertAlmostEqual(probs_one['1'], 1.0)

    def test_medicion_superposicion(self):
        sqrt2_inv = 1 / cmath.sqrt(2)
        estado_plus = EstadoCuantico("q+", [sqrt2_inv, sqrt2_inv], "computacional")
        probs = estado_plus.medir()
        self.assertAlmostEqual(probs['0'], 0.5)
        self.assertAlmostEqual(probs['1'], 0.5)

    def test_str_representation(self):
        estado = EstadoCuantico("q_test", [1+0j, 0+0j], "computacional")
        expected_str = "q_test: vector=[(1+0j), 0j] en base computacional"
        self.assertEqual(str(estado), expected_str)

    def test_vector_vacio_raises_error(self):
        with self.assertRaises(ValueError):
            EstadoCuantico("q_empty", [], "computacional")

class TestOperadorCuantico(unittest.TestCase):
    def setUp(self):
        # Puerta X (NOT)
        self.op_x = OperadorCuantico("X", [[0, 1], [1, 0]])
        # Puerta Hadamard
        self.sqrt2_inv = 1 / cmath.sqrt(2)
        self.op_h = OperadorCuantico("H", [[self.sqrt2_inv, self.sqrt2_inv], [self.sqrt2_inv, -self.sqrt2_inv]])
        # Estado |0>
        self.estado_0 = EstadoCuantico("q0", [1, 0], "computacional")
        # Estado |1>
        self.estado_1 = EstadoCuantico("q1", [0, 1], "computacional")

    def test_creacion_operador_valido(self):
        self.assertEqual(self.op_x.nombre, "X")
        self.assertEqual(self.op_x.matriz, [[complex(0), complex(1)], [complex(1), complex(0)]])
        self.assertEqual(self.op_x.dim, 2)
        
    def test_matriz_no_cuadrada_raises_error(self):
        with self.assertRaises(ValueError):
            OperadorCuantico("Invalid", [[1, 2, 3], [4, 5, 6]])

    def test_aplicar_x_a_0(self):
        nuevo_estado = self.op_x.aplicar(self.estado_0)
        self.assertEqual(nuevo_estado.id, "q0_X")
        self.assertAlmostEqual(nuevo_estado.vector[0], complex(0))
        self.assertAlmostEqual(nuevo_estado.vector[1], complex(1))

    def test_aplicar_x_a_1(self):
        nuevo_estado = self.op_x.aplicar(self.estado_1)
        self.assertEqual(nuevo_estado.id, "q1_X")
        self.assertAlmostEqual(nuevo_estado.vector[0], complex(1))
        self.assertAlmostEqual(nuevo_estado.vector[1], complex(0))

    def test_aplicar_h_a_0(self):
        nuevo_estado = self.op_h.aplicar(self.estado_0)
        self.assertEqual(nuevo_estado.id, "q0_H")
        self.assertAlmostEqual(nuevo_estado.vector[0], self.sqrt2_inv)
        self.assertAlmostEqual(nuevo_estado.vector[1], self.sqrt2_inv)

    def test_aplicar_h_dos_veces_a_0(self):
        estado_plus = self.op_h.aplicar(self.estado_0)
        estado_back_to_0 = self.op_h.aplicar(estado_plus)
        self.assertEqual(estado_back_to_0.id, "q0_H_H") # Verifica el id compuesto
        self.assertAlmostEqual(estado_back_to_0.vector[0], complex(1))
        self.assertAlmostEqual(estado_back_to_0.vector[1], complex(0))

    def test_aplicar_operador_dimension_invalida(self):
        estado_3d = EstadoCuantico("q_3d", [1, 0, 0], "computacional")
        with self.assertRaises(ValueError):
            self.op_x.aplicar(estado_3d)

class TestRepositorioDeEstados(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioDeEstados()
        self.temp_file = "test_estados.json"
        # Operadores para pruebas
        self.op_x = OperadorCuantico("X", [[0, 1], [1, 0]])
        self.sqrt2_inv = 1 / cmath.sqrt(2)
        self.op_h = OperadorCuantico("H", [[self.sqrt2_inv, self.sqrt2_inv], [self.sqrt2_inv, -self.sqrt2_inv]])

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_listar_estados_vacio(self):
        self.assertEqual(self.repo.listar_estados(), ["No hay estados cuánticos registrados."])

    def test_agregar_estado(self):
        self.assertTrue(self.repo.agregar_estado("q0", [1, 0], "computacional"))
        self.assertIn("q0: vector=[(1+0j), 0j] en base computacional", self.repo.listar_estados())
        self.assertEqual(len(self.repo._estados), 1)

    def test_agregar_estado_duplicado(self):
        self.repo.agregar_estado("q0", [1, 0], "computacional")
        self.assertFalse(self.repo.agregar_estado("q0", [0, 1], "computacional"))
        self.assertEqual(len(self.repo._estados), 1) # Asegura que no se añadió el duplicado

    def test_obtener_estado(self):
        self.repo.agregar_estado("q0", [1, 0], "computacional")
        estado = self.repo.obtener_estado("q0")
        self.assertIsNotNone(estado)
        self.assertEqual(estado.id, "q0")

    def test_obtener_estado_no_existente(self):
        estado = self.repo.obtener_estado("q_fake")
        self.assertIsNone(estado)

    def test_aplicar_operador_nuevo_id(self):
        self.repo.agregar_estado("q_initial", [1, 0], "computacional")
        self.assertTrue(self.repo.aplicar_operador("q_initial", self.op_x, "q_final"))
        final_state = self.repo.obtener_estado("q_final")
        self.assertIsNotNone(final_state)
        self.assertAlmostEqual(final_state.vector[0], complex(0))
        self.assertAlmostEqual(final_state.vector[1], complex(1))
        self.assertIsNotNone(self.repo.obtener_estado("q_initial")) # Original should still exist

    def test_aplicar_operador_auto_id(self):
        self.repo.agregar_estado("q0", [1, 0], "computacional")
        self.assertTrue(self.repo.aplicar_operador("q0", self.op_h))
        hadamard_state = self.repo.obtener_estado("q0_H")
        self.assertIsNotNone(hadamard_state)
        self.assertAlmostEqual(hadamard_state.vector[0], self.sqrt2_inv)
        self.assertAlmostEqual(hadamard_state.vector[1], self.sqrt2_inv)

    def test_aplicar_operador_estado_no_existe(self):
        self.assertFalse(self.repo.aplicar_operador("q_nonexistent", self.op_x))

    def test_medir_estado_existente(self):
        estado_plus_id = "q_plus_test"
        self.repo.agregar_estado(estado_plus_id, [self.sqrt2_inv, self.sqrt2_inv], "computacional")
        # Captura la salida de print para verificar
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            self.assertTrue(self.repo.medir_estado(estado_plus_id))
        output = f.getvalue()
        self.assertIn("Medición del estado 'q_plus_test' (base computacional):", output)
        self.assertIn("  - Estado base |0⟩: 0.5000 (50.00%)", output)
        self.assertIn("  - Estado base |1⟩: 0.5000 (50.00%)", output)

    def test_medir_estado_no_existente(self):
        self.assertFalse(self.repo.medir_estado("q_nonexistent"))

    def test_persistencia_guardar_cargar(self):
        self.repo.agregar_estado("q0", [1, 0], "computacional")
        self.repo.agregar_estado("q1", [0, 1], "computacional")
        
        self.assertTrue(self.repo.guardar(self.temp_file))
        self.assertTrue(os.path.exists(self.temp_file))

        # Crear un nuevo repositorio para simular una nueva sesión
        new_repo = RepositorioDeEstados()
        self.assertTrue(new_repo.cargar(self.temp_file))
        
        self.assertEqual(len(new_repo._estados), 2)
        self.assertIsNotNone(new_repo.obtener_estado("q0"))
        self.assertIsNotNone(new_repo.obtener_estado("q1"))
        self.assertEqual(new_repo.obtener_estado("q0").vector, [complex(1), complex(0)])

    def test_cargar_archivo_no_existente(self):
        new_repo = RepositorioDeEstados()
        self.assertFalse(new_repo.cargar("non_existent_file.json"))

    def test_guardar_complejos_y_cargar(self):
        complex_state_vector = [complex(0.6, 0.8), complex(0.8, -0.6)] # Not normalized, but for complex test
        self.repo.agregar_estado("q_complex", complex_state_vector, "computacional")
        
        self.assertTrue(self.repo.guardar(self.temp_file))
        
        new_repo = RepositorioDeEstados()
        self.assertTrue(new_repo.cargar(self.temp_file))
        
        loaded_state = new_repo.obtener_estado("q_complex")
        self.assertIsNotNone(loaded_state)
        # Check if real and imaginary parts are preserved
        self.assertAlmostEqual(loaded_state.vector[0].real, complex(0.6, 0.8).real)
        self.assertAlmostEqual(loaded_state.vector[0].imag, complex(0.6, 0.8).imag)
        self.assertAlmostEqual(loaded_state.vector[1].real, complex(0.8, -0.6).real)
        self.assertAlmostEqual(loaded_state.vector[1].imag, complex(0.8, -0.6).imag)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)