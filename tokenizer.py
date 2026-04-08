# -*- coding: utf-8 -*-
"""
Kazakh Tokenizer - Morphological Analysis
Research-based: SozKZ (50K BPE), ByteKaz (byte-level), IS2AI corpus
"""

import re
from dataclasses import dataclass
from typing import List, Dict
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
    FRONT = {'е', 'і', 'ө', 'ү'}
    BACK = {'а', 'ы', 'о', 'у'}
    
    @staticmethod
    def last_class(word: str) -> str:
        for v in reversed(word.lower()):
            if v in Harmony.FRONT:
                return "front"
            if v in Harmony.BACK:
                return "back"
        return "neutral"
    
    @staticmethod
    def check(root: str, suffix: str) -> bool:
        cls = Harmony.last_class(root)
        sfx_v = [c.lower() for c in suffix if c.lower() in Harmony.FRONT | Harmony.BACK]
        if not sfx_v:
            return True
        return (cls == "front" and sfx_v[0] in Harmony.FRONT) or \
               (cls == "back" and sfx_v[0] in Harmony.BACK) or \
               cls == "neutral"


class Morphology:
    NOUN_DERIV = {
        "-шы/-ші": "agent",
        "-лық/-лік": "quality",
        "-ша/-ше": "dim",
        "-ңғы/-нғы": "rel",
        "-ын/-ін/-ун/-үн": "collect",
    }
    
    NOUN_INFL = {
        "-лар/-лер": "pl",
        "-ым/-ім/-ум/-үм": "poss.1sg",
        "-ның/-нің": "gen",
        "-ға/-ге/-қа/-ке": "dat",
        "-да/-де/-та/-те": "loc",
        "-дан/-ден": "abl",
        "-ты/-ті/-ды/-ді": "acc",
    }
    
    VERB_DERIV = {
        "-та/-те": "hab",
        "-ғал/-гел": "incp",
        "-ыл/-іл": "pass",
    }
    
    VERB_INFL = {
        "-ды/-ді": "past",
        "-жы/-жі": "cont",
        "-май/-мей": "neg",
        "-ай/-ей": "pres",
    }


class Tokenizer:
    def __init__(self):
        self.all_morph = {
            **Morphology.NOUN_DERIV,
            **Morphology.NOUN_INFL,
            **Morphology.VERB_DERIV,
            **Morphology.VERB_INFL
        }
    
    def segment(self, word: str) -> List[Morpheme]:
        morphs = []
        rem = word
        pos = 0
        
        sorted_m = sorted(self.all_morph.items(), 
                         key=lambda x: len(x[0].split('/')[0]), 
                         reverse=True)
        
        while len(rem) > 2:
            found = False
            
            for suffix_key, gloss in sorted_m:
                for var in suffix_key.split('/'): 
                    if rem.endswith(var):
                        root = rem[:-len(var)]
                        
                        if Harmony.check(root, var):
                            is_deriv = any(k in suffix_key for k in \
                                         list(Morphology.NOUN_DERIV.keys()) + \
                                         list(Morphology.VERB_DERIV.keys()))
                            
                            morphs.append(Morpheme(
                                form=var,
                                type=MorphType.DERIV if is_deriv else MorphType.INFL,
                                gloss=gloss
                            ))
                            rem = root
                            pos += 1
                            found = True
                            break
                
                if found:
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
        words = re.findall(r'\b[а-яғқңөәүіa-z]+\b', text.lower())
        return [self.analyze(w) for w in words]


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