from pydantic import BaseModel


class RepoSchema(BaseModel):
    assigment_description: str
    github_repo_url: str
    candidate_level: str
