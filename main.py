import copy

def create_flow(service_spec, deployment_spec, flow_uuid, dev_branch_host, neon_project_id, neon_main_branch_id, neon_api_key):
    # assume dev branch already exists for now

	# deployment_spec = create_and_replace_branch(deployment_spec)

    new_deployment_spec = copy.deepcopy(deployment_spec)

    # change neondb proxy to point to dev branch

    new_deployment_spec['spec']['template']['spec']['containers'][0]['env']['PG_SERVER_NAME'] = dev_branch_host

    return new_deployment_spec, config_map
	
def delete_flow(config_map, flow_uuid):
    return
    # delete dev branch when its done
	# neon_api, neon_branch, neon_project_id = extract_neon_data(config_map, service_name)
	# neon.delete_branch(neon_api, neon_branch, neon_project_id)

def create_and_replace_branch(deployment_spec):
    return

def extract_neon_data(config_map, service_name):
    return