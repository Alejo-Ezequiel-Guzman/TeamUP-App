import flet as ft
from datetime import datetime
from database.models import Notification

class NotificationsPage:
    def __init__(self, theme_manager, db_manager=None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.content = None
        self.current_user = None
        self.notifications_list = None
        self.on_back = None
        self.page_callbacks = None
    
    def set_user(self, user):
        """Establecer el usuario actual"""
        self.current_user = user
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        if not self.current_user:
            return ft.Container(
                content=ft.Text("Debe iniciar sesión para ver notificaciones"),
                padding=20
            )
        
        # Obtener notificaciones
        notifications = []
        if self.db_manager:
            notifications = self.db_manager.get_user_notifications(self.current_user.id)
        
        # Header con botón de regresar
        header = ft.Container(
            bgcolor=colors["card_bg"],
            padding=20,
            margin=ft.margin.only(bottom=10),
            border_radius=15,
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=colors["text_primary"],
                        tooltip="Volver",
                        on_click=self.go_back
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "Notificaciones",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=colors["text_primary"]
                            ),
                            ft.Text(
                                f"{len(notifications)} notificaciones",
                                size=14,
                                color=colors["text_secondary"]
                            ),
                        ],
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DONE_ALL,
                        icon_color=colors["text_primary"],
                        tooltip="Marcar todas como leídas",
                        on_click=self.mark_all_as_read
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        
        # Lista de notificaciones
        self.notifications_list = ft.Column(
            controls=self._create_notification_cards(notifications),
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )
        
        # Contenedor principal
        main_content = ft.Column(
            controls=[
                header,
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=15,
                    border_radius=15,
                    content=self.notifications_list if notifications else ft.Container(
                        padding=40,
                        content=ft.Column(
                            controls=[
                                ft.Icon(
                                    ft.Icons.NOTIFICATIONS_NONE,
                                    size=80,
                                    color=colors["text_secondary"]
                                ),
                                ft.Text(
                                    "No tienes notificaciones",
                                    size=18,
                                    color=colors["text_secondary"],
                                    text_align=ft.TextAlign.CENTER
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        )
                    )
                )
            ],
            scroll=ft.ScrollMode.AUTO
        )
        
        self.content = ft.ListView(
            expand=True,
            spacing=0,
            padding=10,
            controls=[main_content]
        )
        
        return self.content
    
    def _create_notification_cards(self, notifications):
        """Crear tarjetas de notificaciones"""
        colors = self.theme_manager.get_theme_colors()
        cards = []
        
        for notification in notifications:
            # Icono según el tipo
            icon, icon_color = self._get_notification_icon(notification.type)
            
            # Tiempo relativo
            time_ago = self._get_time_ago(notification.created_at)
            
            card = ft.Container(
                bgcolor=colors["content_bg"] if notification.is_read else colors["card_bg"],
                padding=15,
                border_radius=10,
                border=ft.border.all(
                    2 if not notification.is_read else 1,
                    ft.Colors.RED_500 if not notification.is_read else colors["divider_color"]
                ),
                content=ft.Row(
                    controls=[
                        # Avatar del usuario
                        ft.Container(
                            content=ft.Image(
                                src=notification.from_user_avatar or "https://i.pravatar.cc/150?img=1",
                                width=50,
                                height=50,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.all(25)
                            ),
                        ),
                        # Contenido
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            notification.from_username,
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=colors["text_primary"]
                                        ),
                                        ft.Icon(icon, size=16, color=icon_color),
                                    ],
                                    spacing=5
                                ),
                                ft.Text(
                                    notification.message,
                                    size=13,
                                    color=colors["text_secondary"]
                                ),
                                ft.Text(
                                    time_ago,
                                    size=11,
                                    color=colors["text_secondary"],
                                    italic=True
                                ),
                            ],
                            spacing=3,
                            expand=True
                        ),
                        # Botones de acción
                        ft.Column(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.CHECK if not notification.is_read else ft.Icons.CHECK_CIRCLE,
                                    icon_size=20,
                                    icon_color=ft.Colors.GREEN_500 if not notification.is_read else colors["text_secondary"],
                                    tooltip="Marcar como leída" if not notification.is_read else "Leída",
                                    on_click=lambda e, nid=notification.id: self.mark_as_read(nid)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_size=20,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Eliminar",
                                    on_click=lambda e, nid=notification.id: self.delete_notification(nid)
                                ),
                            ],
                            spacing=0
                        )
                    ],
                    spacing=10
                ),
                on_click=lambda e, n=notification: self.handle_notification_click(n)
            )
            cards.append(card)
        
        return cards
    
    def _get_notification_icon(self, notification_type):
        """Obtener icono según el tipo de notificación"""
        icons = {
            "like": (ft.Icons.FAVORITE, ft.Colors.RED_500),
            "comment": (ft.Icons.COMMENT, ft.Colors.BLUE_500),
            "follow": (ft.Icons.PERSON_ADD, ft.Colors.GREEN_500),
        }
        return icons.get(notification_type, (ft.Icons.NOTIFICATIONS, ft.Colors.GREY_500))
    
    def _get_time_ago(self, timestamp):
        """Calcular tiempo transcurrido"""
        if not timestamp:
            return "Ahora"
        
        try:
            if isinstance(timestamp, str):
                created = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            else:
                created = timestamp
            
            now = datetime.now()
            diff = now - created
            
            if diff.days > 7:
                return created.strftime("%d/%m/%Y")
            elif diff.days > 0:
                return f"Hace {diff.days} día{'s' if diff.days > 1 else ''}"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"Hace {hours} hora{'s' if hours > 1 else ''}"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"Hace {minutes} minuto{'s' if minutes > 1 else ''}"
            else:
                return "Ahora"
        except:
            return "Hace un momento"
    
    def mark_as_read(self, notification_id):
        """Marcar notificación como leída"""
        if self.db_manager:
            self.db_manager.mark_notification_as_read(notification_id)
            self.refresh_notifications()
    
    def mark_all_as_read(self, e):
        """Marcar todas como leídas"""
        if self.db_manager and self.current_user:
            self.db_manager.mark_all_notifications_as_read(self.current_user.id)
            self.refresh_notifications()
    
    def delete_notification(self, notification_id):
        """Eliminar notificación"""
        if self.db_manager:
            self.db_manager.delete_notification(notification_id)
            self.refresh_notifications()
    
    def refresh_notifications(self):
        """Refrescar lista de notificaciones"""
        if self.db_manager and self.current_user and self.notifications_list:
            notifications = self.db_manager.get_user_notifications(self.current_user.id)
            self.notifications_list.controls = self._create_notification_cards(notifications)
            self.notifications_list.update()
    
    def handle_notification_click(self, notification):
        """Manejar clic en notificación"""
        # Marcar como leída
        if not notification.is_read:
            self.mark_as_read(notification.id)
        
        # Navegar según el tipo
        if notification.type in ["like", "comment"] and notification.post_id:
            # Aquí podrías navegar al post específico
            print(f"Navegando al post {notification.post_id}")
            # Si tienes una función para mostrar un post específico:
            # if self.page_callbacks and "show_post" in self.page_callbacks:
            #     self.page_callbacks["show_post"](notification.post_id)
        elif notification.type == "follow":
            # Navegar al perfil del usuario
            print(f"Navegando al perfil de {notification.from_username}")
            # if self.page_callbacks and "show_user_profile" in self.page_callbacks:
            #     self.page_callbacks["show_user_profile"](notification.from_user_id)
    
    def go_back(self, e):
        """Volver a la página anterior"""
        if self.on_back:
            self.on_back()
    
    def update_theme(self):
        """Actualizar tema"""
        if not self.content:
            return  # Aún no existe la UI
        
        # Solo refrescar si ya está en la página
        if self.content.page:
            self.refresh_notifications()