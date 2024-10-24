from fastapi import APIRouter, HTTPException
from app.schemas.schema import RepoSchema
from app.services.repo import r
from app.services.gpt import check_code
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post('/review')
async def code_review(data: RepoSchema) -> dict:
    try:
        repo_data = r.read_file_content(data.github_repo_url)
        if not repo_data:
            raise HTTPException(detail="Repository not found", status_code=404)
        file_path = ''
        code = ''
        structure = ''
        for i in range(len(repo_data)):
            code = repo_data[i]['content']
            structure.join(repo_data[i]['path'])
        res = check_code(data.assigment_description, structure, file_path, code, data.candidate_level)
        return {'message': res}
    except Exception as e:
        logger.error(f'{e}')
        raise HTTPException(
            detail=str(e),
            status_code=400
        )
