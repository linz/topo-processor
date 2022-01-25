def test() -> None:

    n: float = -41.28509

    if isinstance(n, float):
        print("it's a float.")
    elif isinstance(n, int):
        print("it's an int.")
    print(n)


test()
