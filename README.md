# SharePay Backend

**SharePay** is a web application for event management, allowing users to create events, manage attendees, send notifications, and track activity. This repository contains the backend API built with Django.

## Features

- Event creation and user management  
- Real-time notifications and activity tracking  
- Secure authentication and authorization  
- RESTful API endpoints ready for integration with the SharePay frontend

## Requirements

Make sure you have the following installed:

- Python 3.10 or higher  
- Django 4.2.5 or higher  
- Virtualenv 20.24 or higher  

## Getting Started

Follow these steps to set up and run the project locally:

1. **Clone the repository:**

   ```bash
   git clone git@github.com:Riddimental/SharePay_Backend.git
   cd SharePay_Backend
   ```

2. **Create a virtual environment:**

   - **Windows:**

     ```cmd
     python -m venv myenv
     ```

   - **macOS / Linux:**

     ```sh
     python3 -m venv myenv
     ```

3. **Activate the virtual environment:**

   - **Windows:**

     ```cmd
     .\myenv\Scripts\activate
     ```

   - **macOS / Linux:**

     ```sh
     source myenv/bin/activate
     ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Make migrations**

   ```bash
   python manage.py makemigrations && python manage.py migrate
   ```

6. **Make superuser**

   ```bash
   python manage.py createsuperuser
   ```

   give a username, email (optional) and password, you can acces to the api admin view at:
   ```
   http://127.0.0.1:8000/admin/
   ```

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

Once the server is running, the backend will be available at:

```
http://127.0.0.1:8000/
```

## Related Projects

- [SharePay Frontend Repository](https://github.com/MavelSterling/SharePay_AppWeb)