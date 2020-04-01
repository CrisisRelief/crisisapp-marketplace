import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher
from spacy.tokens import Span

nlp = English()
ruler = EntityRuler(nlp, validate=True)


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


p4 = [
    {"LEMMA": {"IN": ["give", "provide", "offer"]}},
]
p2 = [
    {"LEMMA": {"IN": ["give", "provide", "offer"]}},
    { "OP" : "*" },
    { "TEXT" : { "REGEX" : "accommo*|assistance*" } }
]

p3 = [     { "TEXT" : { "REGEX" : "accommo*|assistance*" } } ]

patterns =  [
    #{ "label" : "ACC" , "pattern" : p4 },
    #{ "label" : "ACC" , "pattern" : p3},
    { "label" : "ACC" , "pattern" : p2}
]

ruler.add_patterns(patterns)
nlp.add_pipe(ruler)

doc = nlp(messages[0])
print([(ent.text, ent.label_) for ent in doc.ents])

doc = nlp(messages[1])
print([(ent.text, ent.label_) for ent in doc.ents])
