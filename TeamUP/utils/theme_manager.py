import flet as ft

class ThemeManager:
    def __init__(self):
        self.is_dark_mode = True
    
    def get_theme_colors(self):
        if self.is_dark_mode:
            return {
                "page_bg": ft.Colors.BLACK,
                "phone_bg": ft.Colors.GREY_900,
                "content_bg": ft.Colors.GREY_800,
                "text_primary": ft.Colors.WHITE,
                "text_secondary": ft.Colors.GREY_300,
                "icon_color": ft.Colors.WHITE,
                "divider_color": ft.Colors.GREY_600,
                "card_bg": ft.Colors.GREY_800
            }
        else:
            return {
                "page_bg": ft.Colors.GREY_100,
                "phone_bg": ft.Colors.WHITE,
                "content_bg": ft.Colors.WHITE,
                "text_primary": ft.Colors.BLACK,
                "text_secondary": ft.Colors.GREY_700,
                "icon_color": ft.Colors.GREY_800,
                "divider_color": ft.Colors.GREY_300,
                "card_bg": ft.Colors.GREY_200
            }
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        return self.get_theme_colors()