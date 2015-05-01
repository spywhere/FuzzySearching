class Fuzzy:
    def __init__(self, collections=None):
        self.collections = collections or []

    def search(self, term, limit=10):
        result = []
        for text in self.collections:
            score = self.calculate_score(term, text)
            if score is None:
                continue
            result.append((score, text))
        result = sorted(result, key=lambda x: x[0], reverse=True)

        output = []
        while len(result) > 0 and len(output) < limit:
            output.append(result[0][1])
            result = result[1:]
        return (output, len(result) - len(output))

    def calculate_score(self, term, text):
        if len(text) < len(term):
            return None
        score = (len(term) - len(text)) * 0.1
        index = 0
        for c in term:
            if c == text[index]:
                score += 1
            index += 1
        return score
