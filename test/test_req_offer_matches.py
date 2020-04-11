import pandas as pd
import copy
import src.common.req_offer_template as req_offer_cfg


f = "test/request_offer_help.csv"

def read_test_file(f):

    reqs = []
    offers = []
    
    df = pd.read_csv(f)
    print(df.shape)

    for index, row in df.iterrows():

        sub_type_req = False
        if row['Crisis name'] != "COVID-19 pandemic":
            continue
        sub = copy.deepcopy(req_offer_cfg.req_offer)
        sub_type_request = False
        sub['submission_date'] = row['Completed']
        sub['crisis_name'] = row['Crisis name']
        if 'offer' in row['Requesting or offering help']:
            sub['submission_type'] = "offering_help"
            sub_type_request = False
        else:
            sub['submission_type'] = "requesting_help"
            sub_type_request = True
            
        sub['full_name'] = row['Full name']
        cats = row['Request/offer category']
        list_of_cats = cats.split(";")
        
        #if len(list_of_cats) == 1 and 'Other - please detail' in row['Request/offer category']:
        #    continue

        if not 'Other - please detail' in row['Request/offer category']:
            continue
        
        sub['serial_number'] = row['Serial number']
        sub['req_offer_cat'] = list_of_cats
        sub['req_offer_details'] = row['Detailed description']
        sub['email'] = row['Your email']
        sub['phone_number'] = row['Your phone number']
        sub['loc_st_addr'] = row['Your location: Address']
        sub['loc_suburb'] = row['Your location: City/Town']
        
        '''Entry does not have valid state
        '''
        #if row['Your location: State'] == 'Select State':
        #    continue
        sub['loc_state'] = row['Your location: State']
        sub['loc_post_code'] = row['Your location: Postcode']

        if sub_type_request:
            reqs.append(sub)
        else:
            offers.append(sub)
            
    return reqs, offers

r, o = read_test_file(f)

from src.nlp.req_offer_matcher import match_request

mr = match_request()
matches = mr.match_reqs_with_offers(r, o, nlp_match_only=False)

op = pd.DataFrame(matches)
op.to_cs("match_outputs.csv", index = False)



