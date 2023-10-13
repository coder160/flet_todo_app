import flet as ft


class Controles:
    def display_texto(t, s=None, c=ft.colors.WHITE, bgc=None, w=None):
        return ft.Text(t,   size=s, color=c,    bgcolor=bgc,    weight=w)

    def input_texto(txt="",e=True,fn=None):
        return ft.TextField(hint_text=txt, on_submit=fn, expand=e)        

    def input_checkbox(val, lbl=None, fn=None):
        return ft.Checkbox(value=val,   label=lbl,  on_change=fn)
    
    def layout_fila(c=[],a=None,va=None, s=0, v=True):
        return ft.Row(alignment=a,  vertical_alignment=va,  controls=c, spacing=s, visible=v)
    
    def boton(txt,icon=None,fn=None):
        return ft.IconButton(icon=icon, tooltip=txt,    on_click=fn)
    
    def icono(icon,color=None,txt=None,fn=None):
        return ft.IconButton(icon=icon,    icon_color=color,   tooltip=txt,    on_click=fn)
        
