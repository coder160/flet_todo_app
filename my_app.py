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
        self.fecha = Controles.display_texto(str(_fecha_actual))
        self.hora_inicio = Controles.display_texto(
            f"{_fecha_actual.hour}:{_fecha_actual.minute}:{_fecha_actual.second}")
        # self.hora_inicio = Controles.display_texto("Algo")
        self.hora_fin = Controles.display_texto("--")
        self.edit_name = ft.TextField(expand=1)
        self.display_task = ft.Checkbox(
            value=False,
            label=self.task_name,
            on_change=self.status_changed
        )
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                self.hora_inicio,
                self.hora_fin,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip=texto.editar,
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip=texto.eliminar,
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip=texto.actualizar,
                    on_click=self.save_clicked,
                ),
            ],
        )
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
        self.new_task = ft.TextField(
            hint_text=texto.tooltip_agregar, on_submit=self.add_clicked, expand=True
        )
        self.tasks = ft.Column()
        self.encabezado = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                Controles.display_texto("Actividad"),
                Controles.display_texto("Hora Inicio"),
                Controles.display_texto("Hora Fin"),
                Controles.display_texto("Acciones")
            ]
        )

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text=texto.tabs_todas),
                  ft.Tab(text=texto.tabs_activas),
                  ft.Tab(text=texto.tabs_completas)],
        )

        self.items_left = ft.Text(texto.sin_entradas)

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(value=texto.encabezado,
                             style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        self.encabezado,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text=texto.limpiar_todos,
                                    on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

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
        status = self.filter.tabs[self.filter.selected_index].text
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
