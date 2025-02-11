# Animal Adoption Web App

This is a Django-based web application for animal adoption, allowing users to browse available animals, apply for adoption, and find nearby veterinary clinics and animal shelters using Google Maps API, and search different types of useful articles.

## Features

- **User Authentication**: Users can sign up, log in, and manage their accounts.
- **Animal Listings**: Users can browse available animals for adoption.
- **Adoption Requests**: Users can apply to adopt animals.
- **Google Maps Integration**: Displays nearby veterinary clinics and animal shelters based on the user's city.
- **Email Notifications**: Sends email confirmations and notifications using a configured Gmail SMTP server.
- **Pagination**: Large lists of animals are paginated for better performance and usability.
- **Web Scraping**: Uses `BeautifulSoup` and `requests` to extract relevant animal articles.

## Prerequisites

- **Python 3.x** installed
- **Django** framework
- **Google API Key** (for Maps API integration)
- **Gmail Account** (with 2 step authentication enabled)

## Set Up Environment Variables

In `settings.py`, configure the following settings:
```bash
GOOGLE_API_KEY = 'your-generated-password'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-mail@gmail.com'
EMAIL_HOST_PASSWORD = 'password-generated'
```
## Run Migrations
```bash
python manage.py makemigrations

python manage.py migrate
```
## Start the Server
```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`.

## Google Maps Integration

The application uses the Google Maps JavaScript API to display veterinary clinics and animal shelters within the user's city. This feature requires a valid Google API key set in `settings.py`.

## Project Structure

- **models.py**: Defines database models, including User and Animal models.
- **views.py**: Contains logic for rendering pages and handling user requests.
- **urls.py**: Maps URLs to their corresponding views.
- **templates/**: Contains HTML templates for rendering the frontend.
- **static/**: Stores static files like CSS and JavaScript.

## Dependencies

This project requires the following dependencies:

- **Django**: Backend framework for building the application.
- **Google Maps API**: Used to fetch and display veterinary clinics and shelters.
- **BeautifulSoup & Requests**: Used for web scraping animal articles.
- **Django Authentication**: Manages user authentication and login sessions.
