# hashie v1.3.0

hashie is a Python tool to query a Hashtopolis instance for various information, create new hashlists and tasks, and export cracked hashes.

Hashtopolis.py is a custom API built just for hashie purposes. It's functionality is pretty limited to only what I need for hashie.py, but I may add to it if the use case comes up.

## Setup

Git clone this repo, cd into the repo directory, and grab required Python packages using ```python3 -m pip install -r requirements.txt```.

You can put the Hashtopolis hostname, port, and API key in ```/root/.hashie/config.json``` if you don't want to provide it via commandline in the following format:

```json
{
    "hashtopolis":"hashtopolisurl.com",
    "port":hashtopolisport,
    "apiKey":"hashtopolisapikey"
}
```

## Usage
```
Usage: hashie.py ACTION [OPTIONS]

  hashie v1.3.0

  Available ACTIONs:

  list-tasks            List highest priority tasks
  list-hashlists        List recently added hashlists
  list-superhashlists   List recently added superhashlists
  create-task           Create a new task
  find-hashlist         Find matching hashlists from name
  export-hashes         Export cracked hashes for given hashlist ID
  export-superhashes    Export cracked hashes for given superhashlist ID
  
Options:
  -h, --hashtopolis        Hostname Of Hashtopolis Instance
  -p, --port               Port For Hashtopolis  [default: 443]
  -a, --api-key            API Key For Hashtopolis
  -i, --hashlist-id        Hashlist ID
  -s, --superhashlist-id   Superhashlist ID
  -n, --hashlist-name      Hashlist Name
  -t, --hashtype           Hashlist type (ntlm, ntlmv2, kerbtgt23)
  -f, --hash-file          File containing your hashes
  --num-tasks              Number of tasks to get [default: 15]
  --num-hashlists          Number Of Hashlists To Get  [default: 15]
  --priority               Set your new task to have the highest priority
  --help                   Show this message and exit.
```
### List recently added hashlists
```python
python3 hashie.py list-hashlists -h myhashtopolis.com -a [api_key]
```
### List 30 most recently added superhashlists
```python
python3 hashie.py list-superhashlists --num-hashlists 30
```
### Find matching hashlists with a name containing 'myHashlist'
```python
python3 hashie.py find-hashlist -n myHashlist
```
### Create hashlist named 'newHashlist' with ntlmhashes.txt containing NTLM hashes and start a supertask for it
```python
python3 hashie.py create-task -n newHashlist -t ntlm -f ntlmhashes.txt
```
### Same as one above but automatically set your new supertask at the highest priority
```python
python3 hashie.py create-task -n newHashlist -t ntlm -f ntlmhashes.txt
```
### Export cracked hashes given a hashlist ID
```python
python3 hashie.py export-hashes -i [hashlist-id]
```
### Export cracked hashes given a superhashlist ID
```python
python3 hashie.py export-superhashes -s [superhashlist-id]
```