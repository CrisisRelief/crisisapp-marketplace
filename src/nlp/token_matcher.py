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
    Callback function to collect spans of interest from sentences in a block of text.

    Args:
        matcher (spacy.Matcher): matcher object set to nlp.vocab
        doc (spacy.tokens.Doc): spacy Doc object
        i (int): index for the match
        matches (List): list of matches
                        
    Returns:
        None
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
    '''
    Add predefined patterns to the pattern library

    Args:
        pattern_types (List): list of the patterns of interest

    Returns:
        None
    '''
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
    Detects patterns of interest from a list of blocks of text
    Args:
        content (List): list of text blocks from which patterns need to be detected
    Returns:
        op (List): list of matched patterns with spans and related info
    """
    global matched_sents
    for txt in content:
        doc = nlp(txt)
        matches = matcher(doc)

    op = matched_sents
    matched_sents = []
    return op


add_patterns(["pickups", "accommodation"])

