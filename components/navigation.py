import flet as ft
from utils.theme_manager import ThemeManager

class NavigationManager:
    def __init__(self, theme_manager: ThemeManager, page_callbacks: dict, current_page):
        self.theme_manager = theme_manager
        self.page_callbacks = page_callbacks
        self.current_page = current_page
        self.nav_bar = None

    def create_app_bar(self):
        colors = self.theme_manager.get_theme_colors()
        
        return ft.Container(
            bgcolor=colors["card_bg"],
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.MENU,
                        icon_color=colors["text_primary"],
                        on_click=self.show_menu,
                        tooltip="Menú"
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "TeamUP",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=colors["text_primary"]
                            ),
                            ft.Text(
                                "Entrena con tu comunidad",
                                size=12,
                                color=colors["text_secondary"]
                            ),
                        ],
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS,
                        icon_color=colors["text_primary"],
                        tooltip="Notificaciones",
                        on_click=self.show_notifications  
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def create_bottom_bar(self, page):
        colors = self.theme_manager.get_theme_colors()
        
        self.nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME,
                    label="Inicio"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.ADD_A_PHOTO,
                    label="Subir"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON,
                    label="Perfil"
                ),
            ],
            bgcolor=colors["card_bg"],
            indicator_color=ft.Colors.RED_500,
            on_change=self.on_nav_change
        )
        
        return ft.Container(
            bgcolor=colors["card_bg"],
            content=self.nav_bar
        )

    def on_nav_change(self, e):
        selected_index = self.nav_bar.selected_index
        
        if selected_index == 0:
            self.page_callbacks["show_home"]()
        elif selected_index == 1:
            self.page_callbacks["show_upload"]()
        elif selected_index == 2:
            self.page_callbacks["show_profile"]()

    def show_menu(self, e):
        colors = self.theme_manager.get_theme_colors()

        page = e.page

        def close_menu(ev=None):
            menu_modal.open = False
            page.update()

        menu_items = [
            ("Inicio", ft.Icons.HOME, "show_home"),
            ("Perfil", ft.Icons.PERSON, "show_profile"),
            ("Mapa de entrenamiento", ft.Icons.MAP, "show_map"),
            ("Tema oscuro", ft.Icons.DARK_MODE, "toggle_theme"),
            ("Cerrar sesión", ft.Icons.LOGOUT, "logout"),
        ]

        def make_handler(callback_key):
            def handler(ev):
                close_menu()

                if callback_key == "toggle_theme":
                    self.theme_manager.toggle_theme()
                    if "update_theme" in self.page_callbacks:
                        self.page_callbacks["update_theme"]()
                    return

                if callback_key in self.page_callbacks:
                    self.page_callbacks[callback_key]()
            return handler

        # BOTÓN X DE CIERRE
        close_button = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=colors["text_primary"],
                    on_click=close_menu
                )
            ],
            alignment=ft.MainAxisAlignment.END
        )

        menu_controls = [close_button]

        for label, icon, callback_key in menu_items:
            menu_controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon, color=colors["text_primary"], size=24),
                            ft.Text(label, color=colors["text_primary"], size=16),
                        ],
                        spacing=15
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                    on_click=make_handler(callback_key),
                )
            )

        menu_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Menú", color=colors["text_primary"]),
            content=ft.Column(controls=menu_controls, scroll=ft.ScrollMode.AUTO),
            bgcolor=colors["content_bg"],
        )

        page.overlay.append(menu_modal)
        menu_modal.open = True
        page.update()


    

    def handle_menu_click(self, callback_key):
        if callback_key == "toggle_theme":
            self.theme_manager.toggle_theme()
            self.page_callbacks["update_theme"]()
        elif callback_key in self.page_callbacks:
            self.page_callbacks[callback_key]()

    def update_navigation(self, page):
        """Actualizar la barra de navegación según la página actual"""
        if self.nav_bar:
            if self.current_page.current == "home":
                self.nav_bar.selected_index = 0
            elif self.current_page.current == "upload":
                self.nav_bar.selected_index = 1
            elif self.current_page.current == "profile":
                self.nav_bar.selected_index = 2
        
        return ft.Container(
            bgcolor=self.theme_manager.get_theme_colors()["card_bg"],
            content=self.nav_bar
        )
    def show_notifications(self, e):
        """Mostrar página de notificaciones"""
        if "show_notifications" in self.page_callbacks:
            self.page_callbacks["show_notifications"]()
