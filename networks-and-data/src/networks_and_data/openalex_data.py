import requests
import json
import networkx as nx

#1 To fetch upto 75000 results 

def fetch_results_mini(url, p1, p2, mailto):
    all_data = []  # List to store all the data from all pages

    for p in range(p1,p2):
      params = {
        'per_page': 25, # Number of results per page (max is 200)
        'page' : p,
        "mailto" : mailto
      }
      response = requests.get(url,params=params)
      data = response.json()


      if not isinstance(data, dict):
          print(f"Unexpected response type on page {p}: {type(data)}")
          break

        # Check for the 'results' key in the response
      if 'results' not in data:
          print(f"'results' key not found on page {p}. Response: {data}")
          break


      # Add the results from this page to the total list
      all_data.extend(data['results'])


    return all_data

def fetch_results_in_range(base_url, start, end, mailto):
    all_data = []
    cursor = '*'  # Start from the beginning
    # base_url = "https://api.openalex.org/works"  # Replace with the correct endpoint
    total_fetched = 0
    per_page = 200  # Max records per page

    # First, skip the first `start` records (100,000 records)
    while total_fetched < start:
        params = {
            'per_page': per_page,
            'cursor': cursor,
            "mailto": mailto  # Add your email to comply with OpenAlex API requirements
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        # Check for errors
        if 'error' in data:
            print(f"API Error: {data['error']}")
            break

        # Check if 'results' key exists and increment total_fetched
        if 'results' in data:
            total_fetched += len(data['results'])
        else:
            print(f"'results' key missing. Response: {data}")
            break

        # Check for the next cursor to continue fetching
        if 'meta' in data and 'next_cursor' in data['meta']:
            cursor = data['meta']['next_cursor']
            print(f"Skipped {total_fetched} records. Continuing with cursor: {cursor}")
        else:
            print("No more data available.")
            break

    # Now fetch records between 100,001 and 200,000
    while total_fetched < end:
        # Adjust per_page to not exceed the end limit
        remaining = end - total_fetched
        if remaining < per_page:
            per_page = remaining

        params = {
            'per_page': per_page,
            'cursor': cursor,
            "mailto": mailto  # Add your email to comply with OpenAlex API requirements
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        # Check for errors
        if 'error' in data:
            print(f"API Error: {data['error']}")
            break

        # Add the fetched results to the list
        if 'results' in data:
            all_data.extend(data['results'])
            total_fetched += len(data['results'])  # Update the total count
            print(f"Fetched {total_fetched} records.")
        else:
            print(f"'results' key missing. Response: {data}")
            break

        # Check for the next cursor to continue fetching
        if 'meta' in data and 'next_cursor' in data['meta']:
            cursor = data['meta']['next_cursor']
        else:
            print("No more data available.")
            break

    return all_data

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)  # 'indent=4' makes it readable with proper formatting
    print(f"Data successfully saved to {filename}")

def institution_collaborations(all_data):
  collaborations = {}
  for work in all_data:
    institutes = set()
    for auth in work['authorships']:
      for inst in auth['institutions']:
        institutes.add(inst['display_name'])
    # print(institutes)

    institutions = list(institutes)
    if len(institutions) > 1:
      for i in range(len(institutions)):
        for j in range(i + 1, len(institutions)):
          inst1 = institutions[i]
          inst2 = institutions[j]
          if (inst1, inst2) in collaborations:
            collaborations[(inst1, inst2)] += 1
          elif (inst2, inst1) in collaborations:
            collaborations[(inst2, inst1)] += 1
          else:
            collaborations[(inst1, inst2)] = 1

          # print(collaborations)

  return collaborations


def convert_to_networkx_format(collaborations):
    edge_list = []
    for (university1, university2), weight in collaborations.items():
        edge_list.append((university1, university2, weight))  # Each entry is (university1, university2, weight)
    return edge_list

def build_university_network(collaborations):
    edge_list = convert_to_networkx_format(collaborations)
    G = nx.Graph()  # Create an undirected graph
    G.add_weighted_edges_from(edge_list)  # Add weighted edges from the edge list
    return G


def load_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    print(f"Data successfully loaded from {filename}")
    return data

