# Test Task The Capital

## Description

This project implements a web application that retrieves a
matrix from a remote server and returns it to the user
in the form of a `List[int]`. The returned list contains
the result of traversing the received matrix in a clockwise
direction, starting from the top left corner.

## Setup Instructions

1. Clone the repository to your computer.
    ```shell
   git clone https://github.com/Sparix/TestTask_TheCapital.git
   cd <project-directory>
2. Create a virtual environment by running `python -m venv venv`.
3. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On macOS and Linux: `source venv/bin/activate`
4. Install the required dependencies `pip install -r requirements.txt`.
5. Run migration `python manage.py migrate`
6. Run the Django server `python manage.py runserver`.
7. Access the application in your web browser at `http://127.0.0.1:8000/api/docs#/default`.

## Technologies Used

- Django
- Django Ninja
- Python
- aiohttp
- BeautifulSoup