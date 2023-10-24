import requests
import json

class Hashtopolis:
    def __init__(self, hostname="", port="", apiKey=""):
        self.uri = "https://" + str(hostname) + ":" + str(port) + "/api/user.php"
        self.apiKey = str(apiKey)

    # ---------------------------------------------------------------------------------------------------------------------#

    # List all tasks
    #
    # IN  |  numTasks - Number of tasks to list (Default to 10)
    # OUT |  Prints numHashlists recent Hashlists and their IDs
    def listTasks(self, numTasks):
        post_json = {
            "section": "task",
            "request": "listTasks",
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        for x in range(numTasks):
            print(resp.json()['tasks'][x])

    # List all hashlists starting from the most recently uploaded ones
    #
    # IN  |  numHashlists - Number of Hashlists to list
    # OUT |  Prints numHashlists recent Hashlists and their IDs
    def listHashlists(self, numHashlists):
        post_json = {
            "section": "hashlist",
            "request": "listHashlists",
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        startIndex = -1
        for x in range(startIndex, startIndex - numHashlists, -1):
            print(resp.json()['hashlists'][x])

    # List all Superhashlists
    #
    # IN  |  numHashlists - Number of Hashlists to list
    # OUT |  Prints numHashlists recent Hashlists and their IDs
    def listSuperhashlists(self, numHashlists):
        post_json = {
            "section": "superhashlist",
            "request": "listSuperhashlists",
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        startIndex = -1
        for x in range(startIndex, startIndex - numHashlists, -1):
            print(resp.json()['superhashlists'][x])

    # List all hashlists that contain the given hashlistName
    #
    # IN  |  hashlistName - Hashlist name to search for
    # OUT |  Prints Hashlists that contain hashlistName
    def listHashlistFromName(self, hashlistName):
        post_json = {
            "section": "hashlist",
            "request": "listHashlists",
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        startIndex = -1
        for x in range(startIndex, startIndex - len(resp.json()['hashlists']), -1):
            if str(hashlistName).lower() in str(resp.json()['hashlists'][x]["name"]).lower():
                print(resp.json()['hashlists'][x])

    # List all Supertasks
    #
    # IN  |  None :)
    # OUT |  Prints Supertasks and their respective IDs
    def listSupertasks(self):
        post_json = {
            "section": "supertask",
            "request": "listSupertasks",
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        for x in range(len(resp.json()['supertasks'])):
            print(resp.json()['supertasks'][x])

    # Return the current highest priority
    #
    # IN  |  None
    # OUT |  Returns an integer of the current highest priority
    def getHighestPriority(self):
        post_json = {
            "section": "task",
            "request": "listTasks",
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        return resp.json()['tasks'][0]['priority']

    # Return the SupertaskId given a hashlistId
    #
    # IN  |  hashlistId to check for a SupertaskId for
    # OUT |  Returns an integer of the SupertaskId assosicated with the hashlistId if it exists
    def getSupertaskId(self, hashlistId):
        post_json = {
            "section": "task",
            "request": "listTasks",
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        for x in range(20):
            if resp.json()['tasks'][x]['hashlistId'] == hashlistId:
                return resp.json()['tasks'][x]['supertaskId']
        return False

    # ---------------------------------------------------------------------------------------------------------------------#

    # Return all Hashlists in list format for a given SuperhashlistID
    #
    # IN  |  SuperhashlistID - ID of the Superhashlist that you want to obtain the hashlist ID for
    # OUT |  Returns Hashlists that are part of the Superhashlist
    def getHashlistsFromSuperhashlist(self, SuperhashlistId):
        post_json = {
            "section": "superhashlist",
            "request": "getSuperhashlist",
            "accessKey": self.apiKey,
            "superhashlistId": SuperhashlistId
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        return resp.json()["hashlists"]

    # Return a list of most recent 20 tasks
    #
    # IN  |  None!
    # OUT |  Returns list of 20 most recent tasks and their details
    def getTasks(self):
        post_json = {
            "section":"task",
            "request":"listTasks",
            "accessKey":self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        tasks = []
        for x in range(20):
            tasks.append(resp.json()['tasks'][x])
        return tasks

    # Create a hashlist by uploading hashes in a base64 blob
    #
    # IN  |  hashlistName - What you want to name your new hashlist
    #        hashtypeId   - Type of hash (NTLM 1000, NTLMv2 5600, kerbtgt23 13100)
    #        dataBlob
    # OUT |  Returns list of 20 most recent tasks and their details
    def createHashlist(self, hashlistName, hashtypeId, dataBlob):
        post_json = {
            "section": "hashlist",
            "request": "createHashlist",
            "name": hashlistName,
            "isSalted": False,
            "isSecret": False,
            "isHexSalt": False,
            "separator": ":",
            "format": 0,
            "hashtypeId": hashtypeId,
            "accessGroupId": 1,
            "data": dataBlob,
            "useBrain": False,
            "brainFeatures": 0,
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            print(resp.json())
            return False
        elif resp.json()['response'] == 'OK':
            return resp.json()['hashlistId']
    
    # Run a supertask
    #
    # IN  |  hashtypeId  - Hashlist you want to start
    #        supertaskId - Supertask to run
    #                      Fast Hashes v1.1 (19)
    #                      Slow Hashes v1.1 (20)
    # OUT |  Returns list of 20 most recent tasks and their details
    def runSupertask(self, hashlistId, supertaskId):
        post_json = {
            "section": "task",
            "request": "runSupertask",
            "hashlistId": hashlistId,
            "supertaskId": supertaskId,
            "crackerVersionId": 2,
            "accessKey": self.apiKey
        }
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        elif resp.json()['response'] == 'OK':
            return True

    # Get all cracked hashes in list format for a given hashlistID
    #
    # IN  |  hashlistID - ID of the Hashlist that you want to get all cracked hashes for
    # OUT |  Returns a list of cracked hashes for the given hashlistID
    def exportCracked(self, hashlistID):
        post_json = {"section":"hashlist", "request":"getCracked", "accessKey":self.apiKey, "hashlistId":hashlistID}
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        crackedHashes = []
        for x in range(len(resp.json()['cracked'])):
            crackedHashes.append(resp.json()['cracked'][x]['hash'] + ':' + resp.json()['cracked'][x]['plain'])
        return crackedHashes

    # Set priority of a supertaskId
    #
    # IN  |  supertaskId - ID of the task that you want to change priority for
    #        priority    - Priority value you want to set for your supertask
    # OUT |  Returns a list of cracked hashes for the given hashlistID
    def setSupertaskPriority(self, supertaskId, priority):
        post_json = {
            "section":"task",
            "request":"setSupertaskPriority",
            "supertaskId":supertaskId,
            "supertaskPriority":priority,
            "accessKey":self.apiKey}
        resp = requests.post(self.uri, json = post_json)
        if resp.json()['response'] == 'ERROR':
            return resp.json()
        return True

def main():
    hashie = Hashtopolis('hash.toastshell.com', apiKey='70PF9iGcC8M1bwkY2G6lygCAk195GM')
    hashie.listTasks(10)
    print(hashie.getSupertaskId(2014))

if __name__ == "__main__":
    main()