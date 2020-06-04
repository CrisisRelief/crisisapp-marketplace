
#Patterns to detect accommodation related queries


pattern_details0 = {
    "LABEL" : "PANDEMIC",
    "pattern" : [
        { "TEXT" : { "REGEX" : "isolation" } }
    ]
}


pattern_details1 = {
    "LABEL" : "ACCOMMODATE",
    "pattern" : [
        { "TEXT" : { "REGEX" : "accommodat*" } }
    ]
}

pattern_details2 = {
    "LABEL" : "ACC_LEMMAS",
    "pattern" : [
        {"LEMMA": {"IN": ["give", "provide", "offer"]}},
        { "OP" : "*" },
        { "TEXT"  : { "REGEX" :  "accommodation" } }
    ]
}

pattern_details3 = {
    "LABEL" : "ACC_REGEX",
    "pattern" : [
        { "TEXT"  : { "REGEX" :  "accommodation|\bassistance\b|\bhous*\b|\bhotel\b|\bmotel\b|\bstay\b|\bhome\b|\bresiden\b*|\blodg\b*|\bhost\b|\binn\b|\bboarding\b|\bsuite\b|\bbunk\b|\brenter\b|\bbungalow\b" } },
    ]
}

patterns = [
    #pattern_details1,pattern_details2, pattern_details3
    pattern_details0
]


