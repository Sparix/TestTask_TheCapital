from typing import List

from ninja import NinjaAPI, Router
from matrix_api.matrix import get_matrix, parse_matrix
from matrix_api.models import Matrix

api = NinjaAPI()
router = Router()

URL = (
    "https://raw.githubusercontent.com/"
    "Real-Estate-THE-Capital/"
    "python-assignment/main/matrix.txt"
)


@router.get("/matrix-traversal-url/", response=List[int])
async def traverse_matrix_by_url(request, url: str = URL) -> List[int]:
    matrix = await get_matrix(url)
    return matrix


@router.get("/matrix-traversal-db/", response=List[List[int]])
def traverse_matrix_db(request) -> list[list[int]]:
    all_matrix = Matrix.objects.all()
    traverse = [parse_matrix(matrix.matrix_text) for matrix in all_matrix]
    return traverse
