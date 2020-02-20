class Analysis:
    def __init__(self):
        from datas.hero_id import hero_id
        self.hero_id_to_name = hero_id

    def total_odds(self, account_id, match_details, verbose=True):
        """
        Analysis total win rate.

        :param account_id:
        :param match_details:
        :param verbose:
        :return: dict
        """
        length = len(match_details)
        win = 0
        for matches in match_details:
            for player in matches["players"]:
                if player["account_id"] == account_id:
                    if player["win"]:
                        win += 1
        ret = {"total": length, "win": win, "lose": length - win, "win_rate": win / length}
        if verbose:
            print(ret)
        return ret

    def hero_odds(self, account_ids, match_details, need_sort=True, verbose=True):
        """
        Analysis the odds for heroes in matches.

        :param account_ids: list of account ID
        :param match_details: list of json
        :param need_sort: sort the statistics in the order of (odds, win_number)
        :param verbose: print the stat results
        :return: dict {username: {hero: {win: 0, lose: 0}, ...}, ...}
        """
        stat = {}
        for account_id in account_ids:
            for matches in match_details:
                for player in matches["players"]:
                    if player["account_id"] == account_id:
                        username = player["personaname"]
                        if username not in stat:
                            stat[username] = {}
                        hero_name = self.hero_id_to_name[player["hero_id"]]
                        if hero_name not in stat[username]:
                            stat[username][hero_name] = {"win": 0, "lose": 0}
                        if player["win"]:
                            stat[username][hero_name]["win"] += 1
                        else:
                            stat[username][hero_name]["lose"] += 1
        if need_sort:
            for username, datas in stat.items():
                datas = sorted(
                    datas.items(),
                    key=lambda d:(d[1]["win"] / (d[1]["win"] + d[1]["lose"]), d[1]["win"]),
                    reverse=True)
                # unified format
                datas = {k: v for (k, v) in datas}
                stat[username] = datas
        if verbose:
            for username, datas in stat.items():
                print("username", username)
                for hero, info in datas.items():
                    print("\t", hero, info)
                print("------------------------------------------")

        return stat


