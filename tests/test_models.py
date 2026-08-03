import os
import sys
import tempfile
import unittest
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import src.database
from src.database import (
    DESTINOS_SEED, RESTAURANTES_SEED, TIENDAS_SEED,
    TRANSPORTES_SEED, HOSPEDAJES_SEED,
    seed_destinos, seed_restaurantes, seed_tiendas,
    seed_transportes, seed_hospedajes,
)
from src.models.ciudadano import Ciudadano
from src.models.presupuesto import Presupuesto
from src.models.ahorro import Ahorro
from src.models.historial import Historial
from src.models.recomendacion import Recomendacion
from src.models.destino import Destino
from src.models.restaurante import Restaurante
from src.models.tienda import Tienda
from src.models.transporte import Transporte
from src.models.hospedaje import Hospedaje
from src.models.exportador import Exportador


class TestWithDB(unittest.TestCase):
    """Base class: creates a temporary DB with all tables + seeds."""

    @classmethod
    def setUpClass(cls):
        cls._original_get_connection = src.database.get_connection

    @classmethod
    def tearDownClass(cls):
        src.database.get_connection = cls._original_get_connection

    def setUp(self):
        self._db_fd, self._db_path = tempfile.mkstemp(suffix=".db")
        src.database.DB_PATH = self._db_path
        from src.database import init_db
        init_db()

    def tearDown(self):
        os.close(self._db_fd)
        os.unlink(self._db_path)

    _email_counter = 0

    def _crear_ciudadano(self, nombre="Test", email=None, telefono="999888777", contrasena="pass123"):
        TestWithDB._email_counter += 1
        if email is None:
            email = f"test{TestWithDB._email_counter}@test.com"
        c = Ciudadano(nombre, email, telefono, contrasena)
        ok, msg = c.guardar()
        self.assertTrue(ok, msg)
        return {"id_ciudadano": c.id_ciudadano, "nombre": nombre, "email": email}


# ── CIUDADANO ──────────────────────────────────────────────────────────

class TestCiudadano(TestWithDB):

    def test_guardar_y_crear_id(self):
        c = Ciudadano("Juan", "juan@mail.com", "999111222", "clave123")
        ok, msg = c.guardar()
        self.assertTrue(ok, msg)
        self.assertIsNotNone(c.id_ciudadano)

    def test_email_duplicado(self):
        Ciudadano("A", "dup@mail.com", "111", "xxx").guardar()
        c2 = Ciudadano("B", "dup@mail.com", "222", "yyy")
        ok, msg = c2.guardar()
        self.assertFalse(ok)
        self.assertIn("ya está registrado", msg)

    def test_iniciar_sesion_ok(self):
        uniq = f"login{TestWithDB._email_counter}@ok.com"
        self._crear_ciudadano(email=uniq, contrasena="miclave")
        ok, data = Ciudadano.iniciar_sesion(uniq, "miclave")
        self.assertTrue(ok)
        self.assertEqual(data["email"], uniq)

    def test_iniciar_sesion_fail(self):
        ok, msg = Ciudadano.iniciar_sesion("noexiste@x.com", "x")
        self.assertFalse(ok)

    def test_actualizar_perfil(self):
        c = self._crear_ciudadano()
        ok, msg = Ciudadano.actualizar(c["id_ciudadano"], "NuevoNombre", "nuevo@mail.com", "777")
        self.assertTrue(ok)
        ok2, data = Ciudadano.iniciar_sesion("nuevo@mail.com", "pass123")
        self.assertTrue(ok2)
        self.assertEqual(data["nombre"], "NuevoNombre")

    def test_actualizar_con_contrasena(self):
        c = self._crear_ciudadano()
        Ciudadano.actualizar(c["id_ciudadano"], "X", "x@x.com", "777", "nuevaclave")
        ok, data = Ciudadano.iniciar_sesion("x@x.com", "nuevaclave")
        self.assertTrue(ok)

    def test_validar_email(self):
        self.assertTrue(Ciudadano.validar_email("a@b.com"))
        self.assertFalse(Ciudadano.validar_email("invalido"))

    def test_validar_telefono(self):
        self.assertTrue(Ciudadano.validar_telefono("999888777"))
        self.assertTrue(Ciudadano.validar_telefono("+51999888777"))
        self.assertFalse(Ciudadano.validar_telefono("abc"))

    def test_validar_contrasena(self):
        self.assertTrue(Ciudadano.validar_contrasena("123456"))
        self.assertFalse(Ciudadano.validar_contrasena("12345"))


# ── PRESUPUESTO ────────────────────────────────────────────────────────

