import requests

BASE_URL = "https://api.ebird.org/v2"
API_KEY = "rc0e5cf9s6ld"  # please input your own API key!
# user_id = "MTQyNTMzNA"


headers = {
    "X-eBirdApiToken": API_KEY
}

def get_recent_observations(region_code):
    endpoint = f"{BASE_URL}/data/obs/{region_code}/recent"
    response = requests.get(endpoint, headers=headers)
    # return response.json()
    data = response.json()
    bird_names = [entry['comName'] for entry in data][:5]
    return(bird_names)

# testing the code
observations = get_recent_observations("US-IL-031")
#Print out the first 10 observations as an example:
# for obs in observations[:10]:
#     print(f"{obs['speciesCode']}: {obs['comName']} seen at {obs['obsDt']} in location {obs['locName']}.")


# print(observations)