import os

def create_project_structure(base_dir):
    directories = [
        f"{base_dir}/app",
        f"{base_dir}/app/services",
        f"{base_dir}/app/utils"
    ]
    
    files = {
        f"{base_dir}/app/__init__.py": "",
        f"{base_dir}/app/config.py": "",
        f"{base_dir}/app/services/__init__.py": "",
        f"{base_dir}/app/services/destination_service.py": "",
        f"{base_dir}/app/services/user_service.py": "",
        f"{base_dir}/app/services/auth_service.py": "",
        f"{base_dir}/app/utils/__init__.py": "",
        f"{base_dir}/app/utils/auth_utils.py": "",
        f"{base_dir}/app/utils/validators.py": "",
        f"{base_dir}/requirements.txt": "",
        f"{base_dir}/run.py": "",
        f"{base_dir}/README.md": "# Project README"
    }
    
    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create files
    for filepath, content in files.items():
        with open(filepath, 'w') as file:
            file.write(content)
            print(f"Created file: {filepath}")

if __name__ == "__main__":
    project_name = "travel_api_project"  # Change as needed
    create_project_structure(project_name)
