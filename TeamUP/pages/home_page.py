import flet as ft
from components.post_component import create_post

class HomePage:
    def __init__(self, theme_manager, db_manager=None):
        self.theme_manager = theme_manager
        self.db_manager = db_manager
        self.content = None
    
    def create_content(self):
        colors = self.theme_manager.get_theme_colors()
        
        # Get posts from database if available
        posts_data = []
        if self.db_manager:
            try:
                posts_data = self.db_manager.get_posts_feed(limit=20)
            except Exception as e:
                print(f"Error fetching posts: {e}")
                posts_data = []
        
        if not posts_data:
            # Post defaults si no hay posts en la base de datos
            sample_posts = [
                {
                    "username": "luciana.dev",
                    "user_avatar": "https://i.pravatar.cc/150?img=3",
                    "image_url": "https://picsum.photos/375/250?1",
                    "caption": "Morning training session complete! 💪 Ready to crush today's goals! #TeamUP #MorningMotivation",
                    "likes_count": 24,
                    "comments_count": 5
                },
                {
                    "username": "juan.martinez",
                    "user_avatar": "https://i.pravatar.cc/150?img=5",
                    "image_url": "https://picsum.photos/375/250?2",
                    "caption": "New personal record! 🏃‍♂️ Thanks to everyone who supported me during training #PR #Athletics",
                    "likes_count": 18,
                    "comments_count": 3
                },
                {
                    "username": "natalia_arte",
                    "user_avatar": "https://i.pravatar.cc/150?img=8",
                    "image_url": "https://picsum.photos/375/250?3",
                    "caption": "Recovery day with some yoga 🧘‍♀️ Balance is key in athletic performance #Recovery #Mindfulness",
                    "likes_count": 31,
                    "comments_count": 7
                },
            ]
            
            posts = [
                create_post(
                    post["username"],
                    post["user_avatar"],
                    post["image_url"],
                    post["caption"],
                    colors,
                    post["likes_count"],
                    post["comments_count"]
                ) for post in sample_posts
            ]
        else:
            posts = [
                create_post(
                    post.username,
                    post.user_avatar or "https://i.pravatar.cc/150?img=1",
                    post.image_url,
                    post.caption,
                    colors,
                    post.likes_count,
                    post.comments_count
                ) for post in posts_data
            ]
        
        self.content = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            controls=posts
        )
        
        return self.content
    
    def update_theme(self):
        if self.content:
            colors = self.theme_manager.get_theme_colors()
            self.content.bgcolor = colors["content_bg"]
            
            # Actulizar el tema de cada post
            for control in self.content.controls:
                if hasattr(control, 'bgcolor'):
                    control.bgcolor = colors["card_bg"]
                    # Actualizar colores de texto e iconos
                    self._update_post_colors(control, colors)
    
    def _update_post_colors(self, post_container, colors):
        if hasattr(post_container, 'content') and isinstance(post_container.content, ft.Column):
            for item in post_container.content.controls:
                if isinstance(item, ft.Row):
                    for subitem in item.controls:
                        if isinstance(subitem, ft.Text):
                            subitem.color = colors["text_primary"]
                        elif isinstance(subitem, ft.Icon):
                            subitem.color = colors["icon_color"]
                elif isinstance(item, ft.Text):
                    item.color = colors["text_primary"]
                elif isinstance(item, ft.Divider):
                    item.color = colors["divider_color"]