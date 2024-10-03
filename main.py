from urllib.parse import urlparse, urlunparse
import copy
import requests
import json

def create_flow(service_spec, pod_spec, flow_uuid, NEON_PROJECT_ID, NEON_FORK_FROM_BRANCH_ID, NEON_API_KEY):
    modified_pod_spec = copy.deepcopy(pod_spec)

    container = modified_pod_spec['containers'][0]

    postgres_url = ""
    for env in container['env']:
        if env.get("name") == "POSTGRES":
            postgres_url = env.get("value")

    dev_branch_hostname, dev_branch_id, error = create_neon_branch(NEON_API_KEY, NEON_PROJECT_ID, NEON_FORK_FROM_BRANCH_ID)
    if error:
        print(f"Error: {error}")

    new_postgres_url = update_postgres_url(postgres_url, dev_branch_hostname)
    container['env'] = [
        {'name': 'POSTGRES', 'value': new_postgres_url},
    ]

    modified_pod_spec['containers'] = [container]

    return {
        "pod_spec": modified_pod_spec,
        "config_map": {
            "NEON_API_KEY": NEON_API_KEY,
            "NEON_PROJECT_ID": NEON_PROJECT_ID,
            "NEON_BRANCH_ID": dev_branch_id,
        }
    }
	
def delete_flow(config_map, flow_uuid):
    resopnse = delete_neon_branch(config_map["NEON_API_KEY"], config_map["NEON_PROJECT_ID"], config_map["NEON_BRANCH_ID"])
    print(resopnse)
    return

def create_neon_branch(neon_api_key, project_id, parent_branch_id):
    url = f"https://console.neon.tech/api/v2/projects/{project_id}/branches"

    json_payload = {
        "endpoints": [{"type": "read_write"}],
        "branch": {"parent_id": parent_branch_id}
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {neon_api_key}"
    }

    try:
        response = requests.post(url, json=json_payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return "", f"Error sending request: {e}"

    if response.status_code != 201:
        return "", f"Unexpected status code: {response.status_code}, body: {response.text}"

    try:
        result = response.json()
    except json.JSONDecodeError as e:
        return "", f"Error decoding response: {e}"

    endpoints = result.get("endpoints", [])
    if not endpoints:
        return "", "Endpoints not found in response"

    first_endpoint = endpoints[0]
    host = first_endpoint.get("host")
    if not host:
        return "", "Host not found in response"

    branch_id = result.get("branch", {}).get("id")
    if not branch_id:
        return "", "", "Branch ID not found in response"

    return host, branch_id, None

def delete_neon_branch(neon_api_key, project_id, branch_id):
    url = f"https://console.neon.tech/api/v2/projects/{project_id}/branches/{branch_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {neon_api_key}"
    }

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error sending request: {e}"

    if response.status_code != 204:
        return f"Unexpected status code: {response.status_code}, body: {response.text}"

    return "Branch deleted successfully"

def update_postgres_url(postgres_url, new_hostname):
    parsed_url = urlparse(postgres_url)

    if parsed_url.username and parsed_url.password:
        userinfo = f"{parsed_url.username}:{parsed_url.password}@"
    elif parsed_url.username:
        userinfo = f"{parsed_url.username}@"
    else:
        userinfo = ""

    new_netloc = f"{userinfo}{new_hostname}:{parsed_url.port}" if parsed_url.port else f"{userinfo}{new_hostname}"
    updated_url = urlunparse(parsed_url._replace(netloc=new_netloc))

    return updated_url

