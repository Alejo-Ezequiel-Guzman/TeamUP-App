import flet as ft
from database.database_manager import DatabaseManager
from database.models import Post

class UploadPage:
    def __init__(self, theme_manager, db_manager: DatabaseManager, current_user, upload_callback):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.current_user = current_user
        self.upload_callback = upload_callback
        self.content = None
        
        # Form fields
        self.caption_field = ft.TextField()
        self.image_url_field = ft.TextField()
        self.error_text = ft.Text()
        self.success_text = ft.Text()
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        self.caption_field = ft.TextField(
            label="Descripcion",
            width=320,
            multiline=True,
            max_lines=4,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            hint_text="Comparte tu aventura"
        )
        
        self.image_url_field = ft.TextField(
            label="URL de la Imagen",
            width=320,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            hint_text="https://example.com/image.jpg"
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
        
        upload_content = ft.Container(
            bgcolor=colors["content_bg"],
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(height=20),
                    ft.Text(
                        "Crea una publicacion",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=colors["text_primary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Comparte tus logros",
                        size=16,
                        color=colors["text_secondary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
                    
                    # Vista previa de la imagen
                    ft.Container(
                        width=320,
                        height=200,
                        bgcolor=colors["card_bg"],
                        border_radius=10,
                        content=ft.Column(
                            controls=[
                                ft.Icon(
                                    ft.Icons.IMAGE,
                                    size=60,
                                    color=colors["text_secondary"]
                                ),
                                ft.Text(
                                    "Previsualizacion de la imagen",
                                    color=colors["text_secondary"]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                    
                    ft.Container(height=20),
                    self.image_url_field,
                    
                    ft.Container(height=20),
                    self.caption_field,
                    
                    ft.Container(height=10),
                    self.error_text,
                    self.success_text,
                    
                    ft.Container(height=20),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Cancelar",
                                width=150,
                                bgcolor=colors["card_bg"],
                                color=colors["text_primary"],
                                on_click=lambda e: self.upload_callback()
                            ),
                            ft.ElevatedButton(
                                "Publicar",
                                width=150,
                                bgcolor=ft.Colors.RED_500,
                                color=ft.Colors.WHITE,
                                on_click=self.handle_upload
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        )
        
        self.content = upload_content
        return self.content
    
    def set_image_url(self, url):
        self.image_url_field.value = url
        self.image_url_field.update()
    
    def handle_upload(self, e):
        if not self.validate_form():
            return
        
        if not self.current_user.current:
            self.show_error("Inicia sesion para crear una publicacion")
            return
        
        # Crear objeto publicacion
        new_post = Post(
            user_id=self.current_user.current.id,
            caption=self.caption_field.value.strip(),
            image_url=self.image_url_field.value.strip()
        )
        
        # intentar crear la publicacion
        post_id = self.db_manager.create_post(new_post)
        if post_id:
            self.show_success("Publicacion creada exitosamente!")
            # Limpiar el formulario
            self.clear_form()
            # Ir a la pagina anterior despues de 2 segundos
            import threading
            threading.Timer(2.0, lambda: self.upload_callback()).start()
        else:
            self.show_error("Error al crear la publicacion. Intenta de nuevo")
    
    def validate_form(self):
        if not self.caption_field.value or not self.caption_field.value.strip():
            self.show_error("Ingresa una descripcion para la publicacion")
            return False
        
        if not self.image_url_field.value or not self.image_url_field.value.strip():
            self.show_error("URL de la imagen es requerida")
            return False
        
        # Basic URL validation
        url = self.image_url_field.value.strip()
        if not (url.startswith("http://") or url.startswith("https://")):
            self.show_error("Ingresa una URL valida para la imagen")
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
        self.caption_field.value = ""
        self.image_url_field.value = ""
        self.caption_field.update()
        self.image_url_field.update()
    
    def update_theme(self):
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]