import json
import re
import unicodedata
from rapidfuzz import fuzz

def normalize_text(text: str) -> str:
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

class KnowledgeBase:
    def __init__(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        for item in self.data:
            item['norm_question'] = normalize_text(item['question'])

    def get_answer(self, question: str) -> str:
        norm_question = normalize_text(question)

        best_score = 0
        best_answer = None
        for item in self.data:
            score = fuzz.ratio(norm_question, item['norm_question'])
            if score > best_score:
                best_score = score
                best_answer = item['answer']

        if best_score > 60:
            return best_answer
        else:
            return self._default_response()

    def _default_response(self) -> str:
        # Získáme přehled otázek (např. první věta každé otázky nebo klíčová slova)
        topics = [item['question'] for item in self.data[:5]]  # vezmeme prvních 5 otázek jako přehled
        topics_list = '\n - '.join(topics)
        return ("Omlouvám se, tuto otázku nechápu úplně přesně.\n"
                "Mohu vám pomoci s otázkami týkajícími se například:\n - " + topics_list)
