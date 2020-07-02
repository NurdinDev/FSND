# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Reference

### Gating Started

- Base URL: At present this app can only run locally and is not hosted, the backend app is hosted at `http://127.0.0.1:5000`, which set as a proxy in the frontend configuration.
  \_ Authentication: this version of the application doesn't required authentication or API key.

### Error Handling

- Errors are returned as JSON object in the following format.

```
{
  'success': False,
  'error': 400,
  'message': "bad request"

}
```

- 404: Resource Not Found
- 422: Not Processable

### End Points

GET `/categories`

- General

  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

- Sample: `curl http://127.0.0.1:5000/categories`
- Test: Passed

```
{
  '1' : "Science",
  '2' : "Art",
  '3' : "Geography",
  '4' : "History",
  '5' : "Entertainment",
  '6' : "Sports"
}
```

GET `/categories/<int:category_id>/questions`

- General
  - Fetches a dictionary of questions in particular category
- Sample: `curl http://127.0.0.1:5000/categories/3/questions`
- Test: Passed

```
{
    "questions":[
        {
            "answer":"Agra",
            "category":3,
            "difficulty":2,
            "id":15,
            "question":"The Taj Mahal is located in which Indian city?"
        },
        {
            "answer":"Haiti",
            "category":3,
            "difficulty":3,
            "id":26,
            "question":"What country shares the island with Dominican Republic?"
        }
    ],
    "success":true
}
```

GET `/questions`

- General
  - Fetch a directory of questions
- Sample: `curl http://127.0.0.1:5000/questions`
- Test: Passed

```
{
    "categories":{
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
    "current_category":"hard coded category",
    "questions":[
        {
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        @INFO 8 more ...
    ],
    "success":true,
    "total_questions":19
}
```

DELETE `/question/<int:question_id>`

- General
  - Delete a particular question with this id that provided in the url
  - Returns 404 if the id not exist or wrong
  - Return deleted Id and list of question like in GET `/question` api.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/13`
- Test: Passed

```
{
    "deleted": 13,
    "questions":[
        {
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
      @INFO 8 more...
    ],
    "success":true,
    "total_questions":18
}
```

POST `/questions`

- General
  - Create new question
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"test question?","answer":"test answer", "category":1, "difficulty":3}'`
- Test: Passed

```
{
    "question":"test question?",
    "success":true
}
```

POST `/questions`

- General
  - Do a search in questions based on a search term
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm":"soccer"}'`
- Test: Passed

```
{
    "current_category":"",
    "questions":[
        {
            "answer":"Brazil",
            "category":6,
            "difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success":true,
    "total_questions":2
}
```

POST `/quizzes`

- General
  - Get random and not repeated question inside particular category or inside all the categories
- Sample: `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}'`
- Test: Passed

```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
