# alx-backend-python
This project focuses on mastering Python decorators to enhance database operations in Python applications. Through hands-on tasks, learners will create custom decorators to log queries, handle connections, manage transactions, retry failed operations, and cache query results.


## Task Overview
Implement unit tests to verify that the `access_nested_map` function correctly raises `KeyError` exceptions with appropriate messages when accessing invalid paths in nested dictionaries.

## Function Under Test
**`access_nested_map(nested_map: Mapping, path: Sequence) -> Any`**
- Accesses nested dictionaries using a sequence of keys as a path
- Raises `KeyError` when the path is invalid

## Test Cases

### Test Method: `test_access_nested_map_exception`
Verifies that `KeyError` is raised with correct exception messages for invalid access paths.

#### Test Case 1: Empty Map
- **Input**: `nested_map = {}`, `path = ("a",)`
- **Expected**: Raises `KeyError` with message `'a'`
- **Scenario**: Trying to access key 'a' in an empty dictionary

#### Test Case 2: Invalid Nested Path
- **Input**: `nested_map = {"a": 1}`, `path = ("a", "b")`
- **Expected**: Raises `KeyError` with message `'b'`
- **Scenario**: Key 'a' exists but is not a nested dictionary, so cannot access 'b'

## Implementation Details

### Dependencies
- `unittest` - Python testing framework
- `parameterized` - For parameterized test cases
- `utils.access_nested_map` - Function being tested

### Key Testing Components
1. **Parameterized Testing**: Uses `@parameterized.expand` to run multiple test cases
2. **Exception Testing**: Uses `assertRaises` context manager to verify exceptions
3. **Message Verification**: Checks that the exception contains the expected key name

### Test Code Structure
```python
@parameterized.expand([
    ({}, ("a",), 'a'),
    ({"a": 1}, ("a", "b"), 'b')
])
def test_access_nested_map_exception(self, nested_map, path, expected_key):
    with self.assertRaises(KeyError) as context:
        access_nested_map(nested_map, path)
    self.assertEqual(str(context.exception), f"'{expected_key}'")
