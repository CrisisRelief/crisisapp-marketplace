import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
from typing import List

from src.patterns import accommodation as acc
from src.patterns import pickups as pickup

nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)
matched_sents = []

def collect_sents(matcher, doc:spacy.tokens.doc.Doc, i:int, matches:List[Matcher]) -> List:
    """
            Args:
    """
    match_id, start, end = matches[i]
    # Matched span
    span = doc[start:end]
    # Sentence containing matched span
    sent = span.sent

    # get the match span by ofsetting the start and end of the span with the
    # start and end of the sentence in the doc
    string_id = nlp.vocab.strings[match_id]
    start_span = span.start_char - sent.start_char,
    end_span =  span.end_char - sent.start_char,

    match_ents = [{
        "span" : str(span),
        "label": string_id
    }]
    matched_sents.append({"text": sent.text, "ents": match_ents})

    return

def add_patterns(pattern_types:List) -> None:
    for pattern_type in pattern_types:
        if pattern_type is "accommodation":
            for pattern in acc.patterns:
                matcher.add(pattern['LABEL'], collect_sents, pattern['pattern'])

        if pattern_type is "pickups":
            for pattern in pickup.patterns:
                matcher.add(pattern['LABEL'], collect_sents, pattern['pattern'])
                
    return

def detect_patterns(content:List) -> List:
    """
    """
    global matched_sents
    for txt in content:
        doc = nlp(txt)
        matches = matcher(doc)

    op = matched_sents
    matched_sents = []
    return op

add_patterns(["pickups"])

