import flet as ft

def create_post(nombre, avatar_url, imagen_url, descripcion, theme_colors, likes_count=0, comments_count=0):
    return ft.Container(
        bgcolor=theme_colors["card_bg"],
        padding=15,
        margin=ft.margin.only(bottom=5),
        border_radius=15,
        content=ft.Column(
            controls=[
                # Header
                ft.Row(
                    controls=[
                        ft.CircleAvatar(content=ft.Image(src=avatar_url), radius=20),
                        ft.Text(
                            nombre, 
                            weight=ft.FontWeight.BOLD, 
                            color=theme_colors["text_primary"]
                        ),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.MORE_VERT, color=theme_colors["icon_color"]),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                # Divisor
                ft.Container(height=10),
                # Imagen
                ft.Image(
                    src=imagen_url, 
                    fit=ft.ImageFit.COVER, 
                    height=250, 
                    border_radius=ft.border_radius.all(10)
                ),
                ft.Container(height=10),
                # Botones de interaccion
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.FAVORITE_BORDER, color=theme_colors["icon_color"]),
                                ft.Text(str(likes_count), color=theme_colors["text_secondary"], size=12)
                            ],
                            spacing=5
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.MODE_COMMENT_OUTLINED, color=theme_colors["icon_color"]),
                                ft.Text(str(comments_count), color=theme_colors["text_secondary"], size=12)
                            ],
                            spacing=5
                        ),
                        ft.Icon(ft.Icons.NEAR_ME_OUTLINED, color=theme_colors["icon_color"]),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.BOOKMARK_BORDER, color=theme_colors["icon_color"]),
                    ]
                ),
                ft.Container(height=5),
                # Descripcion
                ft.Text(descripcion, size=14, color=theme_colors["text_primary"]),
                ft.Divider(height=15, thickness=1, color=theme_colors["divider_color"]),
            ]
        )
    )