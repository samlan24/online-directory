# RentNest Directory

## Overview

**RentNest Directory** is a web-based platform that allows users to search for real estate agents, movers, and cleaners based on name, location, and ratings. The platform enables users to browse agent profiles, rate agents, send messages, and book appointments. You can read the development journey here > https://withallan.hashnode.dev/the-journey-behind-creating-rentnest-lessons-learned
Here's a demonstration of how it works: https://samlan24.github.io/online-directory/

## Features

- **Search Functionality**: Find agents by name, location, or rating.
- **Agent Profiles**: View detailed profiles with descriptions, locations, and average ratings.
- **Messaging**: Send messages directly to agents from their profiles.
- **Ratings System**: Rate agents and filter search results by average ratings.
- **Appointments**: Book appointments with agents directly from their profile pages.

## Technologies Used

- **Backend**: Flask (Python), Flask-SQLAlchemy
- **Frontend**: Bootstrap, Jinja2, HTML/CSS
- **Database**: MySQL
- **Version Control**: Git & GItHub

## Setup Instructions

### 1. **Fork the Repository**

Go to the GitHub page of the repository and click the "`Fork`" button in the top-right corner to create your own copy of the repository.


### 2. **Clone the Repository**

```
git clone https://github.com/your-username/online-directory.git

cd online-directory
```
#### Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Frontend(HTML/CSS/JS)
    participant Backend(FLASK)
    participant Database(MySQL)

    User->>Frontend: Interacts with UI
    Frontend->>Backend: Sends HTTP request
    Backend->>Database: Queries data via SQLAlchemy
    Database-->>Backend: Returns data
    Backend-->>Frontend: Renders template with data
    Frontend-->>User: Displays data
```

### 2. **Set Up a Virtual Environment**

Before installing the dependencies, it’s recommended to create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. **Install Dependencies**

Install all the necessary dependencies using the `requirements.txt` file:

```
pip install -r requirements.txt
```

### 4. **Create and Configure a `.env` File**

You need to set environment variables for the project. In the root directory of your project, create a `.env` file with the following content:

```
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

# Database Configuration
SQLALCHEMY_DATABASE_URI=mysql+mysqldb://username:password@localhost/your_database_name
```

Replace `username`, `password`, and `your_database_name` with your actual MySQL credentials. The secret key can be any random string.

### 5. **Initialize the Database**

You need to initialize and migrate the database schema for your application:

```
flask db init
flask db migrate
flask db upgrade
```
This will set up your MySQL database with the required tables.

### 6. **Running the Application**

After setting up the database and configurations, you can run the Flask application using:

```
flask run
```
Open `http://127.0.0.1:5000/` in your browser to access the Home Helper Directory.

### 7. **Testing the Application**

To test if the search functionality and filters are working correctly, try searching for agents by their name, location, or rating from the find-agent page. You can also create agent profiles and rate them from the agent details page.


## License

This project is licensed under the MIT License.