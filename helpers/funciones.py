import flet as ft

class Temas:
    txt_headline_med = ft.TextThemeStyle.HEADLINE_MEDIUM
class Iconos:
    create_outline = ft.icons.CREATE_OUTLINED
    delete_outline = ft.icons.DELETE_OUTLINE
    done_outline = ft.icons.DONE_OUTLINE_OUTLINED

class Controles:
    def display_texto(t, s=None, c=ft.colors.WHITE, bgc=None, w=None, st=None):
        return ft.Text(t,   size=s, color=c,    bgcolor=bgc,    weight=w, style= st)

    def input_texto(txt="", e=True, fn=None):
        return ft.TextField(hint_text=txt, on_submit=fn, expand=e)

    def input_checkbox(val, lbl=None, fn=None):
        return ft.Checkbox(value=val,   label=lbl,  on_change=fn)

    def layout_fila(c=[], a=ft.MainAxisAlignment.SPACE_BETWEEN, va=ft.CrossAxisAlignment.CENTER, s=0, v=True):
        return ft.Row(alignment=a,  vertical_alignment=va,  controls=c, spacing=s, visible=v)

    def boton(txt, icon=None, fn=None):
        return ft.IconButton(icon=icon, tooltip=txt,    on_click=fn)

    def icono(icon, color=None, txt=None, fn=None):
        return ft.IconButton(icon=icon,    icon_color=color,   tooltip=txt,    on_click=fn)

    def tab(c=[], scrolleable=False, selected=0, fn=None):
        return ft.Tabs(scrollable=scrolleable, selected_index=selected, on_change=fn, tabs=c)

    def tab_item(txt):
        return ft.Tab(text=txt)
