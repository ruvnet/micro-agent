import difflib

def apply_unified_diff(diff: str, file_content: str) -> str:
    """
    Apply a unified diff to the given file content.

    :param diff: The unified diff as a string.
    :param file_content: The original content of the file.
    :return: The modified file content after applying the diff.
    """
    diff_lines = diff.splitlines()
    result = list(difflib.restore(diff_lines, 2))
    if not result:
        raise ValueError("Failed to apply patch")
    return ''.join(result)
