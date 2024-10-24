from github import Auth, Github, BadCredentialsException, GithubException
from github import Repository
from dotenv import load_dotenv
from app.core.rd import rd
import os
import json
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class GitHubRepoParser:
    def __init__(self):
        self.git_auth = Auth.Token(os.getenv('GITHUB_KEY'))
        self.g = Github(auth=self.git_auth)

    def get_repo(self, repo_name: str):
        try:
            return self.g.get_repo(repo_name)
        except BadCredentialsException:
            logger.error('Invalid GitHub credentials')
            raise
        except GithubException as e:
            logger.error(f'Failed to get repo {repo_name}: {e}')
            raise

    def get_repo_content(self, repo_name: str):
        """отримуємо структуру проекта"""
        cache_key = f'github_repo_content:{repo_name}'
        cache_content = rd.get_data(cache_key)

        try:
            if cache_content:
                logger.info(f'Get cache for {cache_key}')
                return json.loads(cache_content)

            repo = self.get_repo(repo_name)
            contents = repo.get_contents('')
            items = []
            while contents:
                file_contents = contents.pop(0)
                if file_contents.type == 'dir':
                    contents.extend(repo.get_contents(file_contents.path))
                else:
                    items.append(file_contents.path)
            rd.cache(cache_key, items)
            logger.info(f'Cached content for {repo_name}')
            return items
        except GithubException as e:
            logger.error(f'Failed to get contents for repo {repo_name}: {e}')
            raise

    def read_file_content(self, repo_name: str, retries: int = 4):
        cache_key = f'github_repo_file_read:{repo_name}'
        cache_file_read = rd.get_data(cache_key)
        if cache_file_read:
            logger.info(f'Get cache for {cache_key}')
            return json.loads(cache_file_read)

        try:
            repo = self.get_repo(repo_name)
            repo_files = self.get_repo_content(repo_name)
            contents = []
            for repo_path in repo_files:
                file_content = repo.get_contents(repo_path).decoded_content.decode('utf-8')
                if len(file_content) == 0:
                    # якшо файл пустий
                    continue
                contents.append({
                    'path': repo_path,
                    'content': file_content
                })
            rd.cache(cache_key, contents)
            logger.info(f'Cached file read content for {repo_name}')
            return contents
        except GithubException as e:
            logger.error(f'Failed to read file content for repo {repo_name}: {e}')
            raise


r = GitHubRepoParser()
