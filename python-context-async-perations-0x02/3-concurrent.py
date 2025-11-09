import asyncio
import aiosqlite
from datetime import datetime

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    
    Returns:
        list: All user records from the users table
    """
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting async_fetch_users()")
    
    async with aiosqlite.connect('users.db') as db:
        # Configure row factory to return dictionaries
        db.row_factory = aiosqlite.Row
        
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            
            # Convert rows to dictionaries for easier handling
            users = [dict(row) for row in results]
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] async_fetch_users() completed: {len(users)} users")
            
            return users

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database.
    
    Returns:
        list: User records where age > 40
    """
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting async_fetch_older_users()")
    
    async with aiosqlite.connect('users.db') as db:
        # Configure row factory to return dictionaries
        db.row_factory = aiosqlite.Row
        
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            
            # Convert rows to dictionaries for easier handling
            older_users = [dict(row) for row in results]
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] async_fetch_older_users() completed: {len(older_users)} users")
            
            return older_users

async def fetch_concurrently():
    """
    Execute both database queries concurrently using asyncio.gather().
    
    Returns:
        tuple: Results from both queries (all_users, older_users)
    """
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting concurrent execution with asyncio.gather()")
    
    # Execute both queries concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
        return_exceptions=True  # Handle exceptions gracefully
    )
    
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Concurrent execution completed")
    return results

# Enhanced version with more queries and better error handling
async def async_fetch_users_by_age_range(min_age, max_age):
    """
    Asynchronously fetch users within a specific age range.
    
    Args:
        min_age (int): Minimum age
        max_age (int): Maximum age
    
    Returns:
        list: Users within the specified age range
    """
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting async_fetch_users_by_age_range({min_age}, {max_age})")
    
    async with aiosqlite.connect('users.db') as db:
        db.row_factory = aiosqlite.Row
        
        async with db.execute(
            "SELECT * FROM users WHERE age BETWEEN ? AND ?", 
            (min_age, max_age)
        ) as cursor:
            results = await cursor.fetchall()
            users = [dict(row) for row in results]
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] async_fetch_users_by_age_range() completed: {len(users)} users")
            
            return users

async def async_count_users():
    """
    Asynchronously count total number of users.
    
    Returns:
        int: Total number of users
    """
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting async_count_users()")
    
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT COUNT(*) as count FROM users") as cursor:
            result = await cursor.fetchone()
            count = result[0] if result else 0
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] async_count_users() completed: {count} users")
            
            return count

async def fetch_multiple_concurrently():
    """
    Execute multiple database queries concurrently.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Starting multiple concurrent queries")
    
    # Execute multiple queries concurrently
    all_users, older_users, young_adults, total_count = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
        async_fetch_users_by_age_range(20, 30),
        async_count_users(),
        return_exceptions=True
    )
    
    return all_users, older_users, young_adults, total_count

# Setup function to create test database
async def setup_test_database():
    """
    Set up a test database with sample data asynchronously.
    """
    print("Setting up test database...")
    
    async with aiosqlite.connect('users.db') as db:
        # Create users table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER
            )
        ''')
        
        # Clear existing data
        await db.execute("DELETE FROM users")
        
        # Insert sample data
        sample_users = [
            ('John Doe', 'john@example.com', 30),
            ('Jane Smith', 'jane@example.com', 25),
            ('Bob Johnson', 'bob@example.com', 45),
            ('Alice Brown', 'alice@example.com', 28),
            ('Charlie Wilson', 'charlie@example.com', 52),
            ('Diana Davis', 'diana@example.com', 35),
            ('Eve Miller', 'eve@example.com', 41),
            ('Frank Thomas', 'frank@example.com', 22)
        ]
        
        await db.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            sample_users
        )
        
        await db.commit()
        print("✓ Test database setup complete")

# Main execution
def main():
    """
    Main function to run concurrent database queries.
    """
    print("Testing Concurrent Database Queries with Asyncio")
    print("=" * 60)
    
    # First, setup the test database
    asyncio.run(setup_test_database())
    
    print("\n1. Running two queries concurrently:")
    print("-" * 40)
    
    # Use asyncio.run() to execute the concurrent fetch
    start_time = datetime.now()
    results = asyncio.run(fetch_concurrently())
    end_time = datetime.now()
    
    # Unpack results
    all_users, older_users = results
    
    # Check if any results are exceptions
    if isinstance(all_users, Exception):
        print(f"Error in async_fetch_users: {all_users}")
        all_users = []
    if isinstance(older_users, Exception):
        print(f"Error in async_fetch_older_users: {older_users}")
        older_users = []
    
    # Display results
    print(f"\n📊 Query Results:")
    print(f"All users: {len(all_users)} records")
    for user in all_users[:3]:  # Show first 3 users
        print(f"  - {user['name']} (Age: {user['age']})")
    if len(all_users) > 3:
        print(f"  ... and {len(all_users) - 3} more")
    
    print(f"\nUsers older than 40: {len(older_users)} records")
    for user in older_users:
        print(f"  - {user['name']} (Age: {user['age']})")
    
    execution_time = (end_time - start_time).total_seconds()
    print(f"\n⏱️  Concurrent execution time: {execution_time:.3f} seconds")
    
    print("\n2. Running multiple queries concurrently:")
    print("-" * 40)
    
    start_time = datetime.now()
    all_results = asyncio.run(fetch_multiple_concurrently())
    end_time = datetime.now()
    
    all_users, older_users, young_adults, total_count = all_results
    
    print(f"\n📊 Multiple Query Results:")
    print(f"Total users: {total_count}")
    print(f"Users older than 40: {len(older_users)}")
    print(f"Young adults (20-30): {len(young_adults)}")
    
    execution_time = (end_time - start_time).total_seconds()
    print(f"\n⏱️  Multiple concurrent execution time: {execution_time:.3f} seconds")
    
    print("\n3. Performance comparison (sequential vs concurrent):")
    print("-" * 40)
    
    async def sequential_queries():
        """Run queries sequentially for comparison."""
        start = datetime.now()
        users1 = await async_fetch_users()
        users2 = await async_fetch_older_users()
        end = datetime.now()
        return (end - start).total_seconds()
    
    async def concurrent_queries():
        """Run queries concurrently for comparison."""
        start = datetime.now()
        await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
        )
        end = datetime.now()
        return (end - start).total_seconds()
    
    # Run comparison
    sequential_time = asyncio.run(sequential_queries())
    concurrent_time = asyncio.run(concurrent_queries())
    
    print(f"Sequential execution time: {sequential_time:.3f} seconds")
    print(f"Concurrent execution time: {concurrent_time:.3f} seconds")
    print(f"Performance improvement: {((sequential_time - concurrent_time) / sequential_time * 100):.1f}% faster")

if __name__ == "__main__":
    main() 

