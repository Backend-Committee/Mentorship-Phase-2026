import requests
import os
import json


class Analyzer:
    API_KEY = "7e7a7288c67a7b522f1e1b51c8ab56bf"
    LEAGUE_ID = 6
    SEASON = 2023

    def __init__(self, dir_path):
        self.dir_path = dir_path

        self.session = requests.Session()
        self.session.headers["x-apisports-key"] = self.API_KEY

    def get_best_player(self, round: str):
        players_ratings = []

        fixtures = self._get_round_fixtures(round)
        for fixture_dict in fixtures["response"]:
            fixture_id = fixture_dict["fixture"]["id"]
            players_ratings += self._get_players_from_fixture(fixture_id)
        
        best_player = None
        for player in players_ratings:
            if player['rating'] is None:
                continue
            
            if best_player is None:
                best_player = player
                continue
            
            # TODO: There may be many players with same rating
            if player['rating'] > best_player['rating']:
                best_player = player         
        
        with open(os.path.join(self.dir_path, "debug.json"), "w") as f:
            json.dump(best_player, f)
        
        return best_player
        

    def _get_round_fixtures(self, round):
        fixtures_json_path = os.path.join(self.dir_path, f"fixtures_{round}.json")

        if os.path.exists(fixtures_json_path):
            with open(fixtures_json_path, "r") as f:
                print(f"READING FROM CACHED {fixtures_json_path} file")
                input("PRESS ENTER TO CONTINUE")
                print()
                return json.load(f)

        fixtures_resp = self.session.get(
            "https://v3.football.api-sports.io/fixtures/",
            params={"league": self.LEAGUE_ID, "season": self.SEASON, "round": round},
        )
        fixtures = fixtures_resp.json()

        with open(fixtures_json_path, "w") as f:
            f.write(fixtures_resp.text)
        print(f"FETCHED INFO HAS BEEN SAVED TO {fixtures_json_path} file")
        input("PRESS ENTER TO CONTINUE")
        print()
        return fixtures

    def _get_players_from_fixture(self, fixture_id):
        result = []
        stats_json_path = os.path.join(self.dir_path, f"stats_{fixture_id}.json")

        if os.path.exists(stats_json_path):
            with open(stats_json_path, "r") as f:
                print(f"READING FROM CACHED {stats_json_path} file")
                input("PRESS ENTER TO CONTINUE")
                print()
                stats = json.load(f)
        else:
            stats_resp = self.session.get(
                f"https://v3.football.api-sports.io/fixtures/players",
                params={"fixture": fixture_id},
            )
            stats = stats_resp.json()

            with open(stats_json_path, "w") as f:
                f.write(stats_resp.text)
            print(f"FETCHED INFO HAS BEEN SAVED TO {stats_json_path} file")
            input("PRESS ENTER TO CONTINUE")
            print()

        for team_dict in stats["response"]:
            team_name = team_dict["team"]["name"]
            team_logo = team_dict["team"]["logo"]
            for player in team_dict["players"]:
                abstracted_player = {
                    "id": player["player"]["id"],
                    "name": player["player"]["name"],
                    "photo": player["player"]["photo"],
                    "rating": player["statistics"][0]["games"]["rating"],
                    "team_name": team_name,
                    "team_logo": team_logo
                }
                result.append(abstracted_player)

        return result

    def close(self):
        self.session.close()
