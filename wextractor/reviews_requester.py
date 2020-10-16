import json
import requests
from logger import get_logger

logger = get_logger('reviews_requester')

wextractor_auth_key = '<WEXTRACTOR_KEY>'
files_to_open = [
    {"file_to_open": 'exportjsonplace.json', "new_file": 'exportjsonplace_w_reviews.json'},
    {"file_to_open": 'exportjsonplaceB.json', "new_file": 'exportjsonplaceB_w_reviews.json'},
    {"file_to_open": 'exportjsonplaceC.json', "new_file": 'exportjsonplaceC_w_reviews.json'},
    {"file_to_open": 'exportjsonplaceD.json', "new_file": 'exportjsonplaceD_w_reviews.json'}
]

def fetch_reviews_from_extractor(reviews_for_place, place, max_number_of_reviews = 200):
    number_of_request = 0
    was_number_of_reviews_less_than_10 = False

    while (number_of_request < max_number_of_reviews and not was_number_of_reviews_less_than_10):
        wextractor_url = 'https://wextractor.com/api/v1/reviews?auth_token=' + wextractor_auth_key + '&offset=' + str(number_of_request) + '&id=' + place['place_id']
        place_reviews_fetched = requests.get(wextractor_url)
        if(place_reviews_fetched.ok):
            reviews_for_place.extend(place_reviews_fetched.json()["reviews"])
            value_log = {"place_id": place['place_id'], "reviews": place_reviews_fetched.json()["reviews"][:]}
            logger.info("Fetching first %s reviews for place_id '%s'", str(len(reviews_for_place)), place['place_id'])
            logger.debug("Reviews with offset = %s concatenated = %s", number_of_request, value_log)
            number_of_request += 1
            was_number_of_reviews_less_than_10 = len(place_reviews_fetched.json()["reviews"]) < 10
        else:
            logger.error('Fetching reviews for URL: %s FAILED! HTTP STATUS CODE (%s)', wextractor_url, place_reviews_fetched.status_code)


for file in files_to_open:
    with open(file["file_to_open"]) as exportjsonplace_json:
      places_list = json.load(exportjsonplace_json)

    for place in places_list:
        reviews_for_place = []
        places_with_reviews = []
        fetch_reviews_from_extractor(reviews_for_place, place)
        try:
            with open(file['new_file'], "r") as exportjsonplace_new_json:
                places_with_reviews = json.load(exportjsonplace_new_json)
                place['reviews'] = reviews_for_place
                places_with_reviews.append(place)

        except Exception:
            logger.warn('File %s does not have values', file['new_file'])

        with open(file['new_file'], 'w') as exportjsonplace_new_json:
            logger.info("Saving reviews for place_id '%s' into file '%s'", place['place_id'], file['new_file'])
            json.dump(places_with_reviews, exportjsonplace_new_json)
