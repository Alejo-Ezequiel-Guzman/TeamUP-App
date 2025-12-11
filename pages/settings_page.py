import flet as ft
from database.database_manager import DatabaseManager
from database.models import User

class SettingsPage:
    def __init__(self, theme_manager, db_manager: DatabaseManager = None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.current_user = None
        self.on_back = None
        self.content = None
    
    def set_user(self, user: User):
        self.current_user = user
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        settings_controls = [
            ft.Container(
                bgcolor=colors["card_bg"],
                padding=20,
                margin=ft.margin.only(bottom=20),
                border_radius=15,
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            on_click=lambda e: self.on_back() if self.on_back else None
                        ),
                        ft.Text(
                            "Configuración",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=colors["text_primary"]
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            ),
            
            ft.Container(
                bgcolor=colors["card_bg"],
                padding=15,
                margin=ft.margin.only(bottom=10),
                border_radius=15,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Preferencias",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=colors["text_primary"]
                        ),
                        ft.Container(height=10),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Modo Oscuro",
                                    color=colors["text_primary"],
                                    expand=True
                                ),
                                ft.Switch(
                                    value=self.theme_manager.is_dark_mode,
                                    on_change=lambda e: self._toggle_dark_mode(e)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Divider(color=colors["divider_color"]),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Notificaciones",
                                    color=colors["text_primary"],
                                    expand=True
                                ),
                                ft.Switch(value=True),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Divider(color=colors["divider_color"]),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Privacidad de Perfil",
                                    color=colors["text_primary"],
                                    expand=True
                                ),
                                ft.Switch(value=True),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ]
                )
            ),
            
            ft.Container(
                bgcolor=colors["card_bg"],
                padding=15,
                margin=ft.margin.only(bottom=10),
                border_radius=15,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Cuenta",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=colors["text_primary"]
                        ),
                        ft.Container(height=10),
                        ft.TextButton(
                            "Cambiar Contraseña",
                            style=ft.ButtonStyle(color=ft.Colors.RED_500)
                        ),
                        ft.TextButton(
                            "Cerrar Sesión",
                            style=ft.ButtonStyle(color=ft.Colors.RED_500)
                        ),
                    ]
                )
            ),
        ]
        
        content = ft.Column(
            controls=settings_controls,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        self.content = ft.ListView(
            expand=True,
            spacing=0,
            padding=10,
            controls=[content]
        )
        
        return self.content
    
    def _toggle_dark_mode(self, e):
        self.theme_manager.toggle_dark_mode()
        if hasattr(e, 'page') and e.page:
            e.page.update()
    
    def update_theme(self):
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]
