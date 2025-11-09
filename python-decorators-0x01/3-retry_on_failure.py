import time
import sqlite3 
import functools

#### paste your with_db_connection decorator here
def with_db_connection(db_path='users.db'):
    """
    Decorator that automatically handles database connections.
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

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries function execution on failure.
    Decorator function with retry logic
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(retries + 1):  # +1 for the initial attempt
                try:
                    # Attempt to execute the function
                    result = func(*args, **kwargs)
                    
                    # If successful on retry, log the success
                    if attempt > 0:
                        print(f"✓ Attempt {attempt + 1} succeeded after {attempt} previous failures")
                    
                    return result
                    
                except Exception as e:
                    last_exception = e
                    
                    # Check if we should retry
                    if attempt < retries:
                        print(f"✗ Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        # Final attempt failed
                        print(f"✗ All {retries + 1} attempts failed. Last error: {e}")
                        raise last_exception
            
            # This should never be reached, but for safety
            raise last_exception
        
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the database with automatic retry on failure.
    Args:
    conn: Database connection (provided by with_db_connection)
    Returns: list: All user records from the database
    
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)  

