import flet as ft
from database.database_manager import DatabaseManager

class HomePage:
    def __init__(self, theme_manager, db_manager: DatabaseManager = None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.content = None
        
        # Estado de interacciones (me gusta, guardados, etc.)
        self.liked_posts = set()
        self.saved_posts = set()
        self.post_comments = {}
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        # Crear publicaciones de ejemplo
        posts = self._create_sample_posts(colors)
        
        home_content = ft.Column(
            controls=[
                # Encabezado
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=20,
                    margin=ft.margin.only(bottom=10),
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Inicio",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=colors["text_primary"]
                            ),
                            ft.Text(
                                "Descubre entrenamientos de tu comunidad",
                                size=14,
                                color=colors["text_secondary"]
                            ),
                        ]
                    )
                ),
                
                # Feed de publicaciones
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=15,
                    border_radius=15,
                    content=ft.Column(
                        controls=posts,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=15
                    )
                ),
            ],
            scroll=ft.ScrollMode.AUTO
        )
        
        self.content = ft.ListView(
            expand=True,
            spacing=0,
            padding=10,
            controls=[home_content]
        )
        
        return self.content
    
    def _create_sample_posts(self, colors):
        """Crear publicaciones de ejemplo con botones de interacción"""
        posts = []
        
        sample_posts_data = [
            {
                "author": "Carlos Martínez",
                "username": "@carlos_fit",
                "avatar": "https://i.pravatar.cc/150?img=2",
                "image": "https://images.pexels.com/photos/414029/pexels-photo-414029.jpeg",
                "caption": "Sesión de entrenamiento matutina 💪 ¡Nada como empezar el día con energía!",
                "likes": 234,
                "comments": 12,
                "post_id": 1
            },
            {
                "author": "María López",
                "username": "@maria_runner",
                "avatar": "https://i.pravatar.cc/150?img=3",
                "image": "https://images.pexels.com/photos/1199590/pexels-photo-1199590.jpeg",
                "caption": "10km en el Bosque de Palermo 🏃‍♀️ ¡Qué hermoso día para correr!",
                "likes": 456,
                "comments": 28,
                "post_id": 2
            },
            {
                "author": "Juan Rodríguez",
                "username": "@juan_voley",
                "avatar": "https://i.pravatar.cc/150?img=4",
                "image": "https://images.pexels.com/photos/2291872/pexels-photo-2291872.jpeg",
                "caption": "Torneo de vóley en el club 🏐 ¡Ganamos 3-1!",
                "likes": 189,
                "comments": 15,
                "post_id": 3
            },
        ]
        
        for post_data in sample_posts_data:
            post_id = post_data["post_id"]
            is_liked = post_id in self.liked_posts
            is_saved = post_id in self.saved_posts
            
            post_card = ft.Container(
                bgcolor=colors["content_bg"],
                padding=15,
                border_radius=10,
                border=ft.border.all(1, colors["divider_color"]),
                content=ft.Column(
                    controls=[
                        # Encabezado del post
                        ft.Row(
                            controls=[
                                ft.CircleAvatar(
                                    content=ft.Image(src=post_data["avatar"]),
                                    radius=20
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            post_data["author"],
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=colors["text_primary"]
                                        ),
                                        ft.Text(
                                            post_data["username"],
                                            size=12,
                                            color=colors["text_secondary"]
                                        ),
                                    ],
                                    expand=True
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.MORE_VERT,
                                    icon_color=colors["text_secondary"],
                                    icon_size=20
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        
                        ft.Container(height=10),
                        
                        # Imagen del post
                        ft.Image(
                            src=post_data["image"],
                            height=200,
                            fit=ft.ImageFit.COVER,
                            border_radius=8
                        ),
                        
                        ft.Container(height=10),
                        
                        # Descripción
                        ft.Text(
                            post_data["caption"],
                            size=14,
                            color=colors["text_primary"]
                        ),
                        
                        ft.Container(height=10),
                        
                        # Estadísticas
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"❤️ {post_data['likes']} Me gusta",
                                    size=12,
                                    color=colors["text_secondary"]
                                ),
                                ft.Text(
                                    f"💬 {post_data['comments']} Comentarios",
                                    size=12,
                                    color=colors["text_secondary"]
                                ),
                            ],
                            spacing=20
                        ),
                        
                        ft.Divider(color=colors["divider_color"]),
                        
                        # Botones de interacción
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.FAVORITE if is_liked else ft.Icons.FAVORITE_BORDER,
                                    icon_color=ft.Colors.RED_500 if is_liked else colors["text_secondary"],
                                    tooltip="Me gusta",
                                    on_click=lambda e, pid=post_id: self.toggle_like(e, pid, colors)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.COMMENT,
                                    icon_color=colors["text_secondary"],
                                    tooltip="Comentar",
                                    on_click=lambda e, pid=post_id: self.show_comments(e, pid, colors)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.BOOKMARK if is_saved else ft.Icons.BOOKMARK_BORDER,
                                    icon_color=ft.Colors.BLUE_500 if is_saved else colors["text_secondary"],
                                    tooltip="Guardar",
                                    on_click=lambda e, pid=post_id: self.toggle_save(e, pid, colors)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.SHARE,
                                    icon_color=colors["text_secondary"],
                                    tooltip="Compartir",
                                    on_click=lambda e: self.share_post(e)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND
                        ),
                    ]
                )
            )
            
            posts.append(post_card)
        
        return posts
    
    def toggle_like(self, e, post_id, colors):
        """Alternar me gusta en una publicación"""
        if post_id in self.liked_posts:
            self.liked_posts.remove(post_id)
        else:
            self.liked_posts.add(post_id)
        
        # Cambiar icono
        if post_id in self.liked_posts:
            e.control.icon = ft.Icons.FAVORITE
            e.control.icon_color = ft.Colors.RED_500
        else:
            e.control.icon = ft.Icons.FAVORITE_BORDER
            e.control.icon_color = colors["text_secondary"]
        
        e.page.update()
    
    def toggle_save(self, e, post_id, colors):
        """Alternar guardar una publicación"""
        if post_id in self.saved_posts:
            self.saved_posts.remove(post_id)
        else:
            self.saved_posts.add(post_id)
        
        # Cambiar icono
        if post_id in self.saved_posts:
            e.control.icon = ft.Icons.BOOKMARK
            e.control.icon_color = ft.Colors.BLUE_500
        else:
            e.control.icon = ft.Icons.BOOKMARK_BORDER
            e.control.icon_color = colors["text_secondary"]
        
        e.page.update()
    
    def show_comments(self, e, post_id, colors):
        """Mostrar modal de comentarios"""
        comment_field = ft.TextField(
            label="Escribe un comentario...",
            width=250,
            color=colors["text_primary"],
            border_color=colors["divider_color"]
        )
        
        def add_comment(e):
            if comment_field.value:
                if post_id not in self.post_comments:
                    self.post_comments[post_id] = []
                self.post_comments[post_id].append(comment_field.value)
                comment_field.value = ""
                e.page.update()
        
        comments_list = ft.Column(
            controls=[
                ft.Text(
                    f"Comentarios ({len(self.post_comments.get(post_id, []))})",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=colors["text_primary"]
                ),
                *[
                    ft.Container(
                        bgcolor=colors["content_bg"],
                        padding=10,
                        border_radius=8,
                        content=ft.Text(
                            comment,
                            size=12,
                            color=colors["text_primary"]
                        )
                    )
                    for comment in self.post_comments.get(post_id, [])
                ]
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Comentarios", color=colors["text_primary"]),
            content=ft.Column(
                controls=[
                    comments_list,
                    ft.Container(height=10),
                    ft.Row(
                        controls=[
                            comment_field,
                            ft.IconButton(
                                icon=ft.Icons.SEND,
                                icon_color=ft.Colors.RED_500,
                                on_click=add_comment
                            )
                        ]
                    )
                ],
                width=300,
                height=400
            ),
            bgcolor=colors["card_bg"],
        )
        
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()
    
    def share_post(self, e):
        """Compartir publicación"""
        snack = ft.SnackBar(
            ft.Text("Publicación compartida", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_500
        )
        e.page.overlay.append(snack)
        snack.open = True
        e.page.update()
    
    def update_theme(self):
        """Actualizar tema"""
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]
