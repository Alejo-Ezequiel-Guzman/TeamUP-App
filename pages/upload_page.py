import flet as ft
import os
import shutil
from database.database_manager import DatabaseManager
from database.models import Post

class UploadPage:
    def __init__(self, theme_manager, db_manager: DatabaseManager, current_user, upload_callback):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.current_user = current_user
        self.upload_callback = upload_callback
        self.content = None
        
        # Campos del formulario
        self.caption_field = ft.TextField()
        self.selected_image_path = None
        self.image_preview = ft.Image()
        self.error_text = ft.Text()
        self.success_text = ft.Text()
        self.file_picker = ft.FilePicker()
        
        # Crear directorio para imágenes si no existe
        self.images_dir = "assets/images/posts"
        os.makedirs(self.images_dir, exist_ok=True)
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        self.caption_field = ft.TextField(
            label="Descripción",
            width=320,
            multiline=True,
            max_lines=4,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            hint_text="Comparte tu viaje atlético..."
        )
        
        # Configurar file picker
        self.file_picker = ft.FilePicker(
            on_result=self.on_file_picked
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
        
        # Vista previa de imagen
        self.image_preview = ft.Container(
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
                        "Selecciona una imagen",
                        color=colors["text_secondary"]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        upload_content = ft.Container(
            bgcolor=colors["content_bg"],
            expand=True,
            content=ft.Column(
                controls=[
                    self.file_picker,  # Agregar file picker a la página
                    ft.Container(height=20),
                    ft.Text(
                        "Crear nueva publicación",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=colors["text_primary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Comparte tus logros atléticos",
                        size=16,
                        color=colors["text_secondary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
                    
                    # Vista previa de imagen
                    self.image_preview,
                    
                    ft.Container(height=20),
                    
                    # Botones para seleccionar imagen
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Seleccionar imagen",
                                icon=ft.Icons.PHOTO_LIBRARY,
                                bgcolor=ft.Colors.RED_500,
                                color=ft.Colors.WHITE,
                                on_click=self.pick_image
                            ),
                            ft.ElevatedButton(
                                "Tomar foto",
                                icon=ft.Icons.CAMERA_ALT,
                                bgcolor=colors["card_bg"],
                                color=colors["text_primary"],
                                on_click=self.take_photo
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
    
                    
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
    
    def pick_image(self, e):
        """Abrir selector de archivos para imágenes"""
        self.file_picker.pick_files(
            dialog_title="Seleccionar imagen",
            file_type=ft.FilePickerFileType.IMAGE,
            allow_multiple=False
        )
    
    def take_photo(self, e):
        """Placeholder para funcionalidad de cámara"""
        self.show_error("Funcionalidad de cámara no disponible en esta versión")
    
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        """Manejar archivo seleccionado"""
        if e.files:
            file = e.files[0]
            self.selected_image_path = file.path
            
            # Actualizar vista previa
            try:
                self.image_preview.content = ft.Image(
                    src=file.path,
                    width=320,
                    height=200,
                    fit=ft.ImageFit.COVER,
                    border_radius=10
                )
                self.image_preview.update()
                
                # Limpiar mensajes de error
                self.error_text.visible = False
                self.error_text.update()
                
            except Exception as ex:
                self.show_error(f"Error al cargar imagen: {str(ex)}")
    
    
    
    def save_image_locally(self, source_path: str) -> str:
        """Guardar imagen localmente y retornar la ruta"""
        if source_path.startswith("http"):
            # Es una URL de muestra, no necesita guardarse localmente
            return source_path
        
        try:
            # Generar nombre único para el archivo
            import uuid
            file_extension = os.path.splitext(source_path)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            destination_path = os.path.join(self.images_dir, unique_filename)
            
            # Copiar archivo
            shutil.copy2(source_path, destination_path)
            
            # Retornar ruta relativa
            return destination_path
            
        except Exception as e:
            raise Exception(f"Error al guardar imagen: {str(e)}")
    
    def handle_upload(self, e):
        if not self.validate_form():
            return
        
        if not self.current_user.current:
            self.show_error("Por favor inicia sesión para crear publicaciones")
            return
        
        try:
            # Guardar imagen localmente
            image_path = self.save_image_locally(self.selected_image_path)
            
            # Crear objeto publicación
            new_post = Post(
                user_id=self.current_user.current.id,
                caption=self.caption_field.value.strip(),
                image_url=image_path  # Usar ruta local en lugar de URL
            )
            
            # Intentar crear publicación
            post_id = self.db_manager.create_post(new_post)
            if post_id:
                self.show_success("¡Publicación creada exitosamente!")
                # Limpiar formulario y regresar después de un retraso
                self.clear_form()
                # Regresar a la página anterior después de 2 segundos
                import threading
                threading.Timer(2.0, lambda: self.upload_callback()).start()
            else:
                self.show_error("Error al crear la publicación. Inténtalo de nuevo.")
                
        except Exception as ex:
            self.show_error(f"Error al procesar imagen: {str(ex)}")
    
    def validate_form(self):
        if not self.caption_field.value or not self.caption_field.value.strip():
            self.show_error("La descripción es requerida")
            return False
        
        if not self.selected_image_path:
            self.show_error("Por favor selecciona una imagen")
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
        self.selected_image_path = None
        self.caption_field.update()
        
        # Resetear vista previa
        colors = self.theme_manager.get_theme_colors()
        self.image_preview.content = ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.IMAGE,
                    size=60,
                    color=colors["text_secondary"]
                ),
                ft.Text(
                    "Selecciona una imagen",
                    color=colors["text_secondary"]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.image_preview.update()
    
    def update_theme(self):
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]
