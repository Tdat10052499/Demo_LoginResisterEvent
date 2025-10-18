"""
Script để kiểm tra và migrate database schema
Chạy script này để update bảng users với các columns mới
"""

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://demo_user:demouser01@localhost:5432/demo_app")

def check_column_exists(cursor, table_name, column_name):
    """Kiểm tra xem column có tồn tại trong table không"""
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = %s AND column_name = %s
        );
    """, (table_name, column_name))
    return cursor.fetchone()[0]

def get_table_structure(cursor, table_name):
    """Lấy structure của table"""
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, character_maximum_length
        FROM information_schema.columns 
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    return cursor.fetchall()

def migrate_database():
    """Chạy migration để update database schema"""
    try:
        # Kết nối database
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Connected successfully!\n")
        
        # Kiểm tra table users có tồn tại không
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("⚠️  Table 'users' chưa tồn tại.")
            print("💡 Hãy chạy backend để tự động tạo tables:")
            print("   python -m uvicorn app.main:app --reload")
            return
        
        print("📊 Current table structure:")
        print("-" * 80)
        structure = get_table_structure(cursor, 'users')
        for col in structure:
            print(f"  {col[0]:20} {col[1]:15} {col[2]:10} {col[3] if col[3] else ''}")
        print("-" * 80)
        print()
        
        # Kiểm tra các columns cần thiết
        needs_migration = False
        
        print("🔍 Checking required columns...")
        
        # Check username column
        if not check_column_exists(cursor, 'users', 'username'):
            print("  ❌ Column 'username' not found - MIGRATION NEEDED")
            needs_migration = True
        else:
            print("  ✅ Column 'username' exists")
        
        # Check hashed_password column
        if not check_column_exists(cursor, 'users', 'hashed_password'):
            print("  ❌ Column 'hashed_password' not found - MIGRATION NEEDED")
            needs_migration = True
        else:
            print("  ✅ Column 'hashed_password' exists")
        
        print()
        
        if not needs_migration:
            print("✅ Database schema is up to date! No migration needed.")
            print()
            return
        
        # Thực hiện migration
        print("🚀 Starting migration...")
        print("-" * 80)
        
        migration_steps = []
        
        # Add username column
        if not check_column_exists(cursor, 'users', 'username'):
            print("  📝 Adding 'username' column...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS username VARCHAR(100) UNIQUE;
            """)
            migration_steps.append("Added 'username' column")
            print("     ✅ Done")
        
        # Add hashed_password column
        if not check_column_exists(cursor, 'users', 'hashed_password'):
            print("  📝 Adding 'hashed_password' column...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS hashed_password VARCHAR(255);
            """)
            migration_steps.append("Added 'hashed_password' column")
            print("     ✅ Done")
        
        # Make name nullable
        print("  📝 Making 'name' column nullable...")
        cursor.execute("""
            ALTER TABLE users 
            ALTER COLUMN name DROP NOT NULL;
        """)
        migration_steps.append("Made 'name' nullable")
        print("     ✅ Done")
        
        # Make provider nullable
        print("  📝 Making 'provider' column nullable...")
        cursor.execute("""
            ALTER TABLE users 
            ALTER COLUMN provider DROP NOT NULL;
        """)
        migration_steps.append("Made 'provider' nullable")
        print("     ✅ Done")
        
        # Update existing users provider
        print("  📝 Setting default provider for existing users...")
        cursor.execute("""
            UPDATE users 
            SET provider = 'microsoft' 
            WHERE provider IS NULL;
        """)
        migration_steps.append("Set default provider")
        print("     ✅ Done")
        
        # Create indexes
        print("  📝 Creating indexes...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        """)
        migration_steps.append("Created indexes")
        print("     ✅ Done")
        
        # Commit changes
        conn.commit()
        
        print("-" * 80)
        print("✅ Migration completed successfully!")
        print()
        
        # Show updated structure
        print("📊 Updated table structure:")
        print("-" * 80)
        structure = get_table_structure(cursor, 'users')
        for col in structure:
            print(f"  {col[0]:20} {col[1]:15} {col[2]:10} {col[3] if col[3] else ''}")
        print("-" * 80)
        print()
        
        print("📝 Migration Summary:")
        for step in migration_steps:
            print(f"  ✅ {step}")
        print()
        
        print("🎉 Database is now ready for authentication!")
        print()
        print("Next steps:")
        print("  1. Start backend: python -m uvicorn app.main:app --reload")
        print("  2. Test registration: POST /auth/register")
        print("  3. Test login: POST /auth/login")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("\n🔌 Database connection closed.")

if __name__ == "__main__":
    print("=" * 80)
    print("  DATABASE MIGRATION TOOL")
    print("  Demo Login/Register Event - Users Table Migration")
    print("=" * 80)
    print()
    
    migrate_database()
