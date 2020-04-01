
#Patterns to detect accommodation related queries


pattern_details1 = {
    "LABEL" : "PICKUP_REG",
    "pattern" : [
        { "TEXT" : { "REGEX" : "\bpickup\b|\bpick-up\b|\bdeliver*\b|\bgrab*\b" } }
    ]
}

pattern_details2 = {
    "LABEL" : "PICKUP_LEMM",
    "pattern" : [
        { "TEXT"  : { "REGEX" :  "deliver|pickup|pick-up|grab|drop" } },
        { "OP" : "*" },
        { "TEXT" : { "REGEX" : "\bgrocer*\b|\bmedicin*\b|\bmedicat*\b|\bclinic*\b|\bparamedic*\b|\bhealth*\b" }}
          ]
}
          
patterns = [
    pattern_details2, pattern_details1
]

