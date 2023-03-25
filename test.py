import requests

def test_get_summaries():
    url = "http://localhost:5000/app/summarize"
    topic = "mongodb"
    response = requests.post(url, json={"topic": topic})

    if response.status_code == 200:
        summaries = response.json()
        print(f"Summary: {summaries}")
    else:
        print(f"Failed to fetch summaries with status cdde {response.status_code}")

if __name__ == "__main__":
    test_get_summaries()

