import flet as ft
from utils.theme_manager import ThemeManager
from components.navigation import NavigationManager
from pages.home_page import HomePage
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.upload_page import UploadPage
from database.models import User

# Try to import database, but handle gracefully if there are issues
try:
    from database.init_db import initialize_database
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"Database import error: {e}")
    DATABASE_AVAILABLE = False

def main(page: ft.Page):
    page.title = "TeamUP"
    page.window_resizable = True
    page.padding = 0
    page.spacing = 0

    # Iniciar la base de datos si está disponible
    db_manager = None
    if DATABASE_AVAILABLE:
        try:
            db_manager = initialize_database()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
            db_manager = None
    
    theme_manager = ThemeManager()
    
    # Paigna default sera el login a menos que haya una cuenta logeada en la db
    current_page = ft.Ref[str]()
    current_page.current = "login" if db_manager else "home"
    current_user = ft.Ref[User]()
    current_user.current = None
    
    # Inicializar las páginas
    home_page = HomePage(theme_manager, db_manager)
    profile_page = ProfilePage(theme_manager, db_manager)
    login_page = None
    registration_page = None
    upload_page = None
    
    # Main content container
    main_content = ft.Container(expand=True)
    
    def handle_login(user: User):
        current_user.current = user
        current_page.current = "home"
        profile_page.set_user(user)
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
        # Registration successful, go to login
        show_login_page()
    
    def show_upload_page(e=None):
        nonlocal upload_page
        if not current_user.current:
            return
            
        previous_page = current_page.current
        current_page.current = "upload"
        
        def upload_callback():
            # Ir a la pagina anterior
            if previous_page == "home":
                show_home_page()
            elif previous_page == "profile":
                show_profile_page()
        
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
        main_content.content = profile_page.create_content()
        update_theme()
        update_navigation()
        page.update()
    
    def update_theme():
        colors = theme_manager.get_theme_colors()
        page.bgcolor = colors["page_bg"]
        phone_screen.bgcolor = colors["phone_bg"]
        
        if current_page.current == "home":
            home_page.update_theme()
        elif current_page.current == "profile":
            profile_page.update_theme()
        elif current_page.current == "login" and login_page:
            login_page.update_theme()
        elif current_page.current == "registration" and registration_page:
            registration_page.update_theme()
        elif current_page.current == "upload" and upload_page:
            upload_page.update_theme()
        
        page.update()
    
    def hide_navigation():
        phone_screen.content.controls[0].visible = False 
        phone_screen.content.controls[2].visible = False 
    
    def update_navigation():
        if current_page.current in ["home", "profile"]:
            # App bar
            phone_screen.content.controls[0] = nav_manager.create_app_bar()
            phone_screen.content.controls[0].visible = True
            
            # bottom bar
            phone_screen.content.controls[2] = nav_manager.update_navigation(page)
            phone_screen.content.controls[2].visible = True
    
    # Devoluciones para las paginas
    page_callbacks = {
        "show_home": show_home_page,
        "show_profile": show_profile_page,
        "show_upload": show_upload_page,
        "update_theme": update_theme,
        "logout": handle_logout
    }
    
    # Inicializar la navegación
    nav_manager = NavigationManager(theme_manager, page_callbacks, current_page)
    
    # Crear los componentes de navegacion
    app_bar = nav_manager.create_app_bar()
    bottom_bar = nav_manager.create_bottom_bar(page)
    
    # Simular una pntalla de telefono
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

    # Centrar la pantalla
    page.add(
        ft.Row(
            controls=[phone_screen],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Inicializar la pagina 
    if db_manager:
        show_login_page()
    else:
        show_home_page()

ft.app(target=main)