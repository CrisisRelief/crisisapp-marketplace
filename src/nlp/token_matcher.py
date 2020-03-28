import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy
from typing import List

from src.patterns import accommodation as acc

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
        "span" : span,
        "label": string_id
    }]
    matched_sents.append({"text": sent.text, "ents": match_ents})

    return

def add_patterns(pattern_types:List) -> None:
    for pattern_type in pattern_types:
        if pattern_type is "accommodation":
            for pattern in acc.patterns:
                matcher.add(pattern['LABEL'], collect_sents, pattern['pattern'])

    return

def detect_patterns(content:List) -> List:
    """
    """
    for txt in content:
        doc = nlp(txt)
        matches = matcher(doc)

    return matched_sents



messages = [
    "we will provide free accommodation",
    "we will try to accommodate",
    "we will provide assistance",
    "we will provide little bit of lodging",
    "we will provide little bit of assistance in giving our boarding house and bunk beds",
    "I've got bunk beds and a bungalow",
    "we should use the govt. run student hostels",
    "road side inns available for accommodation",
    "we have a place to rent",
    "have a restaurant to deliver food"
]

add_patterns(["accommodation"])

op = detect_patterns(messages)
print(op)
