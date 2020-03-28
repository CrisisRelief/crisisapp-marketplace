
#Patterns to detect accommodation related queries


pattern_details1 = {
    "LABEL" : "ACCOMMODATE",
    "pattern" : [
        { "TEXT" : { "REGEX" : "accommodate" } }
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
        { "TEXT"  : { "REGEX" :  "accommod*|assistance|hous*|hotel|motel|stay|home|residen*|lodg*|host|inn|boarding|suite|bunk|renter|bungalow" } },
    ]
}

patterns = [
    pattern_details1, pattern_details2, pattern_details3
]

