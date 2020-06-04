
'''Includes attributes that come in directly from the webform requests. We ignore
atributes such as ip-address etc. which don't matter for matching
Derived attributes is a set of attributes which we may have to infer based on the request
and will be used in matching requests and offers
'''
req_offer = {
    "submission_date" : "",
    "submitted_by" : "",
    "crisis_name" : "",
    "submission_type" : "",
    "full_name" : "",
    "req_offer_cat" : [],
    "req_offer_cat_other" : 1,
    "req_offer_details" : "",
    "email" :"",
    "phone_number" : "",
    "loc_st_addr" : "",
    "loc_suburb" : "",
    "loc_state" : "",
    "loc_post_code" : "",

    "derived_attrs": {
        "online_request": False,
        "lat_long" : "",
        "time_sensitive": 1
        }
}

    
DEFAULT_COUNTRY_CODE = "AU"
DEFAULT_DISTANCE_THRESHOLD = 100
DEFAULT_DISTANCE_METRIC = "KM"

DEFAULT_SIM_MATCH_THRESHOLD = 0.5
