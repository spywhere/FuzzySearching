import time
from fuzzy import Fuzzy


def generate_collections(starts=""):
    with open("collections.txt", "r") as file:
        return [
            line.strip()
            for line in file.readlines()
            if line.startswith(starts)
        ]
    return []


def format_text(text, matches):
    index = 0
    output = ""
    for c in text:
        if index in matches:
            output += c.upper()
        else:
            output += c
        index += 1
    return output


def run():
    limit = 10
    collection = generate_collections()
    fuzzy = Fuzzy(collection)
    print(fuzzy)
    while True:
        search = input("> ")
        if not search:
            return
        start_time = time.time()
        result = fuzzy.search(search)
        has_more = len(result) - limit
        if has_more == 1:
            limit += 1
        print("\"%s\" [%s of %s results (%.6f seconds)]" % (
            search,
            min(limit, len(result)),
            len(result),
            time.time() - start_time
        ))
        result = result[:limit]
        for text in result:
            print("%s[%8.2f] %s" % (
                " " * 2,
                text[0],
                format_text(text[1], text[2])
            ))
        if has_more > 1:
            print(" " * 2 + "...")


if __name__ == "__main__":
    run()
