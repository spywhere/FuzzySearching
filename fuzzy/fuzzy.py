class Fuzzy:
    def __init__(self, collections=None):
        self.collections = collections or []
        self.weight = {
            # + Matched character
            "match": 1,
            # + Exact position
            "exact": 1.5,
            # - Offset character
            "offset": 1,
            # - Mismatched character
            "mismatch": 1,
            # - Casing mismatch
            "case_mismatch": -1,
            # - Target > Source length
            "length": 0,
            # - Unmatched source character
            "source_unmatch": 1,
            # - Unmatched target character
            "target_unmatch": 1,
            # + Match completion reward
            "complete_reward": 0
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
            score, matches = self.calculate_score(term, text)
            if score is None:
                continue
            result.append((score, text, matches))
        result = sorted(result, key=lambda x: x[0], reverse=True)

        self.last_result = []
        while len(result) > 0 and (limit <= 0 or len(self.last_result) < limit):
            self.last_result.append(result[0])
            result = result[1:]
        return self.last_result

    def calculate_score(self, term, text):
        if len(text) < len(term):
            return (None, [])
        score = (len(term) - len(text)) * self.weight["length"]
        source = 0
        target = 0
        last_match = 0
        matches = []
        while source < len(term) and last_match < len(text):
            if term[source] and term[source] not in text[last_match:]:
                return (None, [])
            if term[source].lower() == text[target].lower():
                if term[source] != text[target]:
                    score -= self.weight["case_mismatch"]
                if source == target:
                    score += self.weight["exact"]
                score += self.weight["match"]
                score -= abs(source - target) * self.weight["offset"]
                source += 1
                matches.append(target)
                last_match = target
            else:
                score -= self.weight["mismatch"]
            target += 1
            if target >= len(text):
                source += 1
                target = last_match
        score -= (len(term) - source) * self.weight["source_unmatch"]
        score -= (len(text) - last_match) * self.weight["target_unmatch"]
        if source == len(term) and last_match == len(text):
            score += self.weight["complete_reward"]
        return (score, matches)

    def __str__(self):
        return "Fuzzy [%s in collections]" % (len(self.collections))
