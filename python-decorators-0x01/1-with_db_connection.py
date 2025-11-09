import sqlite3 
import functools

def with_db_connection(func):
    """
    Decorator that automatically handles database connections.
    
    Opens a database connection before function execution, passes it to the function,
    and ensures the connection is closed afterward.
    
    Args:
        func: The function to be decorated (should accept a connection as first parameter)
    
    Returns:
        Wrapped function with automatic connection management
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Establish database connection
        conn = sqlite3.connect('users.db')
        
        try:
            # Execute the function with the connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Ensure connection is closed even if an exception occurs
            conn.close()
    
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    """
    Get user by ID with automatic connection handling.
    
    Args:
        conn: Database connection (automatically provided by decorator)
        user_id: ID of the user to retrieve
    
    Returns:
        User record or None if not found
    """
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone()

#### Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id=1)
print(user) 

