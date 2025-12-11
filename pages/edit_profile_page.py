import flet as ft
from database.database_manager import DatabaseManager
from database.models import User

class EditProfilePage:
    def __init__(self, theme_manager, db_manager: DatabaseManager = None, page: ft.Page = None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.page = page
        self.current_user = None
        self.on_back = None
        self.content = None
        self.selected_image_path = None
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
    
    def set_user(self, user: User):
        self.current_user = user
    
    def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Maneja la selección de archivo de imagen"""
        if e.files:
            self.selected_image_path = e.files[0].path
            # Actualizar la vista previa de la imagen
            if self.avatar_image:
                self.avatar_image.src = self.selected_image_path
                self.avatar_image.update()
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        if not self.current_user:
            return ft.Container()
        
        self.avatar_image = ft.Image(
            src=self.current_user.avatar_url or "https://i.pravatar.cc/150?img=1",
            width=120,
            height=120,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(60)
        )
        
        avatar_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.avatar_image,
                    ft.ElevatedButton(
                        "Cambiar Foto",
                        icon=ft.Icons.CAMERA_ALT,
                        on_click=lambda e: self.file_picker.pick_files(
                            allowed_extensions=["jpg", "jpeg", "png"]
                        )
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            padding=20,
            bgcolor=colors["card_bg"],
            border_radius=15,
            margin=ft.margin.only(bottom=20)
        )
        
        name_field = ft.TextField(
            label="Nombre Completo",
            value=self.current_user.full_name,
            bgcolor=colors["content_bg"],
            text_size=14,
            border_color=colors["text_secondary"],
            label_style=ft.TextStyle(color=colors["text_secondary"])
        )
        
        bio_field = ft.TextField(
            label="Biografía",
            value=self.current_user.bio or "",
            multiline=True,
            min_lines=3,
            max_lines=5,
            bgcolor=colors["content_bg"],
            text_size=14,
            border_color=colors["text_secondary"],
            label_style=ft.TextStyle(color=colors["text_secondary"])
        )
        
        sport_field = ft.TextField(
            label="Deporte",
            value=self.current_user.sport or "",
            bgcolor=colors["content_bg"],
            text_size=14,
            border_color=colors["text_secondary"],
            label_style=ft.TextStyle(color=colors["text_secondary"])
        )
        
        def save_profile(e):
            if self.db_manager and self.current_user:
                self.current_user.full_name = name_field.value
                self.current_user.bio = bio_field.value
                self.current_user.sport = sport_field.value
                if self.selected_image_path:
                    self.current_user.avatar_url = self.selected_image_path
                self.db_manager.update_user(self.current_user)
            
            if self.on_back:
                self.on_back()
        
        content = ft.Column(
            controls=[
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
                                "Editar Perfil",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=colors["text_primary"]
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                
                avatar_container,
                
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=20,
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            name_field,
                            ft.Container(height=15),
                            bio_field,
                            ft.Container(height=15),
                            sport_field,
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "Guardar Cambios",
                                width=300,
                                bgcolor=ft.Colors.RED_500,
                                color=ft.Colors.WHITE,
                                on_click=save_profile
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        self.content = ft.ListView(
            expand=True,
            spacing=0,
            padding=10,
            controls=[content]
        )
        
        if self.page and self.file_picker not in self.page.overlay:
            self.page.overlay.append(self.file_picker)
        
        return self.content
    
    def update_theme(self):
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]
