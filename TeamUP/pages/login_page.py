import flet as ft
from database.database_manager import DatabaseManager

class LoginPage:
    def __init__(self, theme_manager, db_manager: DatabaseManager, login_callback, registration_callback):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.login_callback = login_callback
        self.registration_callback = registration_callback
        self.content = None
        self.username_field = ft.TextField()
        self.password_field = ft.TextField()
        self.error_text = ft.Text()
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        self.username_field = ft.TextField(
            label="Nombre de Usuario",
            width=300,
            color=colors["text_primary"],
            border_color=colors["divider_color"]
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            color=colors["text_primary"],
            border_color=colors["divider_color"]
        )
        
        self.error_text = ft.Text(
            color=ft.Colors.RED_500,
            size=12,
            visible=False
        )
        
        login_content = ft.Container(
            bgcolor=colors["content_bg"],
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(height=50),
                    ft.Text(
                        "Bienvenido a TeamUP",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=colors["text_primary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Conectar con atletas de todo el mundo",
                        size=16,
                        color=colors["text_secondary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=40),
                    ft.Icon(
                        ft.Icons.SPORTS,
                        size=80,
                        color=ft.Colors.RED_500
                    ),
                    ft.Container(height=40),
                    self.username_field,
                    ft.Container(height=10),
                    self.password_field,
                    ft.Container(height=10),
                    self.error_text,
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Iniciar Sesion",
                        width=300,
                        height=45,
                        bgcolor=ft.Colors.RED_500,
                        color=ft.Colors.WHITE,
                        on_click=self.handle_login
                    ),
                    ft.Container(height=10),
                    ft.TextButton(
                        "No tienes una cuenta? Registrate",
                        on_click=lambda e: self.registration_callback()
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        )
        
        self.content = login_content
        return self.content
    
    def handle_login(self, e):
        username = self.username_field.value
        password = self.password_field.value
        
        if not username or not password:
            self.show_error("Por favor ingresa tu nombre de usuario y contraseña")
            return
        
        user = self.db_manager.authenticate_user(username, password)
        if user:
            self.login_callback(user)
        else:
            self.show_error("Nombre de usuario o contraseña incorrectos")
    
    def show_error(self, message):
        self.error_text.value = message
        self.error_text.visible = True
        self.error_text.update()
    
    def update_theme(self):
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]