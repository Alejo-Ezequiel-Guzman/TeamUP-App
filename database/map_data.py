from typing import List, Dict, Any

class MapDataManager:
    def __init__(self):
        self.locations_data = self._load_buenos_aires_locations()
    
    def _load_buenos_aires_locations(self) -> List[Dict[str, Any]]:
        """Cargar datos de ubicaciones deportivas de Buenos Aires"""
        return [
            # Clubes de Fútbol
            {
                "id": 1,
                "name": "Club Atlético Boca Juniors",
                "category": "clubes",
                "sports": ["futbol"],
                "address": "Brandsen 805, La Boca, CABA",
                "coordinates": {"lat": -34.6354, "lng": -58.3647},
                "description": "Estadio Alberto J. Armando, hogar del Club Atlético Boca Juniors",
                "rating": 4.8,
                "distance": "8.5 km",
                "price_range": "$$",
                "contact": "+54 11 4309-4700",
                "website": "www.bocajuniors.com.ar"
            },
            {
                "id": 2,
                "name": "Club Atlético River Plate",
                "category": "clubes",
                "sports": ["futbol"],
                "address": "Av. Pres. Figueroa Alcorta 7597, Núñez, CABA",
                "coordinates": {"lat": -34.5453, "lng": -58.4498},
                "description": "Estadio Monumental, casa del Club Atlético River Plate",
                "rating": 4.9,
                "distance": "12.3 km",
                "price_range": "$$",
                "contact": "+54 11 4789-1200",
                "website": "www.cariverplate.com.ar"
            },
            
            # Clubes de Básquet
            {
                "id": 3,
                "name": "Club Atlético San Lorenzo",
                "category": "clubes",
                "sports": ["basquet", "futbol"],
                "address": "Av. La Plata 1782, Boedo, CABA",
                "coordinates": {"lat": -34.6292, "lng": -58.4186},
                "description": "Club con excelentes instalaciones para básquet y otros deportes",
                "rating": 4.6,
                "distance": "5.2 km",
                "price_range": "$",
                "contact": "+54 11 4932-3500",
                "website": "www.sanlorenzo.com.ar"
            },
            {
                "id": 4,
                "name": "Club Ferro Carril Oeste",
                "category": "clubes",
                "sports": ["basquet", "voley", "natacion"],
                "address": "Av. Avellaneda 1240, Caballito, CABA",
                "coordinates": {"lat": -34.6158, "lng": -58.4370},
                "description": "Club histórico con múltiples disciplinas deportivas",
                "rating": 4.4,
                "distance": "3.8 km",
                "price_range": "$",
                "contact": "+54 11 4958-7400",
                "website": "www.ferro.org.ar"
            },
            
            # Eventos Deportivos
            {
                "id": 5,
                "name": "3F Corre Aventura - Tres de Febrero",
                "category": "eventos",
                "sports": ["running", "atletismo"],
                "address": "Parque de la Ribera, Tres de Febrero, Buenos Aires",
                "coordinates": {"lat": -34.5892, "lng": -58.5647},
                "description": "Evento de running organizado por la Municipalidad de Tres de Febrero",
                "rating": 4.7,
                "distance": "15.2 km",
                "price_range": "Gratis",
                "contact": "+54 11 4756-9200",
                "website": "www.tresdefebrero.gov.ar",
                "event_date": "Próximo evento: 15 de Abril 2024",
                "event_details": "Distancias: 5K, 10K y 21K"
            },
            {
                "id": 6,
                "name": "Maratón Internacional de Buenos Aires",
                "category": "eventos",
                "sports": ["running", "atletismo"],
                "address": "Largada: Av. 9 de Julio y Av. de Mayo, CABA",
                "coordinates": {"lat": -34.6037, "lng": -58.3816},
                "description": "Maratón internacional que recorre los principales puntos de la ciudad",
                "rating": 4.9,
                "distance": "2.1 km",
                "price_range": "$$",
                "contact": "+54 11 4000-0000",
                "website": "www.maratonbuenosaires.com",
                "event_date": "Próximo evento: 22 de Septiembre 2024",
                "event_details": "42K, 21K, 10K y 5K"
            },
            
            # Parques y Espacios Públicos
            {
                "id": 7,
                "name": "Parque Tres de Febrero (Bosques de Palermo)",
                "category": "parques",
                "sports": ["running", "ciclismo", "yoga"],
                "address": "Av. del Libertador, Palermo, CABA",
                "coordinates": {"lat": -34.5755, "lng": -58.4115},
                "description": "Amplio parque ideal para running, ciclismo y actividades al aire libre",
                "rating": 4.8,
                "distance": "4.5 km",
                "price_range": "Gratis",
                "facilities": ["Pista de running", "Ciclovía", "Espacios verdes"]
            },
            {
                "id": 8,
                "name": "Reserva Ecológica Costanera Sur",
                "category": "parques",
                "sports": ["running", "ciclismo", "caminata"],
                "address": "Av. Tristán Achával Rodríguez 1550, Puerto Madero, CABA",
                "coordinates": {"lat": -34.6158, "lng": -58.3515},
                "description": "Reserva natural con senderos para running y ciclismo",
                "rating": 4.6,
                "distance": "6.8 km",
                "price_range": "Gratis",
                "facilities": ["Senderos", "Miradores", "Área de picnic"]
            },
            
            # Gimnasios
            {
                "id": 9,
                "name": "Megatlon Palermo",
                "category": "gimnasios",
                "sports": ["fitness", "natacion", "crossfit"],
                "address": "Av. Santa Fe 4820, Palermo, CABA",
                "coordinates": {"lat": -34.5889, "lng": -58.4203},
                "description": "Gimnasio completo con piscina, clases grupales y equipamiento moderno",
                "rating": 4.3,
                "distance": "2.8 km",
                "price_range": "$$$",
                "contact": "+54 11 4831-2000",
                "facilities": ["Piscina", "Sauna", "Clases grupales", "Musculación"]
            },
            {
                "id": 10,
                "name": "SportClub Belgrano",
                "category": "gimnasios",
                "sports": ["fitness", "spinning", "pilates"],
                "address": "Av. Cabildo 2280, Belgrano, CABA",
                "coordinates": {"lat": -34.5633, "lng": -58.4553},
                "description": "Centro de fitness con variedad de clases y entrenamiento personalizado",
                "rating": 4.2,
                "distance": "8.1 km",
                "price_range": "$$",
                "contact": "+54 11 4784-5600",
                "facilities": ["Spinning", "Pilates", "Yoga", "Funcional"]
            },
            
            # Canchas de Vóley
            {
                "id": 11,
                "name": "Club Ciudad de Buenos Aires",
                "category": "clubes",
                "sports": ["voley", "tenis", "natacion"],
                "address": "Av. Costanera Rafael Obligado s/n, Núñez, CABA",
                "coordinates": {"lat": -34.5389, "lng": -58.4647},
                "description": "Club con excelentes canchas de vóley y vista al río",
                "rating": 4.5,
                "distance": "11.2 km",
                "price_range": "$$",
                "contact": "+54 11 4784-1213",
                "facilities": ["Canchas de vóley", "Piscina", "Tenis", "Paddle"]
            },
            {
                "id": 12,
                "name": "Polideportivo Parque Chacabuco",
                "category": "canchas",
                "sports": ["voley", "basquet", "futsal"],
                "address": "Av. Asamblea 1301, Parque Chacabuco, CABA",
                "coordinates": {"lat": -34.6389, "lng": -58.4389},
                "description": "Polideportivo municipal con canchas cubiertas",
                "rating": 4.1,
                "distance": "7.3 km",
                "price_range": "$",
                "contact": "+54 11 4921-0800",
                "facilities": ["Canchas cubiertas", "Vestuarios", "Estacionamiento"]
            },
            
            # Piscinas
            {
                "id": 13,
                "name": "Parque Norte",
                "category": "piscinas",
                "sports": ["natacion", "aqua fitness"],
                "address": "Av. Cantilo y Av. Lugones, Núñez, CABA",
                "coordinates": {"lat": -34.5456, "lng": -58.4789},
                "description": "Complejo acuático con piscinas olímpicas y recreativas",
                "rating": 4.4,
                "distance": "13.5 km",
                "price_range": "$$",
                "contact": "+54 11 4784-4010",
                "facilities": ["Piscina olímpica", "Piscina recreativa", "Solarium", "Vestuarios"]
            },
            {
                "id": 14,
                "name": "Club Náutico Hacoaj",
                "category": "clubes",
                "sports": ["natacion", "remo", "vela"],
                "address": "Av. Costanera Norte 6200, Tigre, Buenos Aires",
                "coordinates": {"lat": -34.4203, "lng": -58.5647},
                "description": "Club náutico con actividades acuáticas y deportes de río",
                "rating": 4.6,
                "distance": "25.8 km",
                "price_range": "$$",
                "contact": "+54 11 4749-4500",
                "facilities": ["Puerto deportivo", "Piscina", "Canchas", "Restaurante"]
            }
        ]
    
    def get_all_locations(self) -> List[Dict[str, Any]]:
        """Obtener todas las ubicaciones"""
        return self.locations_data
    
    def get_filtered_locations(self, category_filter: str = "todos", search_query: str = "") -> List[Dict[str, Any]]:
        """Filtrar ubicaciones por categoría y búsqueda"""
        filtered = self.locations_data
        
        # Filtrar por categoría
        if category_filter != "todos":
            filtered = [loc for loc in filtered if loc["category"] == category_filter]
        
        # Filtrar por búsqueda
        if search_query:
            search_lower = search_query.lower()
            filtered = [
                loc for loc in filtered
                if (search_lower in loc["name"].lower() or
                    search_lower in loc["description"].lower() or
                    any(search_lower in sport for sport in loc["sports"]) or
                    search_lower in loc["address"].lower())
            ]
        
        return filtered
    
    def get_locations_by_sport(self, sport: str) -> List[Dict[str, Any]]:
        """Obtener ubicaciones por deporte específico"""
        return [loc for loc in self.locations_data if sport in loc["sports"]]
    
    def get_location_by_id(self, location_id: int) -> Dict[str, Any]:
        """Obtener ubicación por ID"""
        for location in self.locations_data:
            if location["id"] == location_id:
                return location
        return None
    
    def get_nearby_locations(self, lat: float, lng: float, radius_km: float = 5.0) -> List[Dict[str, Any]]:
        """Obtener ubicaciones cercanas (simulado)"""
        # En una implementación real, calcularías la distancia real
        # Por ahora, devolvemos ubicaciones aleatorias
        import random
        locations = self.locations_data.copy()
        random.shuffle(locations)
        return locations[:8]  # Devolver 8 ubicaciones "cercanas"