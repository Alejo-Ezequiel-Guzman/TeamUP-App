import flet as ft
from database.database_manager import DatabaseManager
from database.models import User

class ProfilePage:
    def __init__(self, theme_manager, db_manager: DatabaseManager = None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.content = None
        self.current_user = None
        self.page_callbacks = {}
        
        self.default_user_data = {
            "name": "Usuario TeamUP",
            "username": "@teamup_user",
            "bio": "Deportista apasionado 🏃‍♂️",
            "followers": "0",
            "following": "0",
            "posts": "0",
            "avatar": "https://i.pravatar.cc/150?img=1",
            "sport": "Múltiples deportes",
            "achievements": ["🏃‍♂️ Bienvenido a TeamUP", "💪 Completa tu perfil"]
        }
    
    def set_user(self, user: User):
        self.current_user = user
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        if self.current_user:
            user_data = {
                "name": self.current_user.full_name,
                "username": f"@{self.current_user.username}",
                "bio": self.current_user.bio,
                "followers": str(self.current_user.followers_count),
                "following": str(self.current_user.following_count),
                "posts": str(self.current_user.posts_count),
                "avatar": self.current_user.avatar_url or "https://i.pravatar.cc/150?img=1",
                "sport": self.current_user.sport,
                "achievements": ["🏃‍♂️ Campeon Running 2019", "💪 3er puesto VNL 2022"]
            }
            
            user_posts = []
            if self.db_manager:
                user_posts = self.db_manager.get_user_posts(self.current_user.id)
        else:
            user_data = self.default_user_data
            user_posts = []
        
        edit_button = ft.ElevatedButton(
            "Editar Perfil",
            width=300,
            bgcolor=ft.Colors.RED_500,
            color=ft.Colors.WHITE,
            icon=ft.Icons.EDIT,
            on_click=self.page_callbacks.get("show_edit_profile")
        )
        
        settings_button = ft.ElevatedButton(
            "Configuración",
            width=300,
            bgcolor=colors["card_bg"],
            color=colors["text_primary"],
            icon=ft.Icons.SETTINGS,
            on_click=self.page_callbacks.get("show_settings")
        )
        
        profile_content = ft.Column(
            controls=[
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=20,
                    margin=ft.margin.only(bottom=10),
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.CircleAvatar(
                                        content=ft.Image(
                                            src=user_data["avatar"],
                                            fit=ft.ImageFit.COVER,
                                            error_content=ft.Icon(
                                                ft.Icons.ACCOUNT_CIRCLE,
                                                size=80,
                                                color=colors["text_secondary"]
                                            )
                                        ),
                                        radius=40
                                    ),
                                    ft.Container(width=20),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                user_data["name"],
                                                size=24,
                                                weight=ft.FontWeight.BOLD,
                                                color=colors["text_primary"]
                                            ),
                                            ft.Text(
                                                user_data["username"],
                                                size=16,
                                                color=colors["text_secondary"]
                                            ),
                                            ft.Text(
                                                user_data["sport"],
                                                size=14,
                                                color=ft.Colors.RED_500,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                        ],
                                        expand=True
                                    )
                                ]
                            ),
                            ft.Container(height=15),
                            ft.Text(
                                user_data["bio"],
                                size=14,
                                color=colors["text_primary"]
                            ),
                        ]
                    )
                ),
                
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=15,
                    margin=ft.margin.only(bottom=10),
                    border_radius=15,
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        user_data["posts"],
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["text_primary"]
                                    ),
                                    ft.Text("Publicaciones", size=12, color=colors["text_secondary"])
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.VerticalDivider(color=colors["divider_color"]),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        user_data["followers"],
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["text_primary"]
                                    ),
                                    ft.Text("Seguidores", size=12, color=colors["text_secondary"])
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.VerticalDivider(color=colors["divider_color"]),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        user_data["following"],
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["text_primary"]
                                    ),
                                    ft.Text("Siguiendo", size=12, color=colors["text_secondary"])
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND
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
                                "Publicaciones recientes" if user_posts else "Logros",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=colors["text_primary"]
                            ),
                            ft.Container(height=10),
                            *self._create_posts_or_achievements(user_posts, user_data, colors)
                        ]
                    )
                ),
                
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=15,
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            edit_button,
                            ft.Container(height=10),
                            settings_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
            ],
            scroll=ft.ScrollMode.AUTO
        )
        
        self.content = ft.ListView(
            expand=True,
            spacing=0,
            padding=10,
            controls=[profile_content]
        )
        
        return self.content
    
    def _create_posts_or_achievements(self, user_posts, user_data, colors):
        if user_posts:
            return [ft.Container(
                bgcolor=colors["content_bg"],
                padding=10,
                margin=ft.margin.only(bottom=5),
                border_radius=8,
                content=ft.Column(
                    controls=[
                        ft.Image(
                            src=post.image_url,
                            height=100,
                            fit=ft.ImageFit.COVER,
                            border_radius=5
                        ),
                        ft.Text(
                            post.caption[:50] + "..." if len(post.caption) > 50 else post.caption,
                            size=12,
                            color=colors["text_primary"]
                        ),
                        ft.Text(
                            f"❤️ {post.likes_count} 💬 {post.comments_count}",
                            size=10,
                            color=colors["text_secondary"]
                        )
                    ]
                )
            ) for post in user_posts[:3]]
        else:
            achievements = user_data.get("achievements", ["🏃‍♂️ Campeon Running 2018", "💪 3er puesto VNL 2022"])
            return [ft.Text(
                achievement,
                size=14,
                color=colors["text_primary"]
            ) for achievement in achievements]
    
    def update_theme(self):
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]
    
    def _update_container_colors(self, container, colors):
        if hasattr(container, 'content'):
            self._update_content_colors(container.content, colors)
    
    def _update_content_colors(self, content, colors):
        if isinstance(content, (ft.Column, ft.Row)):
            for control in content.controls:
                if isinstance(control, ft.Text):
                    if control.color != ft.Colors.RED_500: 
                        if control.size == 12 or control.size == 10:  
                            control.color = colors["text_secondary"]
                        else:
                            control.color = colors["text_primary"]
