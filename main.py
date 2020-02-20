import requests
import json
import pickle
import time
from config import BaseConfig
from analysis import Analysis


def construct_request_url(account_ids):
    """
    :param account_ids: players' account ID
    :return: construct URL string for the `game_mode` competitions including
             `account_id` and `included_account_id`
    """
    base_url = 'https://api.opendota.com/api'
    construct_url = base_url + '/players/%s/matches' % str(account_ids[0])
    construct_url += '?'
    for other_id in account_ids[1:]:
        if construct_url[-1] != '?':
            construct_url += '&'
        construct_url += 'included_account_id=%s' % str(other_id)
    #construct_url += '&excluded_account_id=339404043&excluded_account_id=136216469'
    return construct_url


def get_match_ids(url):
    """
    :param url: request url
    :return: list of match ids (RD and Match only)
    """
    r = requests.get(url)
    r_str = r.content.decode()
    r_json = json.loads(r_str)
    res = []
    for item in r_json:
        if item["game_mode"] in [3, 22]:
            res.append(item["match_id"])
    return res


def get_matches_detail(match_ids):
    """
    :param match_ids: list of match ids
    :return: matches detail json list
    """
    res = []
    for match_id in match_ids:
        url = 'https://api.opendota.com/api/matches/%s' % str(match_id)
        r = requests.get(url)
        r_str = r.content.decode()
        r_json = json.loads(r_str)
        res.append(r_json)
        print("players" in r_json)
        time.sleep(1)
    pickle.dump(res, open("match_details_3p.pkl", "wb"))
    return res


if __name__ == '__main__':
    config = BaseConfig()
    analysis = Analysis()
    # request_url = construct_request_url(config.account_ids)
    # print(request_url)
    # match_ids = get_match_ids(request_url)
    # print(len(match_ids))
    # match_detail = get_matches_detail(match_ids)
    match_detail = pickle.load(open("match_details_5p.pkl", "rb"))
    total_odds = analysis.total_odds(config.account_ids[0],
                                     match_detail,
                                     verbose=True)
    stat = analysis.hero_odds(config.account_ids, match_detail, verbose=True)



