# Literary Loans Backend

Welcome to your Django REST project! This README will guide you through setting up your project and getting started with development.

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- Python (version 3.6 or higher)
- pip (Python package installer)
- Virtualenv (optional but recommended)

## Setup
1. **Clone the repository**: 
   ```
   git clone (https://github.com/r4dhika/Literary_Loans_Backend.git)
   cd literaryLoans
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

## Running the Server
To start the development server, run:
```
python3 manage.py runserver
```

The server will start running at `http://127.0.0.1:8000/`.

## Creating Django Apps
To create a new Django app, run:
```
python manage.py startapp <app_name>
```
