"""
sample script
"""

def greet(name):
    """
    Returns a greeting message.
    """
    return f"Hello, {name}!"

def main():
    """
    Main function to execute script logic.
    """
    users = ["Alice", "Bob", "Charlie"]
    for user in users:
        print(greet(user))

if __name__ == "__main__":
    main()
