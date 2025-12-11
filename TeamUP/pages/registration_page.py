import flet as ft
from database.database_manager import DatabaseManager
from database.models import User

class RegistrationPage:
    def __init__(self, theme_manager, db_manager: DatabaseManager, registration_callback, login_callback):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.registration_callback = registration_callback
        self.login_callback = login_callback
        self.content = None
        
        # Form fields
        self.username_field = ft.TextField()
        self.email_field = ft.TextField()
        self.password_field = ft.TextField()
        self.confirm_password_field = ft.TextField()
        self.full_name_field = ft.TextField()
        self.bio_field = ft.TextField()
        self.sport_field = ft.Dropdown()
        self.error_text = ft.Text()
        self.success_text = ft.Text()
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        # Initialize form fields
        self.username_field = ft.TextField(
            label="Nombre de Usuario",
            width=300,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            prefix_icon=ft.Icons.PERSON
        )
        
        self.email_field = ft.TextField(
            label="Email",
            width=300,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            prefix_icon=ft.Icons.EMAIL
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            prefix_icon=ft.Icons.LOCK
        )
        
        self.confirm_password_field = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            prefix_icon=ft.Icons.LOCK_OUTLINE
        )
        
        self.full_name_field = ft.TextField(
            label="Nombre Completo",
            width=300,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            prefix_icon=ft.Icons.BADGE
        )
        
        self.bio_field = ft.TextField(
            label="Bio (Opcional)",
            width=300,
            multiline=True,
            max_lines=3,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            prefix_icon=ft.Icons.DESCRIPTION
        )
        
        self.sport_field = ft.Dropdown(
            label="Deporte que practicas",
            width=300,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            options=[
                ft.dropdown.Option("Atletismo"),
                ft.dropdown.Option("Running"),
                ft.dropdown.Option("Natacion"),
                ft.dropdown.Option("Ciclismo"),
                ft.dropdown.Option("CrossFit"),
                ft.dropdown.Option("Yoga"),
                ft.dropdown.Option("Basketball"),
                ft.dropdown.Option("Football"),
                ft.dropdown.Option("Tenis"),
                ft.dropdown.Option("Futbol Sala"),
                ft.dropdown.Option("Volleyball"),
                ft.dropdown.Option("Otro"),
            ]
        )
        
        self.error_text = ft.Text(
            color=ft.Colors.RED_500,
            size=12,
            visible=False
        )
        
        self.success_text = ft.Text(
            color=ft.Colors.GREEN_500,
            size=12,
            visible=False
        )
        
        registration_content = ft.Container(
            bgcolor=colors["content_bg"],
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(height=20),
                    ft.Text(
                        "Unete a TeamUP",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=colors["text_primary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Crea tu perfil de atleta",
                        size=16,
                        color=colors["text_secondary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    ft.Icon(
                        ft.Icons.SPORTS,
                        size=60,
                        color=ft.Colors.RED_500
                    ),
                    ft.Container(height=20),
                    self.username_field,
                    ft.Container(height=10),
                    self.email_field,
                    ft.Container(height=10),
                    self.password_field,
                    ft.Container(height=10),
                    self.confirm_password_field,
                    ft.Container(height=10),
                    self.full_name_field,
                    ft.Container(height=10),
                    self.bio_field,
                    ft.Container(height=10),
                    self.sport_field,
                    ft.Container(height=10),
                    self.error_text,
                    self.success_text,
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Crear Cuenta",
                        width=300,
                        height=45,
                        bgcolor=ft.Colors.RED_500,
                        color=ft.Colors.WHITE,
                        on_click=self.handle_registration
                    ),
                    ft.Container(height=10),
                    ft.TextButton(
                        "Ya tienes una cuenta? ir al login",
                        on_click=lambda e: self.login_callback()
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        )
        
        self.content = registration_content
        return self.content
    
    def handle_registration(self, e):
        # Validar el formulario
        if not self.validate_form():
            return
        
        # Crear obbjeto usuario
        new_user = User(
            username=self.username_field.value.strip(),
            email=self.email_field.value.strip(),
            password_hash=self.password_field.value,  # La contraseña va a ser encriptada en el manager de base de datos
            full_name=self.full_name_field.value.strip(),
            bio=self.bio_field.value.strip() if self.bio_field.value else "",
            sport=self.sport_field.value if self.sport_field.value else "Other",
            avatar_url=f"https://i.pravatar.cc/150?u={self.username_field.value}"
        )
        
        # Intentar crear el usuario en la base de datos
        user_id = self.db_manager.create_user(new_user)
        if user_id:
            self.show_success("Cuenta creada con exito! Ya puedes ir al login.")
            # Limpiar el formulario
            self.clear_form()
        else:
            self.show_error("Nombre de Usuario o email ya estan en uso, por favor prueba otros.")
    
    def validate_form(self):
        # Checkear si los campos estan llenos
        if not self.username_field.value or not self.username_field.value.strip():
            self.show_error("Ingresa un nombre de usuario")
            return False
        
        if not self.email_field.value or not self.email_field.value.strip():
            self.show_error("Ingresa un email")
            return False
        
        if not self.password_field.value:
            self.show_error("Ingresa una contraseña")
            return False
        
        if not self.full_name_field.value or not self.full_name_field.value.strip():
            self.show_error("Ingresa tu nombre completo")
            return False
        
        # Validar email
        email = self.email_field.value.strip()
        if "@" not in email or "." not in email:
            self.show_error("Por favor ingresa un email valido")
            return False
        
        # Validar contraseñas
        if self.password_field.value != self.confirm_password_field.value:
            self.show_error("Las contraseñas no coinciden")
            return False
        
        # Validar longitud de la contraseña
        if len(self.password_field.value) < 6:
            self.show_error("la contraseña debe tener al menos 6 caracteres")
            return False
        
        # Validar nombre de usuario
        username = self.username_field.value.strip()
        if len(username) < 3:
            self.show_error("Nombre de usuario debe tener al menos 3 caracteres")
            return False
        
        if not username.replace("_", "").replace(".", "").isalnum():
            self.show_error("Nombre de usuario solo puede contener letras, numeros, guiones bajos y puntos")
            return False
        
        return True
    
    def show_error(self, message):
        self.error_text.value = message
        self.error_text.visible = True
        self.success_text.visible = False
        self.error_text.update()
        self.success_text.update()
    
    def show_success(self, message):
        self.success_text.value = message
        self.success_text.visible = True
        self.error_text.visible = False
        self.success_text.update()
        self.error_text.update()
    
    def clear_form(self):
        self.username_field.value = ""
        self.email_field.value = ""
        self.password_field.value = ""
        self.confirm_password_field.value = ""
        self.full_name_field.value = ""
        self.bio_field.value = ""
        self.sport_field.value = None
        self.username_field.update()
        self.email_field.update()
        self.password_field.update()
        self.confirm_password_field.update()
        self.full_name_field.update()
        self.bio_field.update()
        self.sport_field.update()
    
    def update_theme(self):
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]