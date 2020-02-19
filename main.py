import requests
import json
from config import BaseConfig


def construct_request_url(account_id, included_account_id):
    """
    :param account_id: player's account ID
    :param included_account_id: account IDs in the match (array)
    :param game_mode: game mode ID (default 22 is match mode)
    :return: construct URL string for the `game_mode` competitions including
             `account_id` and `included_account_id`
    """
    base_url = 'https://api.opendota.com/api'
    construct_url = base_url + '/players/%s/matches' % str(account_id)
    construct_url += '?'
    for included_id in included_account_id:
        if construct_url[-1] != '?':
            construct_url += '&'
        construct_url += 'included_account_id=%s' % str(included_id)
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


if __name__ == '__main__':
    config = BaseConfig()
    request_url = construct_request_url(config.account_id,
                                        config.included_account_id)
    print(request_url)
    match_ids = get_match_ids(request_url)
    print(len(match_ids))
