from variabes import Variables as texto
from funciones import Controles, Iconos
from datetime import datetime
import pandas as pd
import flet as ft

class Task(ft.UserControl):
    def __init__(self, nombre_actividad, estatus_actividad, eliminar_actividad):
        super().__init__()
        self.completada = False
        self.nombre_actividad = nombre_actividad
        self.estatus_actividad = estatus_actividad
        self.eliminar_actividad = eliminar_actividad
        _fecha_actual = datetime.now()
        self.fecha = Controles.display_texto(str(_fecha_actual))
        self.hora_inicio = Controles.display_texto(
            str(_fecha_actual.strftime('%I:%M:%S %p')))
        self.hora_fin = Controles.display_texto("--")

    def build(self):
        self.editar_nombre = Controles.input_texto(e=1)
        self.actividad_check = Controles.input_checkbox(
            False, self.nombre_actividad, self.status_changed)

        botones_actividad = [Controles.icono(icon=Iconos.create_outline, txt=texto.editar, fn=self.editar_clickeado),
                             Controles.icono(icon=Iconos.delete_outline, txt=texto.eliminar, fn=self.eliminar_clickeado)]
        icono_editar = Controles.icono(icon=Iconos.done_outline,  color="#f0f0f0",
                                       txt=texto.actualizar, fn=self.guardar_clickeado)

        fila_actividad = [self.actividad_check, self.hora_inicio,
                          self.hora_fin, Controles.layout_fila(c=botones_actividad)]
        fila_editar_actividad = [self.editar_nombre, icono_editar]

        self.display_actividad = Controles.layout_fila(c=fila_actividad, v=True)
        self.edit_actividad = Controles.layout_fila(c=fila_editar_actividad, v=False)
        return ft.Column(controls=[self.display_actividad, self.edit_actividad])

    async def editar_clickeado(self, e):
        self.editar_nombre.value = self.actividad_check.label
        self.display_actividad.visible = False
        self.edit_actividad.visible = True
        await self.update_async()

    async def guardar_clickeado(self, e):
        self.actividad_check.label = self.editar_nombre.value
        self.display_actividad.visible = True
        self.edit_actividad.visible = False
        await self.update_async()

    async def actualizar_finalizado(self, e):
        dtn = datetime.now()
        self.hora_fin.value = str(dtn.strftime('%I:%M:%S %p')) if self.completada == True else "--"
        await self.update_async()

    async def status_changed(self, e):
        self.completada = self.actividad_check.value
        await self.actualizar_finalizado(e)
        await self.estatus_actividad(self)

    async def eliminar_clickeado(self, e):
        await self.eliminar_actividad(self)


class TodoApp(ft.UserControl):
    dialogo_descarga = ft.AlertDialog(title=ft.Text("¡Actividades Descargadas!"))
    def build(self):
        self.actividades = ft.Column()
        self.items_faltantes = ft.Text(texto.sin_entradas)
        texto_encabezado_pagina = [ft.Text(value=texto.encabezado, style=ft.TextThemeStyle.HEADLINE_MEDIUM)]
        self.input_nueva_actividad = Controles.input_texto(txt=texto.tooltip_agregar,
                                                           e=True,
                                                           fn=self.agregar_clickeado)
        barra_nueva_actividad = [self.input_nueva_actividad, 
                                 ft.FloatingActionButton(icon=ft.icons.ADD, 
                                                         on_click=self.agregar_clickeado)]
        self.encabezado_actividades = Controles.layout_fila(c=[Controles.display_texto("Actividad"),
                                                               Controles.display_texto("Hora Inicio"),
                                                               Controles.display_texto("Hora Fin"),
                                                               Controles.display_texto("Acciones")])
        self.filtros_tabs = Controles.tab(fn=self.tabs_actualzadas,
                                          c=[Controles.tab_item(texto.tabs_todas),
                                             Controles.tab_item(texto.tabs_activas),
                                             Controles.tab_item(texto.tabs_completas)])
        self.info_footer = Controles.layout_fila(c=[self.items_faltantes, 
                                                    ft.OutlinedButton(text=texto.limpiar_todos,
                                                                      on_click=self.descargar_actividades)])
        return ft.Column(
            width=600,
            controls=[
                Controles.layout_fila(c=texto_encabezado_pagina, a=ft.MainAxisAlignment.CENTER),
                Controles.layout_fila(c=barra_nueva_actividad),
                ft.Column(spacing=25, controls=[self.filtros_tabs,
                                                self.encabezado_actividades,
                                                self.actividades,
                                                self.info_footer])])

    async def agregar_clickeado(self, e):
        if self.input_nueva_actividad.value:
            actividad = Task(self.input_nueva_actividad.value,
                             self.estatus_actividad, self.eliminar_actividad)
            self.actividades.controls.append(actividad)
            self.input_nueva_actividad.value = texto.barra_agregar_vacia
            await self.input_nueva_actividad.focus_async()
            await self.update_async()

    async def estatus_actividad(self, actividad):
        await self.update_async()

    async def eliminar_actividad(self, actividad):
        self.actividades.controls.remove(actividad)
        await self.update_async()

    async def tabs_actualzadas(self, e):
        await self.update_async()

    async def descargar_actividades(self, e):
        mis_actividades = list([])
        fecha = datetime.now()
        nombre_archivo = f'{texto.archivo}/actividades_{fecha}.csv'
        for actividad in self.actividades.controls[:]:
            mi_actividad = {
                'tarea': actividad.nombre_actividad,
                'fecha': actividad.fecha.value,
                'hora_inicio': actividad.hora_inicio.value,
                'hora_fin': actividad.hora_fin.value,
                'estatus': actividad.completada
                }
            mis_actividades.append(mi_actividad)
        df = pd.DataFrame(mis_actividades)
        df.to_csv(nombre_archivo, index=False)
        #TO-DO: Mostrar Dialogo al Descargar
        #self.dialogo_descarga.open = True

    async def update_async(self):
        status = self.filtros_tabs.tabs[self.filtros_tabs.selected_index].text
        count = 0
        for actividad in self.actividades.controls:
            actividad.visible = (status == texto.tabs_todas
                                 or (status == texto.tabs_activas and actividad.completada == False)
                                 or (status == texto.tabs_completas and actividad.completada))
            if not actividad.completada:
                count += 1
        self.items_faltantes.value = texto.cantidad_entradas.format(N=count)
        await super().update_async()


async def main(page: ft.Page):
    page.title = texto.titulo
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.dialog = TodoApp.dialogo_descarga
    await page.add_async(TodoApp())


ft.app(main)



