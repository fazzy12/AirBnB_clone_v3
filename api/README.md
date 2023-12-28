# AirBnB Clone API (AirBnB_clone_v3)

This project is a backend API designed to replicate some functionalities of the popular AirBnB platform. Built on top of Flask, it provides RESTful endpoints to manage various aspects of the application such as users, places, cities, and more.

## Table of Contents
* [Introduction](#Introduction)
* [Features](#Features)
* [Setup and Installation](#Setup_and_Installation)
* [Usage](#Usage)
* [Endpoints](#Endpoints)
* [Contributing](#Contributing)
* [License](#License)
* [Introduction](#Introduction)

This API project serves as a foundation for an AirBnB-like application. It manages storage, user interactions, and content management through various endpoints and models.

## Features
CRUD operations for Users, Places, Cities, and more.
User authentication and authorization.
Search functionalities based on different criteria.

## Setup and Installation
To get started with this project:

1. Clone the repository:

```
git clone https://github.com/yourusername/AirBnB_clone_v3.git
```

2. Navigate to the project directory:

```
cd AirBnB_clone_v3
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Initialize and set up your database:

```
# Assuming you are using SQLite
python setup_db.py
```

5. Run the application:

```
flask run
```

## Usage
After setting up, you can start sending requests to the API using tools like `curl`, Postman, or any other `HTTP` client.

## Endpoints
**GET** `/cities/<city_id>/places`:
* **Description**: Retrieve all Place objects for a specific City.
* **Parameters**: `city_id` - ID of the city for which places are to be retrieved.

**GET** `/places/<place_id>`:
* **Description**: Retrieve a specific Place object.
* **Parameters**: `place_id` - ID of the place to be retrieved.

**DELETE** `/places/<place_id>`:
* **Description**: Delete a specific Place object.
* **Parameters**: place_id - ID of the place to be deleted.

**POST** `/cities/<city_id>/places`:
* **Description**: Create a new Place object.
* **Parameters**: city_id - ID of the city where the place is to be created.
* **Body**: JSON data containing the details of the new place, including `user_id` and name.

**PUT** `/places/<place_id>`:
* **Description**: Update a specific Place object.
* **Parameters**: place_id - ID of the place to be updated.
* **Body**: JSON data containing the fields to be updated for the place.

**POST** `/places_search`:
* **Description**: Search and retrieve Place objects based on provided criteria in the request body.
* **Body**: JSON data containing optional keys like states, cities, and amenities to filter the places.

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](#) file for details on our code of conduct, and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE.md](#) file for details.

