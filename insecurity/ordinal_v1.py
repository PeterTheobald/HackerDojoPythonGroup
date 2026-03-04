
def ordinal(n: int) -> str:
    """Return an integer as its ordinal string (1st, 2nd, 3rd, etc.)."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    abs_n = abs(n)
    last_two = abs_n % 100

    if 11 <= last_two <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(abs_n % 10, "th")

    return f"{n}{suffix}"

if __name__ == '__main__':
    print(1,ordinal(1))    # "1st"
    print(2,ordinal(2))    # "2nd"
    print(3,ordinal(3))    # "3rd"
    print(4,ordinal(4))    # "4th"
    print(11,ordinal(11))   # "11th"
    print(22,ordinal(22))   # "22nd"
    print(113,ordinal(113))  # "113th"
