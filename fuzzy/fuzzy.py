class Fuzzy:
    def __init__(self, collections=None):
        self.collections = collections or []
        self.weight = {
            "match": 1,
            "offset": 1,
            "mismatch": 1,
            "length": 0
        }
        self.last_term = ""
        self.last_result = []

    def search(self, term, limit=0):
        collections = self.collections
        if self.last_term and term.startswith(self.last_term):
            collections = [x[1] for x in self.last_result]
        self.last_term = term

        result = []
        for text in collections:
            score = self.calculate_score(term, text)
            if score is None:
                continue
            result.append((score, text))
        result = sorted(result, key=lambda x: x[0], reverse=True)

        total_result = len(result)
        self.last_result = []
        while len(result) > 0 and (limit <= 0 or len(self.last_result) < limit):
            self.last_result.append(result[0])
            result = result[1:]
        return (self.last_result, total_result - len(self.last_result))

    def calculate_score(self, term, text):
        if len(text) < len(term):
            return None
        score = (len(term) - len(text)) * self.weight["length"]
        source = 0
        target = 0
        last_match = 0
        while source < len(term):
            if term[source] and term[target:] not in text:
                return None
            if term[source] == text[target]:
                score += self.weight["match"]
                score -= abs(source - target) * self.weight["offset"]
                source += 1
                last_match = target
            score -= self.weight["mismatch"]
            target += 1
            if target >= len(text):
                source += 1
                target = last_match
        return score

    def __str__(self):
        return "Fuzzy [%s in collections]" % (len(self.collections))
