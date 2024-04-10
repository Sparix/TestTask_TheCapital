import aiohttp
from bs4 import BeautifulSoup
from typing import List


async def get_matrix(url: str) -> List[int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Page Error. Status code: {response.status}")
                return []
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            matrix = parse_matrix(soup.text)
            print(matrix)
            return matrix


def parse_matrix(matrix: str) -> List[int]:
    matrix_list = []
    for line in matrix.split("\n"):
        numbers = [int(num) for num in line.split() if num.isdigit()]
        if numbers:
            matrix_list.append(numbers)
    return traverse_matrix(matrix_list)


def traverse_matrix(matrix: List[List[int]]) -> List[int]:
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    count = 0
    total_elements = num_rows * num_cols
    current_row = 0
    current_col = 0
    result = []

    while current_row < num_rows and current_col < num_cols:
        if count == total_elements:
            break

        # Traverse the current column from top to bottom
        for i in range(current_row, num_rows):
            result.append(matrix[i][current_col])
            count += 1
        current_col += 1

        if count == total_elements:
            break

        # Traverse the last row from left to right
        for i in range(current_col, num_cols):
            result.append(matrix[num_rows - 1][i])
            count += 1
        num_rows -= 1

        if count == total_elements:
            break

        # Traverse the last column from bottom to top
        if current_row < num_rows:
            for i in range(num_rows - 1, current_row - 1, -1):
                result.append(matrix[i][num_cols - 1])
                count += 1
            num_cols -= 1

        if count == total_elements:
            break

        # Traverse the first row from right to left
        if current_col < num_cols:
            for i in range(num_cols - 1, current_col - 1, -1):
                result.append(matrix[current_row][i])
                count += 1
            current_row += 1

    return result
