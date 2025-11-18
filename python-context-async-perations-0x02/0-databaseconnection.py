import sqlite3

class DatabaseConnection:
    """
    A class-based context manager for automatic database connection handling.
    
    This context manager automatically opens a database connection when entering
    the context and closes it when exiting, ensuring proper resource cleanup.
    """
    
    def __init__(self, database_path):
        """
        Initialize the database context manager.
        
        Args:
            database_path (str): Path to the SQLite database file
        """
        self.database_path = database_path
        self.connection = None
    
    def __enter__(self):
        """
        Enter the runtime context and establish database connection.
        
        Returns:
            DatabaseConnection: Self instance for method chaining
        """
        # Establish database connection
        self.connection = sqlite3.connect(self.database_path)
        
        # Configure connection to return rows as dictionaries
        self.connection.row_factory = sqlite3.Row
        
        print(f"✓ Database connection opened to: {self.database_path}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and close database connection.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred  
            exc_tb: Exception traceback if an exception occurred
            
        Returns:
            bool: False to propagate exceptions, True to suppress
        """
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")
        
        # Return False to propagate any exceptions that occurred
        # Return True only if you want to suppress exceptions
        return False
    
    def execute_query(self, query, params=None):
        """
        Execute a SQL query and return the cursor.         
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for parameterized queries.             
        Returns:
            sqlite3.Cursor: Database cursor with executed query
        """
        cursor = self.connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        return cursor
    
    def fetch_all(self, query, params=None):
        """
        Execute a query and return all results.         
        Args: query (str): SQL query to execute params (tuple): Parameters for parameterized queries
        Returns:
        list: All rows from the query result
        """
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        """
        Execute a query and return first result.
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for parameterized queries
        Returns:
            dict: First row from the query result
        """
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def execute_script(self, script):
        """
        Execute multiple SQL statements.
        
        Args:
            script (str): SQL script with multiple statements
        """
        cursor = self.connection.cursor()
        cursor.executescript(script)
        self.connection.commit()

# Enhanced version with transaction support
class DatabaseConnectionWithTransactions(DatabaseConnection):
    """
    Enhanced database context manager with transaction support.
    """
    
    def __enter__(self):
        """Enter context and begin transaction."""
        super().__enter__()
        # SQLite automatically begins transactions, but we can be explicit
        self.connection.execute("BEGIN")
        return self
    
    def commit(self):
        """Commit the current transaction."""
        self.connection.commit()
        print("✓ Transaction committed")
    
    def rollback(self):
        """Rollback the current transaction."""
        self.connection.rollback()
        print("✓ Transaction rolled back")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context with transaction handling.         
        Commits on success, rolls back on exception.
        """
        try:
            if exc_type is None:
                # No exception occurred - commit changes
                self.connection.commit()
                print("✓ Changes committed automatically")
            else:
                # Exception occurred - rollback changes
                self.connection.rollback()
                print("✓ Changes rolled back due to exception")
        finally:
            # Always close the connection
            if self.connection:
                self.connection.close()
                print("✓ Database connection closed")
        
        # Don't suppress exceptions
        return False

# Test the implementation
def setup_test_database():
    """Set up a test database with sample data."""
    with DatabaseConnection('users.db') as db:
        # Create users table
        db.execute_script('''
            DROP TABLE IF EXISTS users;
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER
            );
        ''')
        
        # Insert sample data
        sample_users = [
            ('John Doe', 'john@example.com', 30),
            ('Jane Smith', 'jane@example.com', 25),
            ('Bob Johnson', 'bob@example.com', 35),
            ('Alice Brown', 'alice@example.com', 28)
        ]
        
        cursor = db.connection.cursor()
        cursor.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            sample_users
        )
        
        db.connection.commit()
        print("✓ Test database setup complete")

# Main execution
if __name__ == "__main__":
    print("Testing Database Connection Context Manager")
    print("=" * 50)
    
    # Setup test database first
    setup_test_database()
    
    print("\n1. Basic context manager usage:")
    print("-" * 30)
    
    # Use the context manager with the 'with' statement
    with DatabaseConnection('users.db') as db:
        # Perform the query 'SELECT * FROM users'
        results = db.fetch_all("SELECT * FROM users")
        
        # Print the results from the query
        print("Users in database:")
        for row in results:
            # Convert Row to dict for pretty printing
            user_dict = dict(row)
            print(f"  - ID: {user_dict['id']}, Name: {user_dict['name']}, "
                  f"Email: {user_dict['email']}, Age: {user_dict['age']}")
    
    print("\n2. Using fetch_one method:")
    print("-" * 30)
    
    with DatabaseConnection('users.db') as db:
        user = db.fetch_one("SELECT * FROM users WHERE id = ?", (1,))
        if user:
            print(f"User with ID 1: {dict(user)}")
    
    print("\n3. Using parameterized queries:")
    print("-" * 30)
    
    with DatabaseConnection('users.db') as db:
        # Find users older than 30
        results = db.fetch_all("SELECT * FROM users WHERE age > ?", (30,))
        print("Users older than 30:")
        for row in results:
            user_dict = dict(row)
            print(f"  - {user_dict['name']} (Age: {user_dict['age']})")
    
    print("\n4. Testing transaction support:")
    print("-" * 30)
    
    try:
        with DatabaseConnectionWithTransactions('users.db') as db:
            # This will work
            db.execute_query(
                "UPDATE users SET age = ? WHERE id = ?", 
                (31, 1)
            )
            print("✓ First update successful")
            
            # This will cause an error (violates UNIQUE constraint)
            db.execute_query(
                "UPDATE users SET email = ? WHERE id = ?", 
                ('john@example.com', 2)  # Duplicate email
            )
            print("✓ Second update successful")
            
        # If we get here, transaction was committed
        print("✓ All updates committed")
        
    except sqlite3.IntegrityError as e:
        print(f"✗ Transaction failed: {e}")
        # The context manager automatically rolled back
    
    print("\n5. Verifying data integrity after failed transaction:")
    print("-" * 30)
    
    with DatabaseConnection('users.db') as db:
        user = db.fetch_one("SELECT * FROM users WHERE id = ?", (1,))
        if user:
            print(f"User 1 age is still: {user['age']} (transaction was rolled back)")

    print("\n6. Exception safety test:")
    print("-" * 30)
    
    try:
        with DatabaseConnection('users.db') as db:
            # This will raise an exception
            results = db.fetch_all("SELECT * FROM non_existent_table")
    except sqlite3.OperationalError as e:
        print(f"✓ Exception properly handled: {e}")
        print("✓ Database connection was still closed properly") 

