import csv
import os
from datetime import datetime
from src.database import get_connection


class Exportador:
    @staticmethod
    def exportar_historial_csv(id_ciudadano, ruta):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT fecha, tipo_actividad, descripcion FROM historial WHERE id_ciudadano = ? ORDER BY fecha DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        conn.close()
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Fecha", "Tipo de Actividad", "Descripción"])
            for r in rows:
                w.writerow([r["fecha"], r["tipo_actividad"], r["descripcion"]])
        return True, f"Historial exportado: {len(rows)} registros"

    @staticmethod
    def exportar_presupuestos_csv(id_ciudadano, ruta):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT created_at, total, dias, destino_principal, fecha_viaje FROM presupuesto WHERE id_ciudadano = ? ORDER BY created_at DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        conn.close()
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Fecha", "Total (S/)", "Días", "Destino", "Fecha Viaje"])
            for r in rows:
                w.writerow([r["created_at"], f"{r['total']:.2f}", r["dias"], r["destino_principal"] or "", r["fecha_viaje"] or ""])
        return True, f"Presupuestos exportados: {len(rows)} registros"

    @staticmethod
    def exportar_ahorros_csv(id_ciudadano, ruta):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT meta, monto_objetivo, monto_actual, fecha_inicio, fecha_limite, estado FROM ahorro WHERE id_ciudadano = ? ORDER BY fecha_inicio DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        conn.close()
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Meta", "Objetivo (S/)", "Ahorrado (S/)", "Inicio", "Límite", "Estado"])
            for r in rows:
                pct = (r["monto_actual"] / r["monto_objetivo"] * 100) if r["monto_objetivo"] > 0 else 0
                w.writerow([r["meta"], f"{r['monto_objetivo']:.2f}", f"{r['monto_actual']:.2f} ({pct:.0f}%)", r["fecha_inicio"], r["fecha_limite"] or "", r["estado"]])
        return True, f"Metas exportadas: {len(rows)} registros"

    @staticmethod
    def exportar_reporte_txt(id_ciudadano, ruta, nombre_ciudadano):
        conn = get_connection()
        cursor = conn.cursor()
        lineas = []
        lineas.append("=" * 60)
        lineas.append("  DESCUBRE AYACUCHO - REPORTE COMPLETO")
        lineas.append(f"  Usuario: {nombre_ciudadano}")
        lineas.append(f"  Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lineas.append("=" * 60)

        lineas.append("\n--- HISTORIAL DE ACTIVIDADES ---")
        cursor.execute(
            "SELECT fecha, tipo_actividad, descripcion FROM historial WHERE id_ciudadano = ? ORDER BY fecha DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        if rows:
            for r in rows:
                lineas.append(f"  [{r['fecha']}] {r['tipo_actividad']}: {r['descripcion']}")
        else:
            lineas.append("  (Sin registros)")
        lineas.append(f"  Total: {len(rows)} actividades")

        lineas.append("\n--- PRESUPUESTOS ---")
        cursor.execute(
            "SELECT created_at, total, dias, destino_principal FROM presupuesto WHERE id_ciudadano = ? ORDER BY created_at DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        if rows:
            for r in rows:
                destino = f" - {r['destino_principal']}" if r["destino_principal"] else ""
                lineas.append(f"  [{r['created_at']}] S/ {r['total']:.2f} para {r['dias']} días{destino}")
        else:
            lineas.append("  (Sin presupuestos)")
        lineas.append(f"  Total: {len(rows)} presupuestos")

        lineas.append("\n--- METAS DE AHORRO ---")
        cursor.execute(
            "SELECT meta, monto_objetivo, monto_actual, estado FROM ahorro WHERE id_ciudadano = ? ORDER BY fecha_inicio DESC",
            (id_ciudadano,),
        )
        rows = cursor.fetchall()
        if rows:
            for r in rows:
                pct = (r["monto_actual"] / r["monto_objetivo"] * 100) if r["monto_objetivo"] > 0 else 0
                lineas.append(f"  {r['meta']}: S/ {r['monto_actual']:.2f} / S/ {r['monto_objetivo']:.2f} ({pct:.0f}%) - {r['estado']}")
        else:
            lineas.append("  (Sin metas de ahorro)")
        lineas.append(f"  Total: {len(rows)} metas")

        lineas.append("\n" + "=" * 60)
        lineas.append("  Fin del reporte")
        lineas.append("=" * 60)

        conn.close()
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas))
        return True, "Reporte TXT generado exitosamente"
