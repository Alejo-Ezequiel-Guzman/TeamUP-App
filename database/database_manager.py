import sqlite3
import hashlib
from datetime import datetime
from typing import List, Optional
from database.models import Notification
from database.models import User, Post, Like, Comment, Follow

class DatabaseManager:
    def __init__(self, db_path: str = "teamup.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de Usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                bio TEXT DEFAULT '',
                avatar_url TEXT DEFAULT '',
                sport TEXT DEFAULT '',
                followers_count INTEGER DEFAULT 0,
                following_count INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 0,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de Posts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                caption TEXT NOT NULL,
                image_url TEXT NOT NULL,
                likes_count INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Tabla de  Likes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (post_id) REFERENCES posts (id),
                UNIQUE(user_id, post_id)
            )
        ''')
        
        # Tabla de Comentarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (post_id) REFERENCES posts (id)
            )
        ''')
        
        # Tabla de Seguidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id INTEGER NOT NULL,
                following_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (follower_id) REFERENCES users (id),
                FOREIGN KEY (following_id) REFERENCES users (id),
                UNIQUE(follower_id, following_id)
            )
        ''')
        # Tabla de Notificaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                from_user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                post_id INTEGER,
                message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (from_user_id) REFERENCES users (id),
                FOREIGN KEY (post_id) REFERENCES posts (id)
            )
        ''')
        
        conn.commit()
        conn.close()

        
    def has_users(self) -> bool:
        """Verificar si existen usuarios en la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        user_count = cursor.fetchone()['count']
        conn.close()
        return user_count > 0
    

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    # User operations
    def create_user(self, user: User) -> Optional[int]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, bio, avatar_url, sport)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user.username, user.email, self.hash_password(user.password_hash), 
                  user.full_name, user.bio, user.avatar_url, user.sport))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users WHERE username = ? AND password_hash = ?
        ''', (username, self.hash_password(password)))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                password_hash=row['password_hash'],
                full_name=row['full_name'],
                bio=row['bio'],
                avatar_url=row['avatar_url'],
                sport=row['sport'],
                followers_count=row['followers_count'],
                following_count=row['following_count'],
                posts_count=row['posts_count'],
                is_verified=row['is_verified'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                full_name=row['full_name'],
                bio=row['bio'],
                avatar_url=row['avatar_url'],
                sport=row['sport'],
                followers_count=row['followers_count'],
                following_count=row['following_count'],
                posts_count=row['posts_count'],
                is_verified=row['is_verified'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        return None
    
    def update_user(self, user: User) -> bool:
        """Actualizar información del usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET full_name = ?,
                    bio = ?,
                    avatar_url = ?,
                    sport = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user.full_name, user.bio, user.avatar_url, user.sport, user.id))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            conn.close()
            return False

    # Post operations
    def create_post(self, post: Post) -> Optional[int]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (user_id, caption, image_url)
            VALUES (?, ?, ?)
        ''', (post.user_id, post.caption, post.image_url))
        
        post_id = cursor.lastrowid
        
        # Update user's post count
        cursor.execute('''
            UPDATE users SET posts_count = posts_count + 1 WHERE id = ?
        ''', (post.user_id,))
        
        conn.commit()
        conn.close()
        return post_id
    
    def get_posts_feed(self, limit: int = 20) -> List[Post]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, u.username, u.avatar_url as user_avatar
            FROM posts p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        posts = []
        for row in rows:
            posts.append(Post(
                id=row['id'],
                user_id=row['user_id'],
                caption=row['caption'],
                image_url=row['image_url'],
                likes_count=row['likes_count'],
                comments_count=row['comments_count'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                username=row['username'],
                user_avatar=row['user_avatar']
            ))
        
        return posts
    
    def get_user_posts(self, user_id: int) -> List[Post]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, u.username, u.avatar_url as user_avatar
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.user_id = ?
            ORDER BY p.created_at DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        posts = []
        for row in rows:
            posts.append(Post(
                id=row['id'],
                user_id=row['user_id'],
                caption=row['caption'],
                image_url=row['image_url'],
                likes_count=row['likes_count'],
                comments_count=row['comments_count'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                username=row['username'],
                user_avatar=row['user_avatar']
            ))
        
        return posts
    
    # Like operations
    def toggle_like(self, user_id: int, post_id: int) -> bool:
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if like exists
        cursor.execute('''
            SELECT id FROM likes WHERE user_id = ? AND post_id = ?
        ''', (user_id, post_id))
        
        existing_like = cursor.fetchone()
        
        if existing_like:
            # Remove like
            cursor.execute('''
                DELETE FROM likes WHERE user_id = ? AND post_id = ?
            ''', (user_id, post_id))
            
            cursor.execute('''
                UPDATE posts SET likes_count = likes_count - 1 WHERE id = ?
            ''', (post_id,))
            
            liked = False
        else:
            # Add like
            cursor.execute('''
                INSERT INTO likes (user_id, post_id) VALUES (?, ?)
            ''', (user_id, post_id))
            
            cursor.execute('''
                UPDATE posts SET likes_count = likes_count + 1 WHERE id = ?
            ''', (post_id,))
            
            # CREAR NOTIFICACIÓN ← NUEVO
            # Obtener el dueño del post
            cursor.execute('SELECT user_id FROM posts WHERE id = ?', (post_id,))
            post_owner = cursor.fetchone()
            
            if post_owner and post_owner['user_id'] != user_id:
                # Solo notificar si no es tu propio post
                cursor.execute('''
                    INSERT INTO notifications (user_id, from_user_id, type, post_id, message)
                    VALUES (?, ?, 'like', ?, 'le dio like a tu publicación')
                ''', (post_owner['user_id'], user_id, post_id))
            
            liked = True
    
        conn.commit()
        conn.close()
        return liked


    def create_comment(self, user_id: int, post_id: int, content: str) -> Optional[int]:
        """Crear un comentario y generar notificación"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insertar comentario
            cursor.execute('''
                INSERT INTO comments (user_id, post_id, content)
                VALUES (?, ?, ?)
            ''', (user_id, post_id, content))
            
            comment_id = cursor.lastrowid
            
            # Actualizar contador de comentarios
            cursor.execute('''
                UPDATE posts SET comments_count = comments_count + 1 WHERE id = ?
            ''', (post_id,))
            
            # CREAR NOTIFICACIÓN
            # Obtener el dueño del post
            cursor.execute('SELECT user_id FROM posts WHERE id = ?', (post_id,))
            post_owner = cursor.fetchone()
            
            if post_owner and post_owner['user_id'] != user_id:
                # Solo notificar si no es tu propio post
                cursor.execute('''
                    INSERT INTO notifications (user_id, from_user_id, type, post_id, message)
                    VALUES (?, ?, 'comment', ?, 'comentó tu publicación')
                ''', (post_owner['user_id'], user_id, post_id))
            
            conn.commit()
            return comment_id
        except Exception as e:
            print(f"Error al crear comentario: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()


    def toggle_follow(self, follower_id: int, following_id: int) -> bool:
        """Seguir/dejar de seguir a un usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar si ya sigue
            cursor.execute('''
                SELECT id FROM follows WHERE follower_id = ? AND following_id = ?
            ''', (follower_id, following_id))
            
            existing_follow = cursor.fetchone()
            
            if existing_follow:
                # Dejar de seguir
                cursor.execute('''
                    DELETE FROM follows WHERE follower_id = ? AND following_id = ?
                ''', (follower_id, following_id))
                
                # Actualizar contadores
                cursor.execute('''
                    UPDATE users SET followers_count = followers_count - 1 WHERE id = ?
                ''', (following_id,))
                
                cursor.execute('''
                    UPDATE users SET following_count = following_count - 1 WHERE id = ?
                ''', (follower_id,))
                
                is_following = False
            else:
                # Seguir
                cursor.execute('''
                    INSERT INTO follows (follower_id, following_id) VALUES (?, ?)
                ''', (follower_id, following_id))
                
                # Actualizar contadores
                cursor.execute('''
                    UPDATE users SET followers_count = followers_count + 1 WHERE id = ?
                ''', (following_id,))
                
                cursor.execute('''
                    UPDATE users SET following_count = following_count + 1 WHERE id = ?
                ''', (follower_id,))
                
                # CREAR NOTIFICACIÓN
                cursor.execute('''
                    INSERT INTO notifications (user_id, from_user_id, type, message)
                    VALUES (?, ?, 'follow', 'comenzó a seguirte')
                ''', (following_id, follower_id))
                
                is_following = True
            
            conn.commit()
            return is_following
        except Exception as e:
            print(f"Error al seguir/dejar de seguir: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()


    def seed_sample_data(self):
        # Users de muestra
        sample_users = [
            User(username="alex_athlete", email="alex@teamup.com", password_hash="password123",
                 full_name="Alex Rodriguez", bio="Professional athlete 🏃‍♂️ | Track & Field Champion",
                 avatar_url="https://i.pravatar.cc/150?img=12", sport="Track & Field"),
            User(username="luciana.dev", email="luciana@teamup.com", password_hash="password123",
                 full_name="Luciana Developer", bio="Software developer and fitness enthusiast 💻💪",
                 avatar_url="https://i.pravatar.cc/150?img=3", sport="CrossFit"),
            User(username="juan.martinez", email="juan@teamup.com", password_hash="password123",
                 full_name="Juan Martinez", bio="Marathon runner 🏃‍♂️ | Personal trainer",
                 avatar_url="https://i.pravatar.cc/150?img=5", sport="Running"),
            User(username="natalia_arte", email="natalia@teamup.com", password_hash="password123",
                 full_name="Natalia Arte", bio="Yoga instructor 🧘‍♀️ | Mindfulness coach",
                 avatar_url="https://i.pravatar.cc/150?img=8", sport="Yoga")
        ]
        
        user_ids = []
        for user in sample_users:
            user_id = self.create_user(user)
            if user_id:
                user_ids.append(user_id)
        
        # Post de muestra
        sample_posts = [
            Post(user_id=user_ids[1], caption="Morning training session complete! 💪 Ready to crush today's goals! #TeamUP #MorningMotivation",
                 image_url="https://picsum.photos/375/250?1"),
            Post(user_id=user_ids[2], caption="New personal record! 🏃‍♂️ Thanks to everyone who supported me during training #PR #Athletics",
                 image_url="https://picsum.photos/375/250?2"),
            Post(user_id=user_ids[3], caption="Recovery day with some yoga 🧘‍♀️ Balance is key in athletic performance #Recovery #Mindfulness",
                 image_url="https://picsum.photos/375/250?3"),
            Post(user_id=user_ids[0], caption="Track practice this morning! Working on my sprint technique 🏃‍♂️⚡ #TrackAndField #SprintTraining",
                 image_url="https://picsum.photos/375/250?4"),
        ]
        
        for post in sample_posts:
            self.create_post(post)
        # Notification operations


    def create_notification(self, notification) -> Optional[int]:
        """Crear una nueva notificación"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO notifications (user_id, from_user_id, type, post_id, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (notification.user_id, notification.from_user_id, notification.type, 
                notification.post_id, notification.message))
            
            notification_id = cursor.lastrowid
            conn.commit()
            return notification_id
        except Exception as e:
            print(f"Error al crear notificación: {e}")
            return None
        finally:
            conn.close()

    def get_user_notifications(self, user_id: int, limit: int = 50):
        """Obtener notificaciones de un usuario"""
        from database.models import Notification
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT n.*, u.username as from_username, u.avatar_url as from_user_avatar
            FROM notifications n
            JOIN users u ON n.from_user_id = u.id
            WHERE n.user_id = ?
            ORDER BY n.created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        notifications = []
        for row in rows:
            notifications.append(Notification(
                id=row['id'],
                user_id=row['user_id'],
                from_user_id=row['from_user_id'],
                type=row['type'],
                post_id=row['post_id'],
                message=row['message'],
                is_read=row['is_read'],
                created_at=row['created_at'],
                from_username=row['from_username'],
                from_user_avatar=row['from_user_avatar']
            ))
        
        return notifications

    def mark_notification_as_read(self, notification_id: int) -> bool:
        """Marcar notificación como leída"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications SET is_read = TRUE WHERE id = ?
        ''', (notification_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def mark_all_notifications_as_read(self, user_id: int) -> bool:
        """Marcar todas las notificaciones como leídas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications SET is_read = TRUE WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        return True

    def get_unread_notifications_count(self, user_id: int) -> int:
        """Obtener cantidad de notificaciones no leídas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as count FROM notifications 
            WHERE user_id = ? AND is_read = FALSE
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return row['count'] if row else 0

    def delete_notification(self, notification_id: int) -> bool:
        """Eliminar una notificación"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM notifications WHERE id = ?
        ''', (notification_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success