import subprocess

def run_tests(path="."):
    """
    Executes pytest on the specified path and returns the output.
    """
    try:
        result = subprocess.run(
            ["pytest", path], 
            capture_output=True, 
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error running tests: {e}"

def generate_test_plan(component_name):
    """
    Generates a structured test plan template for a given component.
    """
    return f"""
    # Test Plan for {component_name}
    
    ## 1. Unit Tests
    - [ ] Test initialization
    - [ ] Test edge cases (null inputs, max limits)
    - [ ] Test error handling
    
    ## 2. Integration Tests
    - [ ] Test interaction with database/API
    - [ ] Test data flow
    
    ## 3. E2E Tests
    - [ ] User flow: Happy path
    - [ ] User flow: Error path
    """
