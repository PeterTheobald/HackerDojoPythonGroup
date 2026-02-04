def clean_names(name):
    """
    Removes trailing whitespace and capitalizes the name.

    >>> clean_names("  peter  ")
    'Peter'
    >>> clean_names("JOSHUA")
    'Joshua'
    """
    return name.strip().capitalize()

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True) # Set verbose=True for detailed output