class TestPresupuesto(TestWithDB):

    def test_guardar_y_gasto_diario(self):
        c = self._crear_ciudadano()
        p = Presupuesto(c["id_ciudadano"], 1000, 5, "Ayacucho", "2026-07-01")
        ok, msg = p.guardar()
        self.assertTrue(ok)
        self.assertEqual(p.gasto_diario(), 200.0)

    def test_desglose(self):
        p = Presupuesto(1, 1000, 5)
        d = p.desglose()
        self.assertAlmostEqual(d["alojamiento"], 80.0)
        self.assertAlmostEqual(d["comida"], 60.0)
        self.assertAlmostEqual(d["transporte"], 40.0)
        self.assertAlmostEqual(d["extras"], 20.0)

    def test_obtener_por_ciudadano(self):
        c = self._crear_ciudadano()
        Presupuesto(c["id_ciudadano"], 500, 2).guardar()
        Presupuesto(c["id_ciudadano"], 1000, 3).guardar()
        pres = Presupuesto.obtener_por_ciudadano(c["id_ciudadano"])
        self.assertEqual(len(pres), 2)
        totales = [p["total"] for p in pres]
        self.assertIn(500, totales)
        self.assertIn(1000, totales)

    def test_obtener_por_ciudadano_vacio(self):
        c = self._crear_ciudadano()
        pres = Presupuesto.obtener_por_ciudadano(c["id_ciudadano"])
        self.assertEqual(len(pres), 0)

    def test_calcular_integrado(self):
        c = self._crear_ciudadano()
        dest = Destino.listar_todos()
        rest = Restaurante.listar_todos()
        trans = Transporte.listar_todos()
        hosp = Hospedaje.listar_todos()
        r = Presupuesto.calcular_integrado(500, 3, dest[0]["id_destino"], rest[0]["id_restaurante"], trans[0]["id_transporte"], hosp[0]["id_hospedaje"])
        self.assertIsNotNone(r)
        self.assertIn("destino", r)
        self.assertIn("costo_total", r)
        self.assertIn("dentro_presupuesto", r)

    def test_calcular_integrado_sin_datos(self):
        r = Presupuesto.calcular_integrado(500, 3, 9999, 9999, 9999, 9999)
        self.assertIsNone(r)


# ── AHORRO ─────────────────────────────────────────────────────────────

class TestAhorro(TestWithDB):

    def test_agregar_y_listar(self):
        c = self._crear_ciudadano()
        ok, msg = Ahorro.agregar(c["id_ciudadano"], "Viaje a Ayacucho", 2000.0, "2026-12-31")
        self.assertTrue(ok)
        metas = Ahorro.listar_por_ciudadano(c["id_ciudadano"])
        self.assertEqual(len(metas), 1)
        self.assertEqual(metas[0]["meta"], "Viaje a Ayacucho")

    def test_listar_activos(self):
        c = self._crear_ciudadano()
        Ahorro.agregar(c["id_ciudadano"], "Meta1", 100, None)
        Ahorro.agregar(c["id_ciudadano"], "Meta2", 200, None)
        activas = Ahorro.listar_activos(c["id_ciudadano"])
        self.assertEqual(len(activas), 2)

    def test_aportar(self):
        c = self._crear_ciudadano()
        Ahorro.agregar(c["id_ciudadano"], "Ahorro test", 500, None)
        metas = Ahorro.listar_por_ciudadano(c["id_ciudadano"])
        id_a = metas[0]["id_ahorro"]
        ok, msg = Ahorro.aportar(id_a, 200)
        self.assertTrue(ok)
        meta = Ahorro.obtener(id_a)
        self.assertEqual(meta["monto_actual"], 200)
        self.assertEqual(meta["estado"], "En progreso")

    def test_aportar_completa(self):
        c = self._crear_ciudadano()
        Ahorro.agregar(c["id_ciudadano"], "Meta corta", 100, None)
        metas = Ahorro.listar_por_ciudadano(c["id_ciudadano"])
        id_a = metas[0]["id_ahorro"]
        Ahorro.aportar(id_a, 100)
        meta = Ahorro.obtener(id_a)
        self.assertEqual(meta["estado"], "Completada")

    def test_actualizar_meta(self):
        c = self._crear_ciudadano()
        Ahorro.agregar(c["id_ciudadano"], "Original", 500, None)
        metas = Ahorro.listar_por_ciudadano(c["id_ciudadano"])
        id_a = metas[0]["id_ahorro"]
        ok, msg = Ahorro.actualizar(id_a, "Actualizada", 1000, "2026-06-01")
        self.assertTrue(ok)
        meta = Ahorro.obtener(id_a)
        self.assertEqual(meta["meta"], "Actualizada")
        self.assertEqual(meta["monto_objetivo"], 1000)

    def test_eliminar_meta(self):
        c = self._crear_ciudadano()
        Ahorro.agregar(c["id_ciudadano"], "A eliminar", 100, None)
        metas = Ahorro.listar_por_ciudadano(c["id_ciudadano"])
        id_a = metas[0]["id_ahorro"]
        ok, msg = Ahorro.eliminar(id_a)
        self.assertTrue(ok)
        self.assertIsNone(Ahorro.obtener(id_a))


