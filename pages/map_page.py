import flet as ft
import json
import webbrowser
import urllib.parse
from typing import List, Dict, Any
from database.map_data import MapDataManager

class MapPage:
    def __init__(self, theme_manager, db_manager=None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.content = None
        self.map_data_manager = MapDataManager()
        self.on_back = None
        
        # Estado del mapa
        self.current_filter = "todos"
        self.search_query = ""
        self.selected_location = None
        
        # Coordenadas de Buenos Aires
        self.buenos_aires_center = {"lat": -34.6118, "lng": -58.3960}
        
        # Controles de UI
        self.search_field = ft.TextField()
        self.filter_dropdown = ft.Dropdown()
        self.locations_list = ft.Column()
        self.map_container = ft.Container()
        
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        # Campo de búsqueda
        self.search_field = ft.TextField(
            label="Buscar lugares deportivos...",
            width=200,                 # antes 300
            prefix_icon=ft.Icons.SEARCH,
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            on_change=self.on_search_change
        )

        # Filtro por categoría
        self.filter_dropdown = ft.Dropdown(
            label="Categoría",
            width=120,                 # antes 150
            color=colors["text_primary"],
            border_color=colors["divider_color"],
            options=[
                ft.dropdown.Option("todos", "Todos"),
                ft.dropdown.Option("clubes", "Clubes"),
                ft.dropdown.Option("eventos", "Eventos"),
                ft.dropdown.Option("parques", "Parques"),
                ft.dropdown.Option("gimnasios", "Gimnasios"),
                ft.dropdown.Option("piscinas", "Piscinas"),
                ft.dropdown.Option("canchas", "Canchas"),
            ],
            value="todos",
            on_change=self.on_filter_change
        )

        
        # Filtros por deporte específico
        sport_filters = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Fútbol",
                    icon=ft.Icons.SPORTS_SOCCER,
                    bgcolor=colors["card_bg"],
                    color=colors["text_primary"],
                    on_click=lambda e: self.filter_by_sport("futbol")
                ),
                ft.ElevatedButton(
                    "Básquet",
                    icon=ft.Icons.SPORTS_BASKETBALL,
                    bgcolor=colors["card_bg"],
                    color=colors["text_primary"],
                    on_click=lambda e: self.filter_by_sport("basquet")
                ),
                ft.ElevatedButton(
                    "Vóley",
                    icon=ft.Icons.SPORTS_VOLLEYBALL,
                    bgcolor=colors["card_bg"],
                    color=colors["text_primary"],
                    on_click=lambda e: self.filter_by_sport("voley")
                ),
                ft.ElevatedButton(
                    "Running",
                    icon=ft.Icons.DIRECTIONS_RUN,
                    bgcolor=colors["card_bg"],
                    color=colors["text_primary"],
                    on_click=lambda e: self.filter_by_sport("running")
                ),
            ],
            wrap=True,
            spacing=10
        )
        
        # Simulación del mapa (ya que Flet no tiene mapa nativo)
        self.map_container = ft.Container(
            width=350,
            height=300,
            bgcolor=colors["card_bg"],
            border_radius=10,
            border=ft.border.all(1, colors["divider_color"]),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "🗺️ Mapa de Buenos Aires",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=colors["text_primary"]
                    ),
                    ft.Text(
                        "Centrado en: Palermo, CABA",
                        size=12,
                        color=colors["text_secondary"]
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "📍 Puntos de interés encontrados:",
                        size=14,
                        color=colors["text_primary"]
                    ),
                    self._create_map_points_preview()
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        
        # Lista de ubicaciones
        self.locations_list = ft.Column(
            controls=self._create_location_cards(),
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )
        
        map_content = ft.Column(
            controls=[
                # Encabezado con botón de regreso
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=20,
                    margin=ft.margin.only(bottom=10),
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK,
                                        icon_color=colors["text_primary"],
                                        tooltip="Volver al inicio",
                                        on_click=self.go_back_to_home
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Mapa de Entrenamiento",
                                                size=28,
                                                weight=ft.FontWeight.BOLD,
                                                color=colors["text_primary"]
                                            ),
                                            ft.Text(
                                                "Descubre lugares deportivos en Buenos Aires",
                                                size=16,
                                                color=colors["text_secondary"]
                                            ),
                                        ],
                                        expand=True
                                    )
                                ]
                            )
                        ]
                    )
                ),
                
                # Controles de búsqueda y filtros
               ft.Container(
                        bgcolor=colors["card_bg"],
                        padding=15,
                        margin=ft.margin.only(bottom=10),
                        border_radius=15,
                        content=ft.Column(
                            controls=[
                                # Búsqueda + categorías
                                ft.Row(
                                    controls=[self.search_field, self.filter_dropdown],
                                    alignment=ft.MainAxisAlignment.CENTER,
                            
                                    wrap=True
                                ),

                                ft.Container(height=12),

                                # Filtros deportivos acomodados y centrados
                                ft.Container(
                                    content=ft.Row(
                                        controls=sport_filters.controls,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                       
                                        wrap=True
                                    )
                                ),
                            ]
                        )
                    ),

                
                # Mapa simulado
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=15,
                    margin=ft.margin.only(bottom=10),
                    border_radius=15,
                    content=self.map_container
                ),
                
                # Lista de ubicaciones
                ft.Container(
                    bgcolor=colors["card_bg"],
                    padding=15,
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Lugares encontrados",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=colors["text_primary"]
                            ),
                            ft.Container(height=10),
                            self.locations_list
                        ]
                    )
                ),
            ],
            scroll=ft.ScrollMode.AUTO
        )
        
        self.content = ft.ListView(
            expand=True,
            spacing=0,
            padding=10,
            controls=[map_content]
        )
        
        return self.content
    
    def go_back_to_home(self, e):
        """Regresar a la página de inicio"""
        if self.on_back:
            self.on_back()
        else:
            print("Callback de navegación no configurado")
        
    def _create_map_points_preview(self):
        """Crear vista previa de puntos en el mapa"""
        colors = self.theme_manager.get_theme_colors()
        locations = self.map_data_manager.get_filtered_locations(self.current_filter, self.search_query)
        
        if not locations:
            return ft.Text("No se encontraron ubicaciones", color=colors["text_secondary"])
        
        points = []
        for i, location in enumerate(locations[:]):  
            points.append(
                ft.Container(
                    width=30,
                    height=30,
                    bgcolor=self._get_category_color(location["category"]),
                    border_radius=15,
                    content=ft.Text(
                        str(i + 1),
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    tooltip=location["name"]
                )
            )
        
        return ft.Row(
            controls=points,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
        )
    
    def _create_location_cards(self):
        """Crear tarjetas de ubicaciones"""
        colors = self.theme_manager.get_theme_colors()
        locations = self.map_data_manager.get_filtered_locations(self.current_filter, self.search_query)
        
        if not locations:
            return [ft.Text("No se encontraron ubicaciones", color=colors["text_secondary"])]
        
        cards = []
        for location in locations:
            card = ft.Container(
                bgcolor=colors["content_bg"],
                padding=15,
                border_radius=10,
                border=ft.border.all(1, colors["divider_color"]),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    self._get_category_icon(location["category"]),
                                    color=self._get_category_color(location["category"]),
                                    size=24
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            location["name"],
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=colors["text_primary"]
                                        ),
                                        ft.Text(
                                            location["address"],
                                            size=12,
                                            color=colors["text_secondary"]
                                        ),
                                    ],
                                    expand=True
                                ),
                                ft.Container(
                                    bgcolor=self._get_category_color(location["category"]),
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=12,
                                    content=ft.Text(
                                        location["category"].title(),
                                        size=10,
                                        color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.BOLD
                                    )
                                )
                            ]
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            location["description"],
                            size=12,
                            color=colors["text_primary"]
                        ),
                        ft.Container(height=8),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"⭐ {location['rating']}/5",
                                    size=12,
                                    color=colors["text_secondary"]
                                ),
                                ft.Text(
                                    f"📍 {location['distance']}",
                                    size=12,
                                    color=colors["text_secondary"]
                                ),
                                ft.Text(
                                    f"💰 {location['price_range']}",
                                    size=12,
                                    color=colors["text_secondary"]
                                ),
                            ],
                            spacing=15
                        ),
                        ft.Container(height=8),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Ver detalles",
                                    bgcolor=ft.Colors.RED_500,
                                    color=ft.Colors.WHITE,
                                    on_click=lambda e, loc=location: self.show_location_details(loc)
                                ),
                                ft.ElevatedButton(
                                    "Cómo llegar",
                                    bgcolor=colors["card_bg"],
                                    color=colors["text_primary"],
                                    icon=ft.Icons.DIRECTIONS,
                                    on_click=lambda e, loc=location: self.show_directions(loc)
                                ),
                            ],
                            spacing=10
                        )
                    ]
                )
            )
            cards.append(card)
        
        return cards
    
    def _get_category_icon(self, category):
        """Obtener icono según la categoría"""
        icons = {
            "clubes": ft.Icons.SPORTS,
            "eventos": ft.Icons.EVENT,
            "parques": ft.Icons.PARK,
            "gimnasios": ft.Icons.FITNESS_CENTER,
            "piscinas": ft.Icons.POOL,
            "canchas": ft.Icons.SPORTS_TENNIS,
        }
        return icons.get(category, ft.Icons.PLACE)
    
    def _get_category_color(self, category):
        """Obtener color según la categoría"""
        colors = {
            "clubes": ft.Colors.BLUE_500,
            "eventos": ft.Colors.ORANGE_500,
            "parques": ft.Colors.GREEN_500,
            "gimnasios": ft.Colors.PURPLE_500,
            "piscinas": ft.Colors.CYAN_500,
            "canchas": ft.Colors.RED_500,
        }
        return colors.get(category, ft.Colors.GREY_500)
    
    def on_search_change(self, e):
        """Manejar cambio en búsqueda"""
        self.search_query = e.control.value
        self.refresh_locations()
    
    def on_filter_change(self, e):
        """Manejar cambio en filtro"""
        self.current_filter = e.control.value
        self.refresh_locations()
    
    def filter_by_sport(self, sport):
        """Filtrar por deporte específico"""
        self.search_query = sport
        self.search_field.value = sport
        self.search_field.update()
        self.refresh_locations()
    
    def refresh_locations(self):
        """Refrescar lista de ubicaciones"""
        if self.locations_list:
            self.locations_list.controls = self._create_location_cards()
            self.locations_list.update()
        
        if self.map_container:
            # Actualizar vista previa del mapa
            map_content = self.map_container.content
            if isinstance(map_content, ft.Column) and len(map_content.controls) > 4:
                map_content.controls[4] = self._create_map_points_preview()
                self.map_container.update()
    
    def show_location_details(self, location):
        """Mostrar detalles de una ubicación - abrir sitio web""" 
        # Obtener la URL del sitio web
        website = location.get('website', '')
        name = location.get('name', '')
        
        if website:
            try:
                webbrowser.open(website)
                print(f"Abriendo sitio web de: {name}")
            except Exception as e:
                print(f"Error al abrir el sitio web: {e}")
        else:
            # Si no tiene sitio web, buscar en Google
            import urllib.parse
            search_query = urllib.parse.quote(f"{name} sitio oficial")
            google_search = f"https://www.google.com/search?q={search_query}"
            try:
                webbrowser.open(google_search)
                print(f"Buscando en Google: {name}")
            except Exception as e:
                print(f"Error al buscar en Google: {e}")
    
    def show_directions(self, location):
        """Mostrar direcciones a una ubicación en Google Maps"""
        # Obtener la dirección completa
        address = location.get('address', '')
        name = location.get('name', '')
        
        # Si hay coordenadas, usarlas
        if 'coordinates' in location and location['coordinates']:
            lat = location['coordinates'].get('lat')
            lng = location['coordinates'].get('lng')
            
            if lat and lng:
                # URL con coordenadas específicas
                maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"
            else:
                # URL con dirección
                destination = urllib.parse.quote(f"{name}, {address}")
                maps_url = f"https://www.google.com/maps/dir/?api=1&destination={destination}"
        else:
            # URL con dirección
            destination = urllib.parse.quote(f"{name}, {address}")
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={destination}"
        
        # Abrir en el navegador
        try:
            webbrowser.open(maps_url)
            print(f"Abriendo direcciones a: {location['name']}")
        except Exception as e:
            print(f"Error al abrir Google Maps: {e}")
    
    def update_theme(self):
        """Actualizar tema"""
        if not self.content:
            return  # Aún no existe la UI, no tocar nada

        colors = self.theme_manager.get_theme_colors()

        # Actualizar campos existentes solo si están en la página
        if self.search_field and self.search_field.page:
            self.search_field.color = colors["text_primary"]
            self.search_field.border_color = colors["divider_color"]
            self.search_field.update()

        if self.filter_dropdown and self.filter_dropdown.page:
            self.filter_dropdown.color = colors["text_primary"]
            self.filter_dropdown.border_color = colors["divider_color"]
            self.filter_dropdown.update()

        # Actualizar map_container
        if self.map_container and self.map_container.page:
            self.map_container.bgcolor = colors["card_bg"]
            self.map_container.border = ft.border.all(1, colors["divider_color"])
            self.map_container.update()

        # Actualizar lista de ubicaciones
        if self.locations_list and self.locations_list.page:
            self.refresh_locations()

        if self.content.page:
            self.content.update()

