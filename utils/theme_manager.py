import flet as ft

class ThemeManager:
    def __init__(self):
        self.is_dark_mode = True
        self.themes = {
            "light": {
                "page_bg": ft.Colors.WHITE,
                "phone_bg": "#F5F5F5",
                "content_bg": "#F5F5F5",
                "card_bg": ft.Colors.WHITE,
                "text_primary": ft.Colors.BLACK,
                "text_secondary": ft.Colors.GREY_700,
                "icon_color": ft.Colors.BLACK,
                "divider_color": ft.Colors.GREY_300,
            },
            "dark": {
                "page_bg": "#121212",
                "phone_bg": "#1E1E1E",
                "content_bg": "#1E1E1E",
                "card_bg": "#2C2C2C",
                "text_primary": ft.Colors.WHITE,
                "text_secondary": ft.Colors.GREY_400,
                "icon_color": ft.Colors.WHITE,
                "divider_color": ft.Colors.GREY_700,
            }
        }
    
    def toggle_theme(self):
        """Alternar entre tema oscuro y claro"""
        self.is_dark_mode = not self.is_dark_mode
    
    def toggle_dark_mode(self):
        """Alias para toggle_theme para compatibilidad"""
        self.toggle_theme()
    
    def get_theme_colors(self):
        """Obtener colores del tema actual"""
        return self.themes["dark" if self.is_dark_mode else "light"]
    
    def get_current_theme(self):
        """Obtener nombre del tema actual"""
        return "dark" if self.is_dark_mode else "light"
