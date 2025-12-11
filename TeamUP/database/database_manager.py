import sqlite3
import hashlib
from datetime import datetime
from typing import List, Optional
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
        
        conn.commit()
        conn.close()
    
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
            
            liked = True
        
        conn.commit()
        conn.close()
        return liked
    
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