# ── HISTORIAL ──────────────────────────────────────────────────────────

class TestHistorial(TestWithDB):

    def test_registrar_y_obtener(self):
        c = self._crear_ciudadano()
        Historial.registrar(c["id_ciudadano"], "Test", "Prueba unitaria")
        registros = Historial.obtener_por_ciudadano(c["id_ciudadano"])
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["descripcion"], "Prueba unitaria")

    def test_filtrar_por_tipo(self):
        c = self._crear_ciudadano()
        Historial.registrar(c["id_ciudadano"], "A", "Act A")
        Historial.registrar(c["id_ciudadano"], "B", "Act B")
        Historial.registrar(c["id_ciudadano"], "A", "Act A2")
        a_acts = Historial.obtener_por_ciudadano(c["id_ciudadano"], tipo="A")
        self.assertEqual(len(a_acts), 2)

    def test_tipos_actividad(self):
        c = self._crear_ciudadano()
        Historial.registrar(c["id_ciudadano"], "X", "xx")
        Historial.registrar(c["id_ciudadano"], "Y", "yy")
        tipos = Historial.tipos_actividad()
        self.assertIn("X", tipos)
        self.assertIn("Y", tipos)


# ── RECOMENDACION ──────────────────────────────────────────────────────

class TestRecomendacion(TestWithDB):

    def test_recomendar_dentro_presupuesto(self):
        destinos = Recomendacion.obtener_destinos(precio_max=100)
        self.assertGreater(len(destinos), 0)
        for d in destinos:
            self.assertLessEqual(d["precio"], 100)

    def test_recomendar_por_provincia(self):
        destinos = Recomendacion.obtener_destinos(provincia="Huamanga")
        for d in destinos:
            self.assertEqual(d["provincia"], "Huamanga")

    def test_recomendar_por_categoria(self):
        destinos = Recomendacion.obtener_destinos(categoria="Cultural")
        for d in destinos:
            self.assertEqual(d["categoria"], "Cultural")

    def test_recomendar_metodo(self):
        rec = Recomendacion(200, 2)
        destinos = rec.recomendar()
        self.assertIsInstance(destinos, list)

    def test_resumen_recomendacion(self):
        rec = Recomendacion(500, 3)
        res = rec.resumen_recomendacion("Huamanga")
        self.assertIn("destinos", res)
        self.assertIn("total", res)
        self.assertIn("dentro_presupuesto", res)
        self.assertIn("categoria_distribucion", res)

    def test_obtener_por_provincia(self):
        destinos = Recomendacion.obtener_por_provincia("Huanta")
        self.assertGreater(len(destinos), 0)
        for d in destinos:
            self.assertEqual(d["provincia"], "Huanta")


# ── DESTINO ────────────────────────────────────────────────────────────

class TestDestino(TestWithDB):

    def test_listar_todos(self):
        dests = Destino.listar_todos()
        self.assertGreaterEqual(len(dests), len(DESTINOS_SEED))

    def test_obtener(self):
        dests = Destino.listar_todos()
        d = Destino.obtener(dests[0]["id_destino"])
        self.assertIsNotNone(d)
        self.assertEqual(d["nombre"], dests[0]["nombre"])

    def test_listar_por_provincia(self):
        dests = Destino.listar_por_provincia("Huamanga")
        self.assertGreater(len(dests), 0)
        for d in dests:
            self.assertEqual(d["provincia"], "Huamanga")

    def test_listar_por_categoria(self):
        dests = Destino.listar_por_categoria("Natural")
        self.assertGreater(len(dests), 0)
        for d in dests:
            self.assertEqual(d["categoria"], "Natural")

    def test_agregar_destino(self):
        ok, msg = Destino.agregar("Huamanga", "Cultural", "Nuevo Destino", 50, "Desc")
        self.assertTrue(ok)
        dests = Destino.listar_todos()
        self.assertGreaterEqual(len(dests), len(DESTINOS_SEED) + 1)

    def test_actualizar_destino(self):
        dests = Destino.listar_todos()
        id_d = dests[0]["id_destino"]
        ok, msg = Destino.actualizar(id_d, "Huanta", "Natural", "Actualizado", 99, "Nueva desc")
        self.assertTrue(ok)
        d = Destino.obtener(id_d)
        self.assertEqual(d["nombre"], "Actualizado")
        self.assertEqual(d["precio"], 99)

    def test_eliminar_destino(self):
        Destino.agregar("Huamanga", "Natural", "Temp", 10, "x")
        dests = Destino.listar_todos()
        id_d = dests[-1]["id_destino"]
        ok, msg = Destino.eliminar(id_d)
        self.assertTrue(ok)
        self.assertIsNone(Destino.obtener(id_d))

    def test_categorias_constantes(self):
        self.assertIn("Cultural", Destino.CATEGORIAS)
        self.assertIn("Huamanga", Destino.PROVINCIAS)


