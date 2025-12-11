from database.database_manager import DatabaseManager

def initialize_database():
    """Initialize database and add sample data"""
    db = DatabaseManager()
    
    # Check if we need to seed data
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    conn.close()
    
    if user_count == 0:
        print("Seeding database with sample data...")
        db.seed_sample_data()
        print("Database initialized with sample data!")
    else:
        print("Database already contains data.")
    
    return db

if __name__ == "__main__":
    initialize_database()