import flet as ft
from utils.theme_manager import ThemeManager
from components.navigation import NavigationManager
from pages.home_page import HomePage
from pages.profile_page import ProfilePage
from pages.edit_profile_page import EditProfilePage
from pages.settings_page import SettingsPage
from pages.map_page import MapPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.upload_page import UploadPage
from database.models import User
from pages.notifications_page import NotificationsPage

try:
    from database.init_db import initialize_database
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"Error de importación de base de datos: {e}")
    DATABASE_AVAILABLE = False

def main(page: ft.Page):
    page.title = "TeamUP"
    page.window_resizable = True
    page.padding = 0
    page.spacing = 0

    db_manager = None
    if DATABASE_AVAILABLE:
        try:
            db_manager = initialize_database()
            print("Base de datos inicializada exitosamente")
        except Exception as e:
            print(f"Error de inicialización de base de datos: {e}")
            db_manager = None
    
    theme_manager = ThemeManager()
    
    current_page = ft.Ref[str]()
    current_user = ft.Ref[User]()
    current_user.current = None

    # Determinar página inicial
    def get_initial_page():
        if not db_manager:
            return "home"
        
        # Si hay usuarios, mostrar login. Si no, mostrar registro
        return "login" if db_manager.has_users() else "registration"

    current_page.current = get_initial_page()
    
    home_page = HomePage(theme_manager, db_manager)
    profile_page = ProfilePage(theme_manager, db_manager)
    edit_profile_page = EditProfilePage(theme_manager, db_manager, page)
    settings_page = SettingsPage(theme_manager, db_manager)
    map_page = MapPage(theme_manager, db_manager)
    notifications_page = NotificationsPage(theme_manager, db_manager)
    login_page = None
    registration_page = None
    upload_page = None
    
    main_content = ft.Container(expand=True)
    
    def handle_login(user: User):
        current_user.current = user
        current_page.current = "home"
        profile_page.set_user(user)
        edit_profile_page.set_user(user)
        settings_page.set_user(user)
        show_home_page()
    
    def handle_logout():
        current_user.current = None
        current_page.current = "login" if db_manager else "home"
        if db_manager:
            show_login_page()
        else:
            show_home_page()
    
    def show_login_page():
        nonlocal login_page
        if not db_manager:
            show_home_page()
            return
            
        current_page.current = "login"
        if not login_page:
            login_page = LoginPage(theme_manager, db_manager, handle_login, show_registration_page)
        main_content.content = login_page.create_content()
        update_theme()
        hide_navigation()
        page.update()
    
    def show_registration_page():
        nonlocal registration_page
        if not db_manager:
            show_home_page()
            return
            
        current_page.current = "registration"
        if not registration_page:
            registration_page = RegistrationPage(theme_manager, db_manager, handle_registration, show_login_page)
        main_content.content = registration_page.create_content()
        update_theme()
        hide_navigation()
        page.update()
    
    def handle_registration(user: User):
        show_login_page()
    
    def show_edit_profile_page(e=None):
        nonlocal edit_profile_page
        if not current_user.current:
            return
        
        previous_page = current_page.current
        current_page.current = "edit_profile"
        
        def go_back():
            if previous_page == "profile":
                show_profile_page()
            else:
                show_home_page()
        
        edit_profile_page.on_back = go_back
        main_content.content = edit_profile_page.create_content()
        update_theme()
        hide_navigation()
        page.update()
    
    def show_settings_page(e=None):
        nonlocal settings_page
        if not current_user.current:
            return
        
        previous_page = current_page.current
        current_page.current = "settings"
        
        def go_back():
            if previous_page == "profile":
                show_profile_page()
            else:
                show_home_page()
        
        settings_page.on_back = go_back
        main_content.content = settings_page.create_content()
        update_theme()
        hide_navigation()
        page.update()
    
    def show_upload_page(e=None):
        nonlocal upload_page
        if not current_user.current:
            return
            
        previous_page = current_page.current
        current_page.current = "upload"
        
        def upload_callback():
            if previous_page == "home":
                show_home_page()
            elif previous_page == "profile":
                show_profile_page()
            elif previous_page == "map":
                show_map_page()
        
        if not upload_page:
            upload_page = UploadPage(theme_manager, db_manager, current_user, upload_callback)
        else:
            upload_page.upload_callback = upload_callback
        
        main_content.content = upload_page.create_content()
        update_theme()
        hide_navigation()
        page.update()
    
    def show_home_page(e=None):
        current_page.current = "home"
        main_content.content = home_page.create_content()
        update_theme()
        update_navigation()
        page.update()
    
    def show_profile_page(e=None):
        current_page.current = "profile"
        profile_page.page_callbacks = page_callbacks
        main_content.content = profile_page.create_content()
        update_theme()
        update_navigation()
        page.update()
    
    def show_map_page(e=None):
        current_page.current = "map"
        map_page.on_back = show_home_page
        main_content.content = map_page.create_content()
        update_theme()
        update_navigation()
        page.update()
    
    def show_notifications_page(e=None):
        if not current_user.current:
            return
        
        previous_page = current_page.current
        current_page.current = "notifications"
        
        def go_back():
            if previous_page == "home":
                show_home_page()
            elif previous_page == "profile":
                show_profile_page()
            elif previous_page == "map":
                show_map_page()
            else:
                show_home_page()
        
        notifications_page.set_user(current_user.current)
        notifications_page.on_back = go_back
        notifications_page.page_callbacks = page_callbacks
        main_content.content = notifications_page.create_content()
        update_theme()
        hide_navigation()
        page.update()
    
    def update_theme():
        colors = theme_manager.get_theme_colors()
        page.bgcolor = colors["page_bg"]
        phone_screen.bgcolor = colors["phone_bg"]
        
        if current_page.current == "home":
            home_page.update_theme()
        elif current_page.current == "profile":
            profile_page.update_theme()
        elif current_page.current == "edit_profile":
            edit_profile_page.update_theme()
        elif current_page.current == "settings":
            settings_page.update_theme()
        elif current_page.current == "map":
            map_page.update_theme()
        elif current_page.current == "login" and login_page:
            login_page.update_theme()
        elif current_page.current == "registration" and registration_page:
            registration_page.update_theme()
        elif current_page.current == "upload" and upload_page:
            upload_page.update_theme()
        elif current_page.current == "notifications":
            notifications_page.update_theme()
        
        page.update()
    
    def hide_navigation():
        phone_screen.content.controls[0].visible = False
        phone_screen.content.controls[2].visible = False
    
    def update_navigation():
        if current_page.current in ["home", "profile", "map"]:
            phone_screen.content.controls[0] = nav_manager.create_app_bar()
            phone_screen.content.controls[0].visible = True
            
            phone_screen.content.controls[2] = nav_manager.update_navigation(page)
            phone_screen.content.controls[2].visible = True
    
    page_callbacks = {
        "show_home": show_home_page,
        "show_profile": show_profile_page,
        "show_map": show_map_page,
        "show_upload": show_upload_page,
        "show_notifications": show_notifications_page,
        "show_edit_profile": show_edit_profile_page,
        "show_settings": show_settings_page,
        "update_theme": update_theme,
        "logout": handle_logout
    }
    
    nav_manager = NavigationManager(theme_manager, page_callbacks, current_page)


    nav_manager = NavigationManager(theme_manager, page_callbacks, current_page)

    # Agregar método para obtener notificaciones no leídas
    def get_unread_count():
        if current_user.current and db_manager:
            return db_manager.get_unread_notifications_count(current_user.current.id)
        return 0

    nav_manager.get_unread_count = get_unread_count
    
    app_bar = nav_manager.create_app_bar()
    bottom_bar = nav_manager.create_bottom_bar(page)
    
    phone_screen = ft.Container(
        width=375,
        height=667,
        bgcolor=ft.Colors.GREY_900,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK12, spread_radius=1),
        content=ft.Column(
            controls=[
                app_bar,
                main_content,
                bottom_bar,
            ],
            spacing=0,
        )
    )

    page.add(
        ft.Row(
            controls=[phone_screen],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    if db_manager:
        show_login_page()
    else:
        show_home_page()

ft.app(target=main)
