import flet as ft

class NavigationManager:
    def __init__(self, theme_manager, page_callbacks, current_page_ref):
        self.theme_manager = theme_manager
        self.page_callbacks = page_callbacks
        self.current_page_ref = current_page_ref
    
    def create_app_bar(self):
        return ft.Container(
            height=56,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.RED_500, ft.Colors.RED_400]
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=10),
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "TeamUP",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        padding=ft.padding.only(left=5),
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(ft.Icons.SEND_ROUNDED, icon_color=ft.Colors.WHITE),
                    ft.IconButton(
                        ft.Icons.ACCOUNT_CIRCLE, 
                        icon_color=ft.Colors.WHITE,
                        on_click=self.page_callbacks["show_profile"],
                        visible=self.current_page_ref.current != "profile"  # Hide on profile page
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    
    def create_bottom_bar(self, page):
        # Create conditional buttons based on current page
        controls = []
        
        # Menu button (always visible)
        controls.append(
            ft.IconButton(
                icon=ft.Icons.MENU, 
                icon_color=ft.Colors.WHITE,
                on_click=lambda e: self.show_menu_options(e, page)
            )
        )
        
        # Spacer
        controls.append(ft.Container(expand=True))
        
        # Home button (visible when not on home page)
        if self.current_page_ref.current != "home":
            controls.append(
                ft.IconButton(
                    icon=ft.Icons.HOME, 
                    icon_color=ft.Colors.WHITE,
                    on_click=self.page_callbacks["show_home"]
                )
            )
        
        # Upload button (visible on home and profile pages)
        if self.current_page_ref.current in ["home", "profile"]:
            controls.append(
                ft.IconButton(
                    icon=ft.Icons.ADD_CIRCLE, 
                    icon_color=ft.Colors.WHITE,
                    on_click=self.page_callbacks.get("show_upload", lambda e: None),
                    tooltip="Crear Post"
                )
            )
        
        # Search button
        controls.append(
            ft.IconButton(
                icon=ft.Icons.SEARCH, 
                icon_color=ft.Colors.WHITE
            )
        )
        
        # Favorites button
        controls.append(
            ft.IconButton(
                icon=ft.Icons.FAVORITE, 
                icon_color=ft.Colors.WHITE
            )
        )
        
        return ft.Container(
            height=60,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.RED_500, ft.Colors.RED_400]
            ),
            padding=ft.padding.symmetric(horizontal=10),
            content=ft.Row(
                controls=controls,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    
    def update_navigation(self, page):
        """Update navigation visibility based on current page"""
        return self.create_bottom_bar(page)
    
    def show_menu_options(self, e, page):
        colors = self.theme_manager.get_theme_colors()
        
        def close_menu(e):
            page.close(menu_sheet)
        
        def toggle_and_close(e):
            self.theme_manager.toggle_theme()
            self.page_callbacks["update_theme"]()
            close_menu(e)

        menu_sheet = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                bgcolor=colors["card_bg"],
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Menu", 
                            size=20, 
                            weight=ft.FontWeight.BOLD,
                            color=colors["text_primary"]
                        ),
                        ft.Divider(color=colors["divider_color"]),
                        
                        # Estadisticas 
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.BAR_CHART_ROUNDED, color=colors["icon_color"]),
                            title=ft.Text("Estadisticas", color=colors["text_primary"]),
                            subtitle=ft.Text("Ver tus estadisticas de juego", color=colors["text_secondary"]),
                            on_click=close_menu
                        ),
                        
                        # Mapa
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.MAP_ROUNDED, color=colors["icon_color"]),
                            title=ft.Text("Mapa de entrenamiento", color=colors["text_primary"]),
                            subtitle=ft.Text("Encuentra lugares donde practicar tu deporte", color=colors["text_secondary"]),
                            on_click=close_menu
                        ),
                        
                        ft.Divider(color=colors["divider_color"]),
                        
                        # Cmabiar de modo
                        ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.DARK_MODE if not self.theme_manager.is_dark_mode else ft.Icons.LIGHT_MODE,
                                color=colors["icon_color"]
                            ),
                            title=ft.Text(
                                f"Cambiar a {'Dark' if not self.theme_manager.is_dark_mode else 'Light'} Mode",
                                color=colors["text_primary"]
                            ),
                            on_click=toggle_and_close
                        ),
                        
                        # Cerrar sesion
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOGOUT, color=colors["icon_color"]),
                            title=ft.Text("Cerrar sesion", color=colors["text_primary"]),
                            on_click=lambda e: [self.page_callbacks.get("logout", lambda: None)(), close_menu(e)]
                        ),
                        
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS, color=colors["icon_color"]),
                            title=ft.Text("Configuracion", color=colors["text_primary"]),
                            on_click=close_menu
                        ),
                        
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.HELP, color=colors["icon_color"]),
                            title=ft.Text("Ayuda y soporte", color=colors["text_primary"]),
                            on_click=close_menu
                        ),
                        
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.INFO, color=colors["icon_color"]),
                            title=ft.Text("Acerca de TeamUP", color=colors["text_primary"]),
                            on_click=close_menu
                        ),
                        
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Cerrar",
                            on_click=close_menu,
                            width=200,
                            bgcolor=ft.Colors.RED_500,
                            color=ft.Colors.WHITE
                        )
                    ],
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                height=500
            )
        )
        page.open(menu_sheet)