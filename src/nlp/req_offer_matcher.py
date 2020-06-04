import pgeocode
from typing import List, Dict

from src.common import req_offer_template as req_offer_cfg
from src.common.fricles_logger import *
from src.nlp.doc_sim import document_similarity as doc_sim

class match_request(object):

    def __init__(self, country_type='AU'):
        try:
            '''
            Country Type defaults to Australia. Update the config file to modify
            '''
            self.geocode_dist = pgeocode.GeoDistance(country_type)
            self.ds = doc_sim()
            
        except Exception as e:
            fricles_logger.warning('Failed to load geocode info for ' + \
                                   str(country_type) + "with error code: " + str(e))
        return

    def get_nlp_match_score(self, req_details:str, offer_details:str) -> float:
        '''
        Get a match score based on the content in 'other details' in the requests/offers
        This can be used to up/down the overall match score for req/offers or can be used
        for requests/offers which are not categorised. 

        Args:
           req_details (str): free text in details provided by the user for requests
           offer_details (str): free text in details provided by the user for offers

        Returns:
            score (float): Match score
        '''
        
        threshold = req_offer_cfg.DEFAULT_SIM_MATCH_THRESHOLD
        if type(req_details) != str or type(offer_details) != str:
            return 0
        
        score = self.ds.get_sent2vec_similarity(req_details.lower(), offer_details.lower())

        return score

    def match_req_with_offer(self, req:req_offer_cfg, offer:req_offer_cfg, nlp_match_only:bool = False) -> float:
        '''
        Match a specific request with offer based on the fields present as part of request/offer datastructure
        This function takes in only one req and offer so that it can be a parallelized operation

        Match score = f(crisis_name, req_type, nlp_match, location_proximity)

        Args:
            req (req_offer_cfg): details of a single request
            offer (req_offer_cfg): details of a single offer
        
        Returns:
            score (float): match score between 0 and 1

        '''
        scores = {}
        score = 0

        nlp_match_score = self.get_nlp_match_score(req['req_offer_details'], offer['req_offer_details'])
        scores['nlp_match_score'] = nlp_match_score
        
        if nlp_match_only:
            return nlp_match_score
        
        score *= 1 + nlp_match_score
        
        if req['crisis_name'] != offer['crisis_name']:
            scores['crisis_match_score'] = 0
            return 0
        else:
            scores['crisis_match_score'] = 1
            score += 1
            
        deg_overlap = len(set(req['req_offer_cat']).intersection(set(offer['req_offer_cat'])))
        if not deg_overlap:
            scores['req_offer_category_match_score'] = 0
            return 0

        scores['req_offer_category_match_score'] = deg_overlap
        score += deg_overlap

        if 'derived_attrs' in req and not req['derived_attrs']['online_request']:
            try:
                dist = self.geocode_dist.query_postal_code(req['loc_post_code'], offer['loc_post_code'])
            except Exception as e:
                fricles_logger.warning('Failed to get distance between post codes: ' + str(e))
                dist = -1
                scores['distance_score'] = -1
        else:
            scores['distance_score'] = -1
                
        '''if distance is greater than threshold the score will be very low 
        '''
        if dist >= 0:
            norm_dist = dist/req_offer_cfg.DEFAULT_DISTANCE_THRESHOLD
            scores['distance_score'] = dist
            scores['normalised_distance_score'] = norm_dist
            
            if norm_dist > 1:
                fricles_logger.info('Distance greater than threshold')
            else:
                score *= 1 + (1 - norm_dist)

        else:
            scores['distance_score'] = -1
            scores['normalised_distance_score'] = -1
            
        fricles_logger.info('Match score: ' + str(score))

        scores['overall_score'] = score
        
        return scores

    def match_reqs_with_offers(self, reqs:List, offers:List, nlp_match_only:bool = False) -> List[Dict]:
        '''
        Match a list of requests and offers, best suited for distributed execution
        Args:
            reqs (List): list of requests
            offers (List): list of offeres

        Returns:
            matches (List): list of matches with details of request, offer and  match score
        '''
        matches = []
        for req in reqs:
            for offer in offers:
                scores = self.match_req_with_offer(req, offer, nlp_match_only)
                if type(scores) != dict:
                    continue
                match = {}
                match['overall_score'] = scores['overall_score']
                match['request_serial_number'] = req['serial_number']
                match['offer_serial_number'] = offer['serial_number']
                match['request_category'] = req['req_offer_cat']
                match['offer_category'] = offer['req_offer_cat']
                match['request_description'] = req['req_offer_details']
                match['offer_description'] = offer['req_offer_details']
                match['request_email'] = req['email']
                match['offer_email'] = offer['email']
                match['request_phone_number'] = req['phone_number']
                match['offer_phone_number'] = offer['phone_number']
                match['request_suburb'] = req['loc_suburb']
                match['offer_suburb'] = offer['loc_suburb']
                match['request_post_code'] = req['loc_post_code']
                match['offer_post_code'] = offer['loc_post_code']
                match['request_state'] = req['loc_state']
                match['offer_state'] = offer['loc_state']
                
                match['nlp_match_score'] = scores['nlp_match_score']
                match['distance_score'] = scores['distance_score']
                match['normalised_distance_score'] = scores['normalised_distance_score']
                match['req_offer_category_match_score'] = scores['req_offer_category_match_score']
                match['crisis_match_score'] = scores['crisis_match_score']
                matches.append(match)
                    

        return matches
        
