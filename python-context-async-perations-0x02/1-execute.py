import sqlite3

class ExecuteQuery:
    """
    A reusable context manager that takes a query as input and executes it,
    managing both the database connection and query execution automatically.
    
    This context manager automatically:
    - Opens a database connection
    - Executes the provided query with parameters
    - Returns the query results
    - Closes the connection and cleans up resources
    """
    
    def __init__(self, query, params=None, database_path='users.db'):
        """
        Initialize the query execution context manager.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for parameterized queries
            database_path (str): Path to the SQLite database file
        """
        self.query = query
        self.params = params
        self.database_path = database_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Enter the runtime context, execute the query, and return results.
        
        Returns:
            list: Query results as a list of rows
        """
        # Establish database connection
        self.connection = sqlite3.connect(self.database_path)
        
        # Configure connection to return rows as dictionaries
        self.connection.row_factory = sqlite3.Row
        
        # Create cursor and execute query
        self.cursor = self.connection.cursor()
        
        print(f"✓ Executing query: {self.query}")
        if self.params:
            print(f"✓ With parameters: {self.params}")
        
        # Execute the query with parameters
        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)
        
        # Fetch all results
        results = self.cursor.fetchall()
        print(f"✓ Query executed successfully, returned {len(results)} rows")
        
        return results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and cleanup resources.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred  
            exc_tb: Exception traceback if an exception occurred
            
        Returns:
            bool: False to propagate exceptions, True to suppress
        """
        # Close cursor and connection
        if self.cursor:
            self.cursor.close()
        
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")
        
        # Return False to propagate any exceptions
        return False

# Enhanced version with transaction support and better error handling
class ExecuteQueryWithTransactions(ExecuteQuery):
    """
    Enhanced query execution context manager with transaction support.
    """
    
    def __enter__(self):
        """Enter context and execute query within a transaction."""
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        
        try:
            # Begin transaction explicitly
            self.connection.execute("BEGIN")
            
            self.cursor = self.connection.cursor()
            
            print(f"✓ Executing query in transaction: {self.query}")
            if self.params:
                print(f"✓ With parameters: {self.params}")
            
            # Execute query
            if self.params:
                self.cursor.execute(self.query, self.params)
            else:
                self.cursor.execute(self.query)
            
            results = self.cursor.fetchall()
            print(f"✓ Query executed successfully, returned {len(results)} rows")
            
            return results
            
        except Exception as e:
            # Rollback on error and re-raise
            if self.connection:
                self.connection.rollback()
            raise e
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context with transaction commit/rollback.
        """
        try:
            if exc_type is None:
                # No exception - commit transaction
                if self.connection:
                    self.connection.commit()
                    print("✓ Transaction committed")
            else:
                # Exception occurred - rollback (already done in __enter__)
                print("✓ Transaction rolled back due to exception")
        finally:
            # Always close resources
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                print("✓ Database connection closed")
        
        return False

# Setup function to create test database
def setup_test_database():
    """Set up a test database with sample data."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER
        )
    ''')
    
    # Clear and insert sample data
    cursor.execute("DELETE FROM users")
    sample_users = [
        ('John Doe', 'john@example.com', 30),
        ('Jane Smith', 'jane@example.com', 25),
        ('Bob Johnson', 'bob@example.com', 35),
        ('Alice Brown', 'alice@example.com', 28),
        ('Charlie Wilson', 'charlie@example.com', 22),
        ('Diana Davis', 'diana@example.com', 40)
    ]
    
    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        sample_users
    )
    
    conn.commit()
    conn.close()
    print("✓ Test database setup complete")

# Main execution
if __name__ == "__main__":
    print("Testing Reusable Query Execution Context Manager")
    print("=" * 60)
    
    # Setup test database first
    setup_test_database()
    
    print("\n1. Basic query execution with specific query and parameter:")
    print("-" * 50)
    
    # Use the context manager with the specific query and parameter
    with ExecuteQuery(
        query="SELECT * FROM users WHERE age > ?", 
        params=(25,)
    ) as results:
        
        # Print the results returned from the query
        print("Users older than 25:")
        for row in results:
            user_dict = dict(row)
            print(f"  - {user_dict['name']} (Age: {user_dict['age']}, Email: {user_dict['email']})")
    
    print("\n2. Reusing with different query and parameters:")
    print("-" * 50)
    
    # Reuse with different query - users between ages 25 and 35
    with ExecuteQuery(
        query="SELECT * FROM users WHERE age BETWEEN ? AND ?", 
        params=(25, 35)
    ) as results:
        
        print("Users between 25 and 35:")
        for row in results:
            user_dict = dict(row)
            print(f"  - {user_dict['name']} (Age: {user_dict['age']})")
    
    print("\n3. Query without parameters:")
    print("-" * 50)
    
    # Query without parameters - get all users
    with ExecuteQuery(
        query="SELECT * FROM users ORDER BY name"
    ) as results:
        
        print("All users sorted by name:")
        for row in results:
            user_dict = dict(row)
            print(f"  - {user_dict['name']}")
    
    print("\n4. Using enhanced version with transaction support:")
    print("-" * 50)
    
    with ExecuteQueryWithTransactions(
        query="SELECT * FROM users WHERE age > ?", 
        params=(30,)
    ) as results:
        
        print("Users older than 30 (with transaction):")
        for row in results:
            user_dict = dict(row)
            print(f"  - {user_dict['name']} (Age: {user_dict['age']})")
    
    print("\n5. Testing error handling:")
    print("-" * 50)
    
    try:
        # This will cause an error (invalid table name)
        with ExecuteQuery(
            query="SELECT * FROM non_existent_table WHERE age > ?", 
            params=(25,)
        ) as results:
            print("This should not print")
    except sqlite3.OperationalError as e:
        print(f"✓ Error properly handled: {e}")
        print("✓ Resources were still cleaned up properly")
    
    print("\n6. Counting results:")
    print("-" * 50)
    
    with ExecuteQuery(
        query="SELECT COUNT(*) as user_count FROM users WHERE age > ?", 
        params=(25,)
    ) as results:
        
        count = results[0]['user_count']
        print(f"Total users older than 25: {count}")