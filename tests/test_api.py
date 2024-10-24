import pytest
from github import GithubException
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from app.main import app


repo_data_example = {
    "github_repo_url": "vladlevkovich/generate-message",
    "assigment_description": "Test description",
    "candidate_level": "junior"
}

repo_fail_data_example = {
    "github_repo_url": "vladlevkovich/invalid-repo",
    "assigment_description": "Test description",
    "candidate_level": "junior"
}

mock_repo_data = [
    {
        'path': 'file1.py',
        'content': 'print("Hello World")'
    },
    {
        'path': 'file2.py',
        'content': 'def my_function(): pass'
    }
]

@pytest.fixture
def mock_parser():
    with patch('app.services.repo.GitHubRepoParser.read_file_content') as mock_read:
        mock_read.return_value = mock_repo_data
        yield mock_read


@pytest.mark.asyncio
async def test_code_review_success(mock_parser):
    transport = ASGITransport(app=app)
    with patch('app.services.gpt.check_code', return_value='Code review Passed'):
        async with AsyncClient(transport=transport, base_url='http://127.0.0.1:8000') as ac:
            response = await ac.post('/review', json=repo_data_example)
            assert response.status_code == 200
            assert 'message' in response.json()
            mock_parser.assert_called_once_with(repo_data_example['github_repo_url'])


@pytest.mark.asyncio
async def test_code_review_failure(mock_parser):
    mock_parser.return_value = []

    transport = ASGITransport(app=app)
    with patch('app.services.repo.GitHubRepoParser.get_repo', side_effect=GithubException):
        async with AsyncClient(transport=transport, base_url='http://127.0.0.1:8000') as client:
            response = await client.post('/review', json=repo_fail_data_example)
            data = response.json()
            print(response.json())
            print(response.content)
            print(response.status_code)
            assert data['status_code'] == 400
            assert 'detail' in response.json()
            assert mock_parser.called

