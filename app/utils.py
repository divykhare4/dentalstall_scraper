import random
import string


def generate_random_alphanumeric(length: int) -> str:
    """
    Generate a random alphanumeric string of the specified length.

    Args:
        length (int): Length of the generated string.

    Returns:
        str: Random alphanumeric string.
    """
    if length <= 0:
        raise ValueError("Length must be greater than 0.")

    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))
