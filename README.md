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

