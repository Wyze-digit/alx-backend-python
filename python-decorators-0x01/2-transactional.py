import sqlite3 
import functools

# Copy the with_db_connection decorator from previous task
def with_db_connection(db_path='users.db'):
    """
    Decorator that automatically handles database connections. The decorator will Opens a database connection before function execution, 
    passes it to the function, and ensures the connection is closed afterward.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Establish database connection
            conn = sqlite3.connect(db_path)
            
            try:
                # Execute the function with the connection as first argument
                result = func(conn, *args, **kwargs)
                return result
            finally:
                # Ensure connection is closed even if an exception occurs
                conn.close()
        
        return wrapper
    return decorator

def transactional(func):
    """
    Decorator that automatically manages database transactions.   
    Wraps a database operation in a transaction. If the function executes 
    successfully, commits the transaction. If any exception occurs, 
    rolls back the transaction.
    
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract connection from arguments (assumes it's the first argument)
        conn = args[0] if len(args) > 0 else None
        
        try:
            # Execute the function
            result = func(*args, **kwargs)
            
            # Commit transaction on success
            if conn:
                conn.commit()
                print("Transaction committed successfully")
            
            return result
            
        except Exception as e:
            # Rollback transaction on error
            if conn:
                conn.rollback()
                print("Transaction rolled back due to error")
            
            # Re-raise the exception to maintain original error behavior
            raise e
    
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    """
    This portion Update user's email with automatic connection and transaction handling. conn: Database connection (provided by with_db_connection)
        user_id: ID of the user to update
        new_email: New email address for the user
    """
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    
    # Check if any rows were affected
    if cursor.rowcount == 0:
        raise ValueError(f"No user found with ID {user_id}")
    
    print(f"Successfully updated email for user {user_id}")

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

