import time
import sqlite3 
import functools

# Global cache for storing query results
query_cache = {}

def cache_query(func):
    """
    Decorator that caches database query results based on the SQL query string.
    Wrapped function with query caching
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from arguments
        query = None
        
        # Check for query in keyword arguments
        if 'query' in kwargs:
            query = kwargs['query']
        # Check for query as first positional argument
        elif args and isinstance(args[0], str):
            query = args[0]
        else:
            # If no query found, execute without caching
            return func(*args, **kwargs)
        
        # Normalize the query for consistent cache keys
        cache_key = query.strip().lower()
        
        # Check if result is already cached
        if cache_key in query_cache:
            print(f"✓ Cache hit for query: {query[:50]}...")
            return query_cache[cache_key]
        else:
            print(f"✗ Cache miss - executing query: {query[:50]}...")
            # Execute the query and cache the result
            result = func(*args, **kwargs)
            query_cache[cache_key] = result
            print(f"✓ Query result cached (Cache size: {len(query_cache)})")
            return result
    
    return wrapper

# Include the with_db_connection decorator
def with_db_connection(db_path='users.db'):
    """
    Decorator will automatically handles database connections.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(db_path)
            try:
                result = func(conn, *args, **kwargs)
                return result
            finally:
                conn.close()
        return wrapper
    return decorator

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from database with query caching.
    conn: Database connection provided by with_db_connection
    query: SQL query to execute operations
    list: Query results
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users") 