# ── RESTAURANTE ────────────────────────────────────────────────────────

class TestRestaurante(TestWithDB):

    def test_listar_todos(self):
        rs = Restaurante.listar_todos()
        self.assertGreaterEqual(len(rs), len(RESTAURANTES_SEED))

    def test_obtener(self):
        rs = Restaurante.listar_todos()
        r = Restaurante.obtener(rs[0]["id_restaurante"])
        self.assertIsNotNone(r)

    def test_listar_por_provincia(self):
        rs = Restaurante.listar_por_provincia("Huamanga")
        self.assertGreater(len(rs), 0)
        for r in rs:
            self.assertEqual(r["provincia"], "Huamanga")

    def test_listar_por_tipo(self):
        rs = Restaurante.listar_por_tipo("Local")
        self.assertGreater(len(rs), 0)

    def test_provincias(self):
        provs = Restaurante.provincias()
        self.assertIn("Huamanga", provs)

    def test_tipos_comida(self):
        tipos = Restaurante.tipos_comida()
        self.assertIn("Local", tipos)

    def test_crud(self):
        ok, msg = Restaurante.agregar("Huanta", "Gourmet", "TestRest", 10, 50, "Plato")
        self.assertTrue(ok)
        rs = Restaurante.listar_todos()
        self.assertGreaterEqual(len(rs), len(RESTAURANTES_SEED) + 1)
        id_r = rs[-1]["id_restaurante"]
        Restaurante.actualizar(id_r, "Huanta", "Local", "TestRest2", 15, 55, "Plato2")
        r = Restaurante.obtener(id_r)
        self.assertEqual(r["nombre"], "TestRest2")
        Restaurante.eliminar(id_r)
        self.assertIsNone(Restaurante.obtener(id_r))


# ── TIENDA ─────────────────────────────────────────────────────────────

class TestTienda(TestWithDB):

    def test_listar_todos(self):
        ts = Tienda.listar_todos()
        self.assertGreaterEqual(len(ts), len(TIENDAS_SEED))

    def test_filtros(self):
        ts = Tienda.listar_por_provincia("Huamanga")
        self.assertGreater(len(ts), 0)
        ts2 = Tienda.listar_por_tipo("Artesanía")
        self.assertGreater(len(ts2), 0)

    def test_auxiliares(self):
        self.assertIn("Huamanga", Tienda.provincias())
        self.assertIn("Artesanía", Tienda.tipos())

    def test_crud(self):
        ok, msg = Tienda.agregar("Huanta", "Ropa", "TestTienda", 5, 30, "Ropa tipica")
        self.assertTrue(ok)
        ts = Tienda.listar_todos()
        self.assertGreaterEqual(len(ts), len(TIENDAS_SEED) + 1)
        id_t = ts[-1]["id_tienda"]
        Tienda.actualizar(id_t, "Huanta", "Calzado", "TestT2", 10, 40, "Zapatos")
        t = Tienda.obtener(id_t)
        self.assertEqual(t["tipo"], "Calzado")
        Tienda.eliminar(id_t)
        self.assertIsNone(Tienda.obtener(id_t))


# ── TRANSPORTE ─────────────────────────────────────────────────────────

