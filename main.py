import flet as ft
from DB_CONN import *
import os


def main(page: ft.Page):

    def conectar():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="control_stock"
        )

    def obtener():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT codigo, descripcion, cantidad_disp, proveedor FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return productos

    def actualizar(lista):
        tabla.rows.clear()

        for p in lista:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(p["codigo"]))),
                        ft.DataCell(ft.Text(p["descripcion"])),
                        ft.DataCell(ft.Text(str(p["cantidad_disp"]))),
                        ft.DataCell(ft.Text(p["proveedor"]))
                    ]
                )
            )

        page.update()

    productos = obtener()

    def filtrar(texto):
        texto = texto.lower().strip()

        if not texto:
            actualizar(productos)
        else:
            filtrados = [
                p for p in productos
                if texto in str(p["codigo"]).lower()
                or texto in p["descripcion"].lower()
                or texto in p["proveedor"].lower()
            ]

            actualizar(filtrados)

    search_field = ft.TextField(
        label="Busqueda",
        on_change=lambda e: filtrar(e.control.value)
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Codigo")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Cantidad disponible")),
            ft.DataColumn(ft.Text("Proveedor")),
        ],
        rows=[]
    )

    actualizar(productos)

    page.add(
        search_field,
        tabla
    )

ft.app(target=main)