import asyncio
import os
from databases import Database

DATABASE_URL = "postgresql://admin:password@localhost:5432/safewalk"

async def init_db():
    database = Database(DATABASE_URL)
    try:
        await database.connect()
        print("Connected to database")
        
        with open("app/schema.sql", "r") as f:
            schema = f.read()
            
        # simple split by semicolon, ignoring empty lines
        statements = [s.strip() for s in schema.split(';') if s.strip()]
        
        for statement in statements:
            try:
                # Skip transactions blocks if any (BEGIN/COMMIT) if they cause issues, 
                # but pure DDL should be fine.
                await database.execute(statement)
            except Exception as e:
                print(f"Error executing statement: {statement[:50]}... -> {e}")
                
        print("Schema applied successfully")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(init_db())
