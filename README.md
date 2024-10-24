# CodeReviewAI

Automatic code verification from GPT

## Зміст

- [Requirements](#requirements)
- [Installation](#installation)
- [Run](#run)
- [Testing](#testing)

## Requirements

Before you start, make sure you have what you need:

- Python 3.x
- Docker

## Installation

1. Clone:

   ```bash
   git clone https://github.com/vladlevkovich/CodeReviewAI.git
   cd repo```

2. Installation
```
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate  # Windows
```
```
poetry install
```
## Run
```
uvicorn app.main:app
```
## Testing
```
pytest
```

## Part 2

To scale an automated code review tool, I would consider a microservice architecture with
using asynchronous queues to process requests in the background. Caching data with Redis
will reduce the number of requests to the GitHub API, which will speed up the processing of repeated requests. 
To handle the use of the OpanAI API GitHub API, I would implement speed limiting mechanisms at the service level
and cache some of the responses.


