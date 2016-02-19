__author__ = 'rshinners'

import urllib2
import json
import requests

environments = [
    {'octopus_id': 'Environments-1', 'led_index': 0},
    {'octopus_id': 'Environments-2', 'led_index': 1},
    {'octopus_id': 'Environments-3', 'led_index': 2},
    {'octopus_id': 'Environments-4', 'led_index': 3}
]
ledstrip_base_url = 'http://localhost:9090'


def get_json(url):
    base_url = 'https://vbuoctopus.vistaprint.net/api'
    api_key = 'API-HJKN1JBVQPXI5NXLXUBGH8XA0'
    req = urllib2.Request(base_url + url)
    req.add_header('X-Octopus-ApiKey', api_key)
    return json.load(urllib2.urlopen(req))


def get_latest_deploy_status(environment):
    """
    Get the status of the last run server task in an environment.
    :param environment: octopus environment id.  Should look like 'Environments-1234'
    :return: returns string of the state of the server task.
        will be one of the following (from http://help.octopusdeploy.com/discussions/questions/5122-api-item-state):
        * "None"        - Task does not exist
        * "Success"     - Task was a success
        * "Warning"     - Task completed with at least one warning
        * "Failure"     - Task failed
        * "InProgress"  - Task is currently in progress
    """

    tasks_data = get_json('/tasks?environment=' + environment)
    if len(tasks_data['Items']) < 1:
        # "None"
        return (0,0,0)
    task = tasks_data['Items'][0]

    if not task['IsCompleted']:
        # "InProgress"
        return (64,0,64)
    if not task['FinishedSuccessfully']:
        # "Failure"
        return (255,0,0)
    if task['HasWarningsOrErrors']:
        # "Warning"
        return (128,128,0)
    # "Success"
    return (0,64,0)


def send_color(index, color):
    r,g,b = color
    request_obj = {'color': {'r': r, 'g': g, 'b': b}}
    response = requests.put(ledstrip_base_url + "/pixel/" + str(index), data=json.dumps(request_obj))
    print response


def main():
    for env in environments:
        color = get_latest_deploy_status(env['octopus_id'])
        send_color(env['led_index'], color)

main()