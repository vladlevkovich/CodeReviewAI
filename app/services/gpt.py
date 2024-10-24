from openai import OpenAI
from dotenv import load_dotenv
# from repo import GitHubRepoParser
import logging
import time
import os

load_dotenv()
logger = logging.getLogger(__name__)

def check_code(task_description: str, structure, file_path: str, code: str, candidate_level: str):
    max_retires = 5     # максимальна кількість спроб якщо запит не відбувся
    retry_attempts = 0
    wait_time = 10
    prompt = (
        f'Task description:\n'
        f'{task_description}\n\n'
        f'You are tasked to perform a detailed code review on a project with the following structure:\n'
        f'{structure}\n\n'
        f'Review the file {file_path}, which contains the following code:\n'
        f'{code}\n\n'
        f'This code was written by a {candidate_level} developer.\n'
        f'Focus on the following aspects:\n'
        f'- Code quality and maintainability\n'
        f'- Best practices for Python development\n'
        f'- Adherence to industry standards\n'
        f'- Potential improvements\n'
        f'- Suggestions for better performance or security\n\n'
        f'Return review results (text) in the following format:\n'
        f'1. **Found files**: Mention the files and their roles in the project structure.\n'
        f'2. **Downsides/Comments**: List issues or weak points in the code, including best practices not followed.\n'
        f'3. **Rating**: Rate the code on a scale of 1-5, where 5 is excellent for the {candidate_level} level.\n'
        f'4. **Conclusion**: Provide a summary of the candidate’s potential and an overall assessment.\n\n'
        f'Please make the review detailed and constructive.'
        f'Answer only in English'
    )
    while retry_attempts <= max_retires:
        try:
            response_blocks = {}
            client = OpenAI(api_key=os.getenv('OPENAI_KEY'))
            chat_completion = client.chat.completions.create(
                model='gpt-4-turbo',
                messages=[
                    {
                        'role': 'system', 'content': 'You are a helpful assistant.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                # stream=True # якшо true то відповідь виводиться поступово
            )
            response_blocks = {
                'found_files': '',
                'downsides_comments': '',
                'rating': '',
                'conclusion': ''
            }
            response = chat_completion.choices[0].message.content
            current_key = None
            for line in response.split('\n'):
                line = line.strip()
                if line.startswith('### 1. **Found Files**:'):
                    current_key = 'found_files'
                    response_blocks[current_key] = line.replace('### 1. **Found Files**:', '').strip()
                elif line.startswith('### 2. **Downsides/Comments**:'):
                    current_key = 'downsides_comments'
                    response_blocks[current_key] = line.replace('### 2. **Downsides/Comments**:', '').strip()
                elif line.startswith('### 3. **Rating**:'):
                    current_key = 'rating'
                    response_blocks[current_key] = line.replace('### 3. **Rating**:', '').strip()
                elif line.startswith('### 4. **Conclusion**:'):
                    current_key = 'conclusion'
                    response_blocks[current_key] = line.replace('### 4. **Conclusion**:', '').strip()
                elif current_key:
                    response_blocks[current_key] += ' ' + line
            return response_blocks
        except Exception as e:
            if 'rate_limit' in str(e).lower():
                logger.warning(f'Rate limit exceeded. Waiting for {wait_time} second before retrying')
                time.sleep(wait_time)
                wait_time *= 2
            else:
                retry_attempts += 1
                logger.error(f'Error: {e}')
                logger.warning(f'Retrying... Attempt {retry_attempts} of {max_retires}')
