import time
from fuzzy import Fuzzy


def generate_collections():
    with open("collections.txt", "r") as file:
        return [line.strip() for line in file.readlines()]
    return []


def run():
    collection = generate_collections()
    fuzzy = Fuzzy(collection)
    while True:
        search = input("> ")
        if not search:
            return
        start_time = time.time()
        result, remain = fuzzy.search(search)
        print("\"%s\" [%s of %s results (%.6f seconds)]" % (
            search,
            len(result),
            len(result) + remain,
            time.time() - start_time
        ))
        for text in result:
            print(" " * 2 + text)
        if remain:
            print(" " * 2 + "...")


if __name__ == "__main__":
    run()