class TestTransporte(TestWithDB):

    def test_listar_todos(self):
        ts = Transporte.listar_todos()
        self.assertGreaterEqual(len(ts), len(TRANSPORTES_SEED))

    def test_filtros(self):
        ts = Transporte.listar_por_tipo("Bus")
        self.assertGreater(len(ts), 0)
        ts2 = Transporte.listar_por_origen("Lima")
        self.assertGreater(len(ts2), 0)
        ts3 = Transporte.listar_por_destino("Ayacucho")
        self.assertGreater(len(ts3), 0)

    def test_auxiliares(self):
        self.assertIn("Bus", Transporte.tipos())
        self.assertIn("Transportes Molina", Transporte.empresas())
        self.assertIn("Ayacucho", Transporte.destinos())

    def test_crud(self):
        ok, msg = Transporte.agregar("Bus", "TestEmp", "TestBus", "Lima", "Ica", 50, "2h")
        self.assertTrue(ok)
        ts = Transporte.listar_todos()
        self.assertGreaterEqual(len(ts), len(TRANSPORTES_SEED) + 1)
        id_t = ts[-1]["id_transporte"]
        Transporte.actualizar(id_t, "Avión", "TestEmp2", "AeroExpreso", "Lima", "Cusco", 200, "1h")
        t = Transporte.obtener(id_t)
        self.assertEqual(t["tipo"], "Avión")
        Transporte.eliminar(id_t)
        self.assertIsNone(Transporte.obtener(id_t))


# ── HOSPEDAJE ──────────────────────────────────────────────────────────

class TestHospedaje(TestWithDB):

    def test_listar_todos(self):
        hs = Hospedaje.listar_todos()
        self.assertGreaterEqual(len(hs), len(HOSPEDAJES_SEED))

    def test_filtros(self):
        hs = Hospedaje.listar_por_provincia("Huamanga")
        self.assertGreater(len(hs), 0)
        hs2 = Hospedaje.listar_por_tipo("Hotel")
        self.assertGreater(len(hs2), 0)

    def test_auxiliares(self):
        self.assertIn("Huamanga", Hospedaje.provincias())
        self.assertIn("Hotel", Hospedaje.tipos())

    def test_crud(self):
        ok, msg = Hospedaje.agregar("Huanta", "Hostal", "TestHosp", 20, 50, "WiFi", "123")
        self.assertTrue(ok)
        hs = Hospedaje.listar_todos()
        self.assertGreaterEqual(len(hs), len(HOSPEDAJES_SEED) + 1)
        id_h = hs[-1]["id_hospedaje"]
        Hospedaje.actualizar(id_h, "Huanta", "Hotel", "TestH2", 30, 60, "WiFi, TV", "456")
        h = Hospedaje.obtener(id_h)
        self.assertEqual(h["tipo"], "Hotel")
        Hospedaje.eliminar(id_h)
        self.assertIsNone(Hospedaje.obtener(id_h))


# ── EXPORTADOR ────────────────────────────────────────────────────────

class TestExportador(TestWithDB):

    def setUp(self):
        super().setUp()
        self.c = self._crear_ciudadano()
        Historial.registrar(self.c["id_ciudadano"], "Test", "Evento de prueba")
        Presupuesto(self.c["id_ciudadano"], 1000, 5, "Ayacucho", "2026-07-01").guardar()
        Ahorro.agregar(self.c["id_ciudadano"], "Meta test", 500, None)

    def test_exportar_historial_csv(self):
        ruta = os.path.join(tempfile.gettempdir(), "test_historial.csv")
        ok, msg = Exportador.exportar_historial_csv(self.c["id_ciudadano"], ruta)
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(ruta))
        with open(ruta, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Evento de prueba", content)
        os.unlink(ruta)

    def test_exportar_presupuestos_csv(self):
        ruta = os.path.join(tempfile.gettempdir(), "test_presupuestos.csv")
        ok, msg = Exportador.exportar_presupuestos_csv(self.c["id_ciudadano"], ruta)
        self.assertTrue(ok)
        with open(ruta, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Ayacucho", content)
        os.unlink(ruta)

    def test_exportar_ahorros_csv(self):
        ruta = os.path.join(tempfile.gettempdir(), "test_ahorros.csv")
        ok, msg = Exportador.exportar_ahorros_csv(self.c["id_ciudadano"], ruta)
        self.assertTrue(ok)
        with open(ruta, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Meta test", content)
        os.unlink(ruta)

    def test_exportar_reporte_txt(self):
        ruta = os.path.join(tempfile.gettempdir(), "test_reporte.txt")
        ok, msg = Exportador.exportar_reporte_txt(self.c["id_ciudadano"], ruta, self.c["nombre"])
        self.assertTrue(ok)
        with open(ruta, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("DESCUBRE AYACUCHO", content)
        self.assertIn("Evento de prueba", content)
        self.assertIn("Ayacucho", content)
        self.assertIn("Meta test", content)
        os.unlink(ruta)


if __name__ == "__main__":
    unittest.main()
