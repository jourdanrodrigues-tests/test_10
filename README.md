# HelloFresh Test

## Style guides used

- [Git Commit Style Guide][git-commit-style-guide-link]
- [PEP8][pep8-link] with exceptions:
  - Line length of 120 characters tops
  - Required trailing comma 
- [The test section from _Django REST in Style_][test-style-guide-link]

## Notes

I never needed/wanted to build a bare Python server before this task.
Is quite interesting to see what the Frameworks that I often use do
underneath.

That said, I want to be completely honest regarding my approaches
(that you can check in commits messages/code) and knowledge sources.

Some of what's implemented in the request handler came from [here][gist-link].

## Instructions

### Running the server

Note: Whenever you run this command, the script for database schema creation is run for your convenience (of course, it
wouldn't work like this in production).

```bash
docker-compose up
```

If you don't want to bind the process to the current terminal, run the following:

```bash
docker-compose up -d
```

### Running the tests

```bash
docker-compose run --rm server pytest
```

### Creating database schema

```bash
docker-compose run --rm server python scripts/create_schema.py
```

### Loading mock data

```bash
docker-compose run --rm server python scripts/load_mock_data.py
```

### Useful cURL commands for API testing

Note: These cURL commands work after loading the mock data

```bash
curl -X GET http://localhost:8080/recipes/ # Retrieve recipe list

curl -X GET http://localhost:8080/recipes/1/ # Retrieve a recipe for the specified ID

curl -X POST \
  http://localhost:8080/recipes/ \
  -H 'Authorization: 1' \
  -H 'Content-Type: application/json' \
  -d '{"name": "A cool recipe", "difficulty": 1, "vegetarian": false, "preparation_time": 15}' # Create a recipe

curl -X PUT \
  http://localhost:8080/recipes/1/ \
  -H 'Authorization: 1' \
  -H 'Content-Type: application/json' \
  -d '{"name": "One fine recipe", "difficulty": 2, "vegetarian": true, "preparation_time": 14}' # Update a recipe with PUT

curl -X PATCH \
  http://localhost:8080/recipes/1/ \
  -H 'Authorization: 1' \
  -H 'Content-Type: application/json' \
  -d '{"name": "One fine recipe", "difficulty": 2, "vegetarian": false, "preparation_time": 13}' # Update a recipe with PATCH

curl -X DELETE http://localhost:8080/recipes/1/ -H 'Authorization: 1' # Delete a recipe

curl -X POST http://localhost:8080/recipes/1/rating/ -H 'Content-Type: application/json' -d '{"value": 2}' # Create a rating for a recipe
```

[pep8-link]: https://www.python.org/dev/peps/pep-0008/
[gist-link]: https://gist.github.com/tliron/8e9757180506f25e46d9
[test-style-guide-link]: https://github.com/jourdanrodrigues/django-rest-in-style#tests
[git-commit-style-guide-link]: https://github.com/slashsBin/styleguide-git-commit-message
