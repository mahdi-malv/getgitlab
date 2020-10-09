#!/usr/bin/python3

import requests
import argparse
from yaspin import yaspin
import subprocess


# author : Mahdi Malvandi
# version: 1.0.1
 
# region functions

def to_http_url(item):
    return item['http_url_to_repo']
def to_ssh_url(item):
    return item['ssh_url_to_repo']

def clone_repo(url):
    with yaspin(text=f"Cloning {url}", color="yellow") as spinner:
        try:
            command = f'git clone {url}'
            p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, close_fds=True)
            out,err = p.communicate()
            if err:
                spinner.fail("💥 ")
            else:
                spinner.ok("✅ ")
        except:
            spinner.fail("💥 ")


# endregion



parser = argparse.ArgumentParser(description='Clone Gitlab Repos of a user')
parser.add_argument('-u', '--username', help='User name', default='')
parser.add_argument('-g', '--group', help='Group name', default='')
parser.add_argument('-t', '--access-token', help='Personal access token', default='')
parser.add_argument('--http', action='store_true',help='Use SSH to clone (Not passing for SSH)', default=False)
parser.add_argument('-p', '--print', action='store_true', help='Just print and no cloning', default=False)
args = parser.parse_args()

username = args.username
group = args.group
token = args.access_token
should_use_ssh = not args.http
should_clone = not args.print


if (group == '' and username == '') or token == '':
    print('Make sure you pass username/goup and also the token')
    exit()
elif group != '' and username != '':
    print('Either username or group must be entered. Can not clone both for now.')
    exit()
else:
    clone_or_print = "Cloning" if should_clone else "Getting"
    print(f"{clone_or_print} repos of {username}")

userUrl = f"https://gitlab.com/api/v4/users/{username}/projects"
groupUrl = f"https://gitlab.com/api/v4/groups/{group}/projects"

is_group = username == '' and group != ''

url = groupUrl if is_group else userUrl


payload = {}
headers = {
  'PRIVATE-TOKEN': token
}

message = f'Group: {group}' if is_group else f'User: {username}'
print(f'Fetching repos of {message}')
response = requests.request("GET", url, headers=headers, data = payload)
result = response.json()

repos = map(to_ssh_url, result) if should_use_ssh else map(to_http_url, result)
print(f'{len(result)} Repos found')
for i in repos:
    if (should_clone):
        clone_repo(i)
    else:
        print(i)