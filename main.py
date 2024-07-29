import copy
import requests
import json

def create_flow(service_spec, deployment_spec, flow_uuid, NEON_PROJECT_ID, NEON_MAIN_BRANCH_ID, NEON_API_KEY):
    # assume script exists for now
    modified_deployment_spec = copy.deepcopy(deployment_spec)

    container = modified_deployment_spec['template']['spec']['containers'][0]

    dev_branch_host, error = create_neon_branch(NEON_API_KEY, NEON_PROJECT_ID, NEON_MAIN_BRANCH_ID)
    if error:
        # how are errors handled in plugins?
        print(f"Error: {error}")

    container['env'] = [
        {'name': 'PG_SERVER_HOSTNAME', 'value': dev_branch_host},
    ]

    modified_deployment_spec['template']['spec']['containers'] = [container]

    return {
        "deployment_spec": modified_deployment_spec,
        "config_map": {}
    }
	
def delete_flow(config_map, flow_uuid):
    # delete dev branch when its done
	# neon_api, neon_branch, neon_project_id = extract_neon_data(config_map, service_name)
	# neon.delete_branch(neon_api, neon_branch, neon_project_id)
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

    return host, None

def delete_neon_branch(config_map, service_name):
    return

def extract_neon_data():
    return