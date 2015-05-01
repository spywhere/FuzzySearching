import time
from fuzzy import Fuzzy


def generate_collections():
    with open("collections.txt", "r") as file:
        return [line.strip() for line in file.readlines()]
    return []


def run():
    limit = 20
    collection = generate_collections()
    fuzzy = Fuzzy(collection)
    print(fuzzy)
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
        has_more = len(result) > limit
        result = result[:limit]
        for text in result:
            print("%s%s [%s]" % (" " * 2, text[1], text[0]))
        if has_more:
            print(" " * 2 + "...")


if __name__ == "__main__":
    run()
