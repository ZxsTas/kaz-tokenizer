# -*- coding: utf-8 -*-
"""
Optimized Kazakh Tokenizer - O(n) performance
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum


class MorphType(Enum):
    ROOT = "root"
    DERIV = "deriv"
    INFL = "infl"


@dataclass
class Morpheme:
    form: str
    type: MorphType
    gloss: str = ""


class Harmony:
    FRONT = frozenset({'е', 'і', 'ө', 'ү'})
    BACK = frozenset({'а', 'ы', 'о', 'у'})
    VOWELS = FRONT | BACK
    
    @staticmethod
    def last_class(word: str) -> str:
        for v in reversed(word.lower()):
            if v in Harmony.FRONT:
                return "front"
            if v in Harmony.BACK:
                return "back"
        return "neutral"
    
    @staticmethod
    def check(root: str, suffix: str, root_class: str) -> bool:
        sfx_v = next((c.lower() for c in suffix if c.lower() in Harmony.VOWELS), None)
        if not sfx_v:
            return True
        if root_class == "front":
            return sfx_v in Harmony.FRONT
        if root_class == "back":
            return sfx_v in Harmony.BACK
        return True


class Morphology:
    SUFFIXES = {
        "-шы/-ші": ("agent", True),
        "-лық/-лік": ("quality", True),
        "-ша/-ше": ("dim", True),
        "-ңғы/-нғы": ("rel", True),
        "-ын/-ін/-ун/-үн": ("collect", True),
        "-лар/-лер": ("pl", False),
        "-ым/-ім/-ум/-үм": ("poss.1sg", False),
        "-ның/-нің": ("gen", False),
        "-ға/-ге/-қа/-ке": ("dat", False),
        "-да/-де/-та/-те": ("loc", False),
        "-дан/-ден": ("abl", False),
        "-ты/-ті/-ды/-ді": ("acc", False),
        "-та/-те": ("hab", True),
        "-ғал/-гел": ("incp", True),
        "-ыл/-іл": ("pass", True),
        "-ды/-ді": ("past", False),
        "-жы/-жі": ("cont", False),
        "-май/-мей": ("neg", False),
        "-ай/-ей": ("pres", False),
    }
    
    SUFFIX_VARIANTS: Dict[str, Tuple[str, bool]] = {}
    
    @classmethod
    def init_variants(cls):
        for key, (gloss, is_deriv) in cls.SUFFIXES.items():
            for variant in key.split('/'):
                cls.SUFFIX_VARIANTS[variant] = (gloss, is_deriv)


class Tokenizer:
    WORD_PATTERN = re.compile(r'\b[а-яғқңөәүіa-z]+\b', re.IGNORECASE)
    
    def __init__(self):
        Morphology.init_variants()
        self.variants = Morphology.SUFFIX_VARIANTS
        self.sorted_variants = sorted(self.variants.keys(), key=len, reverse=True)
    
    def segment(self, word: str) -> List[Morpheme]:
        morphs = []
        rem = word.lower()
        root_class = None
        
        while len(rem) > 2:
            found = False
            for variant in self.sorted_variants:
                if rem.endswith(variant):
                    root = rem[:-len(variant)]
                    
                    if not root_class:
                        root_class = Harmony.last_class(root)
                    
                    if Harmony.check(root, variant, root_class):
                        gloss, is_deriv = self.variants[variant]
                        morphs.append(Morpheme(
                            form=variant,
                            type=MorphType.DERIV if is_deriv else MorphType.INFL,
                            gloss=gloss
                        ))
                        rem = root
                        root_class = Harmony.last_class(rem)
                        found = True
                        break
            
            if not found:
                break
        
        if rem:
            morphs.append(Morpheme(form=rem, type=MorphType.ROOT))
        
        return list(reversed(morphs))
    
    def analyze(self, word: str) -> Dict:
        morph = self.segment(word)
        return {
            "word": word,
            "structure": " + ".join([m.form for m in morph]),
            "morphemes": [(m.form, m.type.value, m.gloss) for m in morph],
            "root": morph[0].form if morph and morph[0].type == MorphType.ROOT else "",
        }
    
    def batch(self, text: str) -> List[Dict]:
        words = self.WORD_PATTERN.findall(text.lower())
        return [self.analyze(w) for w in words]
    
    def batch_fast(self, texts: List[str]) -> List[List[Dict]]:
        return [self.batch(text) for text in texts]


if __name__ == "__main__":
    tok = Tokenizer()
    
    test_words = [
        "оқушыларының",
        "мектептерінде",
        "қалайсың",
        "ойната",
        "балаларын",
    ]
    
    for w in test_words:
        r = tok.analyze(w)
        print(f"{w:20} {r['structure']}")
        for f, t, g in r['morphemes']:
            print(f"  {f:12} {t:8} {g}")
