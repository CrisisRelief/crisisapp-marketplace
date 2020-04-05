import pgeocode
from typing import List, Dict

from src.common import req_offer_template as req_offer_cfg
from src.common.fricles_logger import *

class match_request(object):

    def __init__(self, country_type='AU'):
        try:
            '''
            Country Type defaults to Australia. Update the config file to modify
            '''
            self.geocode_dist = pgeocode.GeoDistance(country_type)
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
        score = 0
        return score

    def match_req_with_offer(self, req:req_offer_cfg, offer:req_offer_cfg) -> float:
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
        score = 0
        if req['crisis_name'] != offer['crisis_name']:
            return 0
        else:
            score += 1

        deg_overlap = len(set(req['req_offer_cat']).intersection(set(offer['req_offer_cat'])))
        if not deg_overlap:
            return 0
        
        score += deg_overlap

        nlp_score = self.get_nlp_match_score(req['req_offer_details'], offer['req_offer_details'])
        score *= 1 + nlp_score

        if 'derived_attrs' in req and not req['derived_attrs']['online_request']:
            try:
                dist = self.geocode_dist.query_postal_code(req['loc_post_code'], offer['loc_post_code'])
            except Exception as e:
                fricles_logger.warning('Failed to get distance between post codes: ' + str(e))
                dist = -1

        '''if distance is greater than threshold the score will be very low 
        '''
        if dist >= 0:
            norm_dist = dist/req_offer_cfg.DEFAULT_DISTANCE_THRESHOLD

            if norm_dist > 1:
                fricles_logger.info('Distance greater than threshold')
            else:
                score *= 1 + (1 - norm_dist)

        fricles_logger.info('Match score: ' + str(score))

        return score

    def match_reqs_with_offers(self, reqs:List, offers:List) -> List[Dict]:
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
                score = self.match_req_with_offer(req, offer)
                if score:
                    match = {}
                    match['score'] = score
                    match['request'] = req
                    match['offer'] = offer
                    matches.append(match)
                    

        return matches
        
