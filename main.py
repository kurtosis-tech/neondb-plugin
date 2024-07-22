import copy

def create_flow(service_spec, deployment_spec, flow_uuid, dev_branch_host, NEON_PROJECT_ID, NEON_MAIN_BRANCH_ID, NEON_API_KEY):
    # assume dev branch already exists for now
    new_deployment_spec = copy.deepcopy(deployment_spec)

    # change neondb proxy to point to dev branch

    print(new_deployment_spec)
    new_deployment_spec['spec']['template']['spec']['containers'][0]['env']['PG_SERVER_NAME'] = dev_branch_host
    new_deployment_spec['spec']['template']['spec']['containers'][0]['env']['PG_SERVER_NAME'] = dev_branch_host
    new_deployment_spec['spec']['template']['spec']['containers'][0]['env']['PG_SERVER_NAME'] = dev_branch_host
    new_deployment_spec['spec']['template']['spec']['containers'][0]['env']['PG_SERVER_NAME'] = dev_branch_host

    return {
        "deployment_spec": new_deployment_spec, 
        "config_map": config_map,
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