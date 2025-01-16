Tournament API
This is a Django-based project with token authentication using Django Rest Framework (DRF). The project is designed to provide secure endpoints for managing data related to players, tournaments, and matches.


Features
Token-based authentication using JSON Web Tokens (JWT).
CRUD operations for Player, Tournament, and Matches models.
Filtering and searching capabilities.


Setting Up the Project
1. Clone the Repository
First, clone the repository to your local machine:
git clone https://github.com/yourusername/your-project.git
cd your-project

2. Create a Virtual Environment
Create and activate a virtual environment to isolate project dependencies:
For macOS/Linux:
python3 -m venv env
source env/bin/activate
For Windows:
python -m venv env
.\env\Scripts\activate

3. Install Dependencies
Install the required dependencies using pip:
pip install -r requirements.txt


Create a Superuser
To access the admin panel and create players, tournaments, or matches, you'll need to create a superuser. Run the following command:
python manage.py createsuperuser


Run the Development Server
To run the development server, use:
python manage.py runserver
By default, the server will run on http://127.0.0.1:8000/.


Authentication (Token-based Authentication)
1. Obtain a Token
To authenticate API requests, you need to obtain a JWT token.

Make a POST request to the /token/ endpoint with your username and password:

Endpoint: http://127.0.0.1:8000/api/token/

Request body (JSON):
{
  "username": "yourusername",
  "password": "yourpassword"
}
Response (JSON):
{
  "access": "your-access-token",
  "refresh": "your-refresh-token"
}

2. Using the Token in API Requests
Once you have the access token, you can use it to authenticate your requests by adding an Authorization header.

Example using Postman or cURL:

POSTMAN:
Set the request type to GET or POST.
Under the Headers section, add:
Key: Authorization
Value: Bearer your-access-token

3. Token Expiration and Refreshing the Token
Tokens are valid for a limited time (by default, 5 minutes for the access token).

When the access token expires, use the refresh token to get a new access token.

Refresh token endpoint:

POST to /token/refresh/ with the refresh token:
{
  "refresh": "your-refresh-token"
}
The response will provide a new access token.


API Endpoints
Here are the available API endpoints:

Players
GET /players/: List all players (read access for everyone).
POST /players/: Create a new player (admin only).
GET /players/{id}/: Retrieve a specific player (read access for everyone).
PUT /players/{id}/: Update an existing player (admin only).
DELETE /players/{id}/: Delete a player (admin only).
Tournaments
GET /tournaments/: List all tournaments (read access for everyone).
POST /tournaments/: Create a new tournament (admin only).
GET /tournaments/{id}/: Retrieve a specific tournament (read access for everyone).
PUT /tournaments/{id}/: Update an existing tournament (admin only).
DELETE /tournaments/{id}/: Delete a tournament (admin only).
Matches
GET /matches/: List all matches (read access for everyone).
POST /matches/: Create a new match (admin only).
GET /matches/{id}/: Retrieve a specific match (read access for everyone).
PUT /matches/{id}/: Update an existing match (admin only).
DELETE /matches/{id}/: Delete a match (admin only).


End of README
This template gives clear and concise instructions for setting up and using your token-authenticated Django API project. You can modify any part of it according to your actual project details and structure.