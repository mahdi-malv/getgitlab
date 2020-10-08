import requests
import argparse
from yaspin import yaspin
from PyInquirer import prompt
import subprocess


# author : Mahdi Malvandi
# version: 0.3.6
 
# region functions

def to_http_url(item):
    return item['http_url_to_repo']
def to_ssh_url(item):
    return item['ssh_url_to_repo']

def clone_repo(url):
    with yaspin(text=f"Cloning {url}", color="yellow") as spinner:
        time.sleep(2)  # time consuming code
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


username = ''
token = ''
should_use_ssh = True
should_clone = True

questions = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'What is your user Name?',
    },
    {
        'type': 'input',
        'name': 'token',
        'message': 'What is your Personal token?',
    },
    {
        'type': 'list',
        'name': 'ssh',
        'message': 'You want your HTTPS or SSH urls of repos?',
        'choices': ['SSH', 'Https'],
        'filter': lambda val: val == 'SSH'
    },
    {
        'type': 'list',
        'name': 'clone',
        'message': 'You want me to clone them after?',
        'choices': ['Print them only', 'Clone it'],
        'filter': lambda val: val == 'Clone it'
    },
]





parser = argparse.ArgumentParser(description='Clone Gitlab Repos of a user')
parser.add_argument('-u', '--username', help='User name', default='')
parser.add_argument('-t', '--access-token', help='Personal access token', default='')
parser.add_argument('--http', action='store_true',help='Use SSH to clone (Not passing for SSH)', default=False)
parser.add_argument('-p', '--print', action='store_true', help='Just print and no cloning', default=False)
args = parser.parse_args()

username = args.username
token = args.access_token
should_use_ssh = not args.http
should_clone = not args.print


if username == '' or token == '':
    answers = prompt(questions)
    print(answers)
    username = answers['username']
    token = answers['token']
    should_use_ssh = answers['ssh']
    should_clone = answers['clone']



if username == '' or token == '':
    print('Can not pass nothing for username neither token')
    exit()
else:
    clone_or_print = "Cloning" if should_clone else "Getting"
    print(f"{clone_or_print} repos of {username}")

url = f"https://gitlab.com/api/v4/users/{username}/projects"
payload = {}
headers = {
  'PRIVATE-TOKEN': token
}

print('Fetching repos...')
response = requests.request("GET", url, headers=headers, data = payload)
result = response.json()

repos = map(to_ssh_url, result) if should_use_ssh else map(to_http_url, result)
print(f'{len(result)} Repos found')
for i in repos:
    if (should_clone):
        clone_repo(i)
    else:
        print(f'Repo: {i}')