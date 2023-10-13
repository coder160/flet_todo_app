import flet as ft
from variabes import Variables as texto
from funciones import Controles
from datetime import datetime


class Task(ft.UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        _fecha_actual = datetime.now()
        _hora_actual = f"{_fecha_actual.hour}:{_fecha_actual.minute}:{_fecha_actual.second}"
        self.fecha = Controles.display_texto(str(_fecha_actual))
        self.hora_inicio = Controles.display_texto(_hora_actual)
        self.hora_fin = Controles.display_texto("--")
        self.edit_name = Controles.input_texto(e=1)
        self.display_task = Controles.input_checkbox(
            False, self.task_name, self.status_changed)
        botones_accion = [Controles.icono(icon=ft.icons.CREATE_OUTLINED, txt=texto.editar, fn=self.edit_clicked),
                          Controles.icono(icon=ft.icons.DELETE_OUTLINE, txt=texto.eliminar, fn=self.delete_clicked)]
        _fila_actividad = [self.display_task, self.hora_inicio,
                           self.hora_fin, Controles.layout_fila(c=botones_accion)]
        self.display_view = Controles.layout_fila(c=_fila_actividad)
        _fila_editar_actividad = [self.edit_name, Controles.icono(icon=ft.icons.DONE_OUTLINE_OUTLINED,
                                                                  txt=texto.actualizar,
                                                                  fn=self.save_clicked,
                                                                  color="#f0f0f0")]
        self.edit_view = Controles.layout_fila(
            c=_fila_editar_actividad, v=False)
        return ft.Column(controls=[self.display_view, self.edit_view])

    async def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def status_changed(self, e):
        _fecha_actual = datetime.now()
        self.completed = self.display_task.value
        if self.completed == True:
            self.hora_fin = Controles.display_texto(
                f"{_fecha_actual.hour}:{_fecha_actual.minute}:{_fecha_actual.second}")

        else:
            self.hora_fin = Controles.display_texto("--")
        await self.task_status_change(self)

    async def delete_clicked(self, e):
        await self.task_delete(self)


class TodoApp(ft.UserControl):
    def build(self):
        self.new_task = Controles.input_texto(
            txt=texto.tooltip_agregar, e=True, fn=self.add_clicked)
        self.tasks = ft.Column()
        self.encabezado = Controles.layout_fila(c=[Controles.display_texto("Actividad"),
                                                   Controles.display_texto(
                                                       "Hora Inicio"),
                                                   Controles.display_texto(
                                                       "Hora Fin"),
                                                   Controles.display_texto("Acciones")])
        self.filtrados = Controles.tab(c=[Controles.tab_item(texto.tabs_todas),
                  Controles.tab_item(texto.tabs_activas),
                  Controles.tab_item(texto.tabs_completas)])

        self.items_left = ft.Text(texto.sin_entradas)

        # application's root control (i.e. "view") containing all other controls
        _encabezado = [ft.Text(value=texto.encabezado,
                               style=ft.TextThemeStyle.HEADLINE_MEDIUM)]
        _barra_nueva_actividad = [self.new_task,
                                  ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked)]
        _info_footer = Controles.layout_fila(c=[self.items_left,
                                                ft.OutlinedButton(
                                                    text=texto.limpiar_todos,
                                                    on_click=self.clear_clicked),
                                                ])
        return ft.Column(
            width=600,
            controls=[
                Controles.layout_fila(
                    c=_encabezado, a=ft.MainAxisAlignment.CENTER),
                Controles.layout_fila(c=_barra_nueva_actividad),
                ft.Column(spacing=25, controls=[self.filtrados,
                                                self.tasks,
                                                self.encabezado,
                                                _info_footer])])

    async def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value,
                        self.task_status_change,
                        self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = texto.barra_agregar_vacia
            await self.new_task.focus_async()
            await self.update_async()

    async def task_status_change(self, task):
        await self.update_async()

    async def task_delete(self, task):
        self.tasks.controls.remove(task)
        await self.update_async()

    async def tabs_changed(self, e):
        await self.update_async()

    async def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                await self.task_delete(task)

    async def update_async(self):
        status = self.filtrados.tabs[self.filtrados.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == texto.tabs_todas
                or (status == texto.tabs_activas and task.completed == False)
                or (status == texto.tabs_completas and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = texto.cantidad_entradas.format(N=count)
        await super().update_async()


async def main(page: ft.Page):
    page.title = texto.titulo
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    await page.add_async(TodoApp())


ft.app(main)
