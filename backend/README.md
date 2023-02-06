# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: 
  - An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
  - A boolean with `success` key and value of `True`
  - A number with `total_categories` key that represents the total count of available categories

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_categories": 6
}
```

`GET '/api/v1.0/questions'`

- Fetches:
  - a list of 10 questions per page
- Request params:
    - `page`: the requested page
    - `category`: category id used to filted questions by category
    - Exampe: `/api/v1.0/questions?page=1&category=2`
- Returns: 
  - An object with a `categories` key, that contains an object of `id: category_string` key: value pairs.
  - An array of 10 questions, each containing an object with `question: question_string`, `answer: answer_string`, `category: category_id`, `difficulty: difficulty_number`, `id: id_number` key: value pairs
  - A boolean with `success` key and value of `True`
  - A number with a `total_questions` key that represents the total count of all the questions

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        ...
    ],
    "success": true,
    "total_questions": 56
}
```

`DELETE '/api/v1.0/questions/<int:question_id>'`

- Deletes a question by id:
  - `question_id`: Integer that represents the question id

- Returns: 
  - An object with a `categories` key, that contains an object of `id: category_string` key: value pairs.
  - A number with a `deleted` key that represents id of the question that was deleted.
  - An array of 10 questions, each containing an object with `question: question_string`, `answer: answer_string`, `category: category_id`, `difficulty: difficulty_number`, `id: id_number` key: value pairs
  - A boolean with `success` key and value of `True`
  - A number with a `total_questions` key that represents the total count of all the questions

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "deleted": 74,
  "questions": [
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    ...
  ],
  "success": true,
  "total_questions": 55
}
```

`POST '/api/v1.0/questions/<int:question_id>'`

- Inserts a new question in the app
- Request Arguments:
  - `question`: String that contains the question
  - `answer`: String that contains the answer
  - `difficulty`: Number that marks the difficulty of the question
  - `category`: Number that represents the id of the category that the question is grouped in

- Returns: 
  - An object with a `categories` key, that contains an object of `id: category_string` key: value pairs.
  - A number with a `created` key that represents id of the question that was added.
  - An array of 10 questions, each containing an object with `question: question_string`, `answer: answer_string`, `category: category_id`, `difficulty: difficulty_number`, `id: id_number` key: value pairs
  - A boolean with `success` key and value of `True`
  - A number with a `total_questions` key that represents the total count of all the questions

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "created": 76,
    "questions": [
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        ...
    ],
    "success": true,
    "total_questions": 56
}
```

`POST '/api/v1.0/questions/<int:question_id>'`

- Search questions by their `question` value
- Request Arguments:
  - `search_term`: String that contains the search term

- Returns: 
  - An array of 10 questions, each containing an object with `question: question_string`, `answer: answer_string`, `category: category_id`, `difficulty: difficulty_number`, `id: id_number` key: value pairs
  - A boolean with `success` key and value of `True`
  - A number with a `total_questions` key that represents the total count of all the questions

```json
{
    "questions": [
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Marcellus Gilmore Edson",
            "category": 3,
            "difficulty": 4,
            "id": 24,
            "question": "Who invented peanut butter?"
        },
        ...
    ],
    "success": true,
    "total_questions": 11
}
```

`POST '/api/v1.0/quizzes'`

- Runs the trivia app
- Request Arguments:
  - `previous_questions`: List of previous question id's
  - `quiz_category`: Dictionary that contains a specific category data:
     - `id`: Category id
     - `type`: String containing the category title
  - if no category is selected in the app the `quiz_category` values should be `"id": 0` and `"type": "click"`

- Returns: 
  - An array of integers with `previous_questions` key that contains the id's of the previous questions in the trivia
  - An object with `question` with `question: question_string`, `answer: answer_string`, `category: category_id`, `id: id_number` key: value pairs
  - A boolean with `success` key and value of `True`

```json
{
    "previous_questions": [
        53
    ],
    "question": {
        "answer": "Marcellus Gilmore Edson",
        "category": 1,
        "id": 28,
        "question": "Who invented peanut butter?"
    },
    "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
