import requests
r = requests.get('http://localhost:8000/api/v1/readings/?station=15')
data = r.json()
print(f"Response type: {type(data)}")
if isinstance(data, dict):
    print(f"Keys: {list(data.keys())}")
    if 'results' in data:
        print(f"Results count on first page: {len(data['results'])}")
        print(f"Total count: {data.get('count')}")
else:
    print(f"List length: {len(data)}")
