## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. The frontend server runs at http://localhost:3000/.
- Authentication: This version of the application does not require authentication or API keys. 
- This is a website to manage the trivia app and play the trivia game.
- You should already have python2,pip and node installed on your development machine.
- Install the dependencies:
       pip install -r requirements.txt
- Run the development backend server:
       export FLASK_APP=flaskr
       export FLASK_ENV=development # enables debug mode
       flask run
- Run the frontend server on http://localhost:3000/
       npm install //only once
       npm start
- All the endpoint test cases are available in ./trivia/trivia_app/starter/backend/test_flaskr.py . how to run the tests
       python ./trivia/trivia_app/starter/backend/test_flaskr.py 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: bad request
- 404: resource not found
- 422: unprocessable
- 405: method not allowed

### Endpoints 
#### GET /categories
- General:
    - Returns a list of categories of the trivia questioins and success value.
    - Sample: `curl http://127.0.0.1:5000/categories`

``` {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports",
        "7": "Economics",
     },
     "success": true
    }
```

#### GET /questions
- General:
    - Returns a list of current questions for trivia, success value, all categories and total number of questions,
    - The list of questions are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions?page=2`
``` {
    'success': True,
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Economics",
    "8": "Craft",
    "9": "Temp",
    "10": "Temp"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": 4
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "rating": 4
    }, 
    ...]
    'total_questions': 25
    }
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted book, success value
- `curl -X DELETE http://127.0.0.1:5000/questions/2`
```
{
  "deleted": 52,
  "success": true
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question,answer,category,difficult and rating. Returns the id of the created question and success value
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{\"question\":\"Where is statue of liberty located\", \"answer\":\"xyz\", \"category\":\"3\", \"difficulty\":\"3\", \"rating\":\"4\"}"`

```{
  "created": 75,
  "success": true
}
```

#### POST /questions_search
- General:
    - Searches question using the submitted search term. Returns the  success value and current questions and total number of questions.
    - The list of questions are paginated in groups of 10. Include a request argument "page" to choose page number, starting from 1. 
- `curl http://127.0.0.1:5000/questions_search -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"Tom\"}"`

```{
   "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": 4
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### GET /categories/<int:cat_id>/questions
- General:
    - Gets the questions of the given category id and page number. Returns success value,current questions based on the given category,total number of questions and                          current_category
- `curl http://127.0.0.1:5000/categories/3/questions?page=1`
```
{
  "current_category": 3,
  "questions": [
    {
      "answer": "xyz",
      "category": 3,
      "difficulty": 3,
      "id": 75,
      "question": "Where is statue of liberty located",
      "rating": 4
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "rating": 4
    },
    ...]
  "success": true,
  "total_questions": 7
}
```

#### POST /quizzes
- General:
    - Gets a random question based on the given category and previous questions. Category id of 0 means gets a random question out of all the questions. 
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"quiz_category\":{\"type\":\"Science\", \"id\":\"1\"}, \"previous_questions\":[22,21]}"`

```{
   "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?",
    "rating": 4
   },
   "success": true
}
```

#### POST /categories
- General:
    - Creates a new category. Returns the id of the created category and success value
- `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d "{\"categoryName\":\"Anatomy\"}"`

```{
   "created": 11,
   "success": true
}
```
