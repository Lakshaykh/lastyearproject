import psycopg2

# Database Configuration
DB_HOST = "localhost"
DB_NAME = "project"
DB_USER = "postgres"
DB_PASSWORD = "@Qwerty123@"
DB_PORT = "5432"

# Function to Establish Database Connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None
