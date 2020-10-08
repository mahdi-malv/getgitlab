# Gitlab clone

Simple script to clone all gitlab projects

## Prerequisites

- Python3
- Pip

> `python` refers to Python and `pip` refers to Pip. Consider changing if you have `python3` or `pip3` or `python3 -m pip`

Download the dependencies:

```
pip install -r requirements.txt
```

## Usage

### Interactive way
All information will be asked from you

```bash
python getgitlab.py
```
### Arg way

```
python getgitlab.py -u USERNAME -t TOKEN [-p] [--http]

# example
python getgitlab.py -u my_user -t sfes34sfsdfser -p # print all my repo
```

|Option|Desc|
|--|--|
|`-u`, `--username` USERNAME |Gitlab user name|
|`-t`, `--access-token` TOKEN |Your account Personal access token|
|`--http` [Optional]|Use HTTPS repo links or `SSH` (For Https you need user pass each time)|
|`-p`,`--print`| No cloning. Just print them|