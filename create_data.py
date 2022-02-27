import requests
from requests.structures import CaseInsensitiveDict
import json
import time
from tqdm import tqdm
import os


bearer_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImVkZmY4YTAyLWIyZGEtNDhkZC1iOGVjLThhMmM1MGE2YTM0MnNpZyJ9.eyJ0cnVzdCI6MTAwLCJpYXQiOjE2NDU4NzcyNDcsImV4cCI6MTY0NTg4MDg0NywiaXNzIjoib2F1dGgyYWNjIiwianRpIjoiZTNiZDI3ZmItMWU4NS00M2QwLWEyYTMtOWJjMzk3YTRmNWZiIiwibGF0IjoxNjQ1ODMxNTExLCJhdWQiOiJjb20ubmlrZS5kaWdpdGFsIiwic3ViIjoiY29tLm5pa2UuY29tbWVyY2UubmlrZWRvdGNvbS53ZWIiLCJzYnQiOiJuaWtlOmFwcCIsInNjcCI6WyJuaWtlLmRpZ2l0YWwiXSwicHJuIjoiNjEyNjUwNDEwNCIsInBydCI6Im5pa2U6cGx1cyJ9.jtSk-57-sOaDKXGhSL2uS9w2yxcPALdaUpK6buli8aa0V1Yrw_NtyiUr05G-N3ms8BZgx3LDp360EGDhBaan-GUGNkn2M7qBhmggMak3TsecZZi6oBOeotl9MR4S6D5FT0iTy_zyal-wY5Wosq_t14rjHf7QiPsNDilqdVFvi_xyZvSFrAvaluNQgDWFIkZGWlevVaq1XgOmorq-kwC1_kcHvPZTdjrvwO71KyouLDnkquQdMxzaZJ7q-TH9pPl6xnGciRA0qSJ1I0pK4Mx5oBbBlziWitDo5eVAbEy_P4obDOkvdP5lhiABDFR--nIWNBRSuXC3Sl5068vV086L1A"
headers = {'content-type': 'application/json', "Authorization": f"Bearer {bearer_token}"}


def get_runs(headers, path = "summaries.json"):
    activities = []
    current_time = 0
    current_activities = True
    while current_activities:
        url = f"https://api.nike.com/sport/v3/me/activities/after_time/{current_time}"
        r = requests.get(url, headers=headers)
        current_activities = json.loads(r.content)["activities"]
        runs = list(filter(lambda act: act["type"]=="run", current_activities))
        if not current_activities:
            json.dump(activities, open(path, "w"), indent=4)
            return activities
        activities += runs
        final_time = current_activities[-1]["start_epoch_ms"]
        current_time = final_time + 100000

def get_run_details(run_id, headers, path = "run_details"):
    filename = os.path.join(path, f"{run_id}.json")
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(filename):
        print(f"{run_id} already exists")
        return None
    url = f"https://api.nike.com/sport/v3/me/activity/{run_id}?metrics=ALL"
    r = requests.get(url, headers=headers)
    details = json.loads(r.content)
    json.dump(details, open(filename, "w"), indent=4)
    return details


def get_all_details(bearer_token = None):
    if not bearer_token:
        bearer_token = pc.paste()
    headers = {'content-type': 'application/json', "Authorization": f"Bearer {bearer_token}"}
    runs = get_runs(headers)
    nruns = len(runs)
    run_dict = dict()
    print(f"Downloading details of {nruns} runs.")
    for run in tqdm(runs):
        run_dict[run["id"]] = get_run_details(run['id'], headers)
    return runs, run_dict

if __name__ == "__main__":
    get_all_details(bearer_token)

