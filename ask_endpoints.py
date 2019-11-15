""""""
import requests
import subprocess

ENDPOINT_COMMAND = "openstack endpoint list -f json | jq .[].URL -r"
TOKEN_COMMAND = "openstack token issue -f json | jq .id)"


def get_endpoint_list():
    """function to get all endpoints avaiable in openstack"""
    try:
        process = subprocess.Popen(ENDPOINT_COMMAND.split(),
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
    except OSError as os_error:
        print("Raise error {} {}".format(os_error, error))

    return output.split()


def get_openstack_id():
    try:
        process = subprocess.Popen(TOKEN_COMMAND.split(),
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
    except OSError as os_error:
        print("Raise error {} {}".format(os_error, error))

    return output


if __name__ == "__main__":
    endpoint_list = get_endpoint_list()
    print(endpoint_list)

    for endpoint in endpoint_list:
        if "project_id" in endpoint:
            endpoint = endpoint[:-1]+"/"
        response = requests.get(endpoint, headers={'X-Auth-Token: {}'.
                                                   format(get_openstack_id())})
        print(response.json())
