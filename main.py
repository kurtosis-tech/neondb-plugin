import copy

def create_flow(service_spec, deployment_spec, flow_uuid, dev_branch_host, NEON_PROJECT_ID, NEON_MAIN_BRANCH_ID, NEON_API_KEY):
    # assume script exists for now
    modified_deployment_spec = copy.deepcopy(deployment_spec)

    container = modified_deployment_spec['template']['spec']['containers'][0]

    container['env'] = [
        {'name': 'PG_SERVER_HOSTNAME', 'value': dev_branch_host},
        # {'name': 'NEON_API_KEY', 'value': db_user},
        # {'name': 'NEON_MAIN_BRANCH_ID', 'value': db_password},
        # {'name': 'NEON_PROJECT_ID', 'value': db_password},
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

def create_and_replace_branch(deployment_spec):
    return

def extract_neon_data(config_map, service_name):
    return