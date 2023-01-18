# Shake - Python Engineer Task

This project is a task for the interviewing process of Shake. The FastAPI framework was used to create an API with 3 endpoints ("/convert", "/currencies", "/history"), each one protected with an API key. The structure of the project is built so the functionality of the app can be easily extended. It is also setup in a way that development/production environments could be added. I've documented the projects functions with docstrings and type annotations to make the code easily understandable. A Free MongoDB server is used to store historical conversion data.

## Prerequisites
- Python 3.10+

## Installing
1. Create a virtual environment: `python -m venv .venv`
2. Activate the virtual environment: `. ./venv/bin/activate`
3. Install all dependencies: `pip install -r requirements.txt`

## Usage
1. Create a file called .secrets.toml and paste the contents I will send to your email (so the passwords won't be on display on github).
2. To start the app you can use the command: `make api`

## Comments
- There could be improvements made, such as better error handling when fetching data from the wiseAPI, but due to the time limit of 4 hours, the current implementation is sufficient to demonstrate my skills.
- The API Key auth was made in a simple manner, if the application was bigger with multiple users, the logic implemented would have been more complex.
- No unit tests were implemented due to the time limit.

Please let me know if you have any question or if you want me to include any other specific information.
