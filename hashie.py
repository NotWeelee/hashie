from Hashtopolis import Hashtopolis
from termcolor import cprint
import click
import json
import os
import base64

CONTEXT_SETTINGS = dict(help_option_names=['--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('action')
@click.option('-h', '--hashtopolis', help='Hostname Of Hashtopolis Instance', required=False, metavar='')
@click.option('-p', '--port', help='Port For Hashtopolis', default=443, show_default=True, required=False, metavar='')
@click.option('-a', '--api-key', help='API Key For Hashtopolis', required=False, metavar='')
@click.option('-i', '--hashlist-id', help='Hashlist ID', required=False, metavar='')
@click.option('-s', '--superhashlist-id', help='Superhashlist ID', required=False, metavar='')
@click.option('-n', '--hashlist-name', help='Hashlist Name', required=False, metavar='')
@click.option('-t', '--hashtype', help='Hashlist Type (ntlm, ntlmv2, kerbtgt23)', type=click.Choice(['ntlm', 'ntlmv2', 'kerbtgt23'], case_sensitive=False), required=False, metavar='')
@click.option('-f', '--hash-file', help='File containing your hashes', required=False, metavar='')
@click.option('--num-tasks', help='Number Of Tasks To Get', default=15, show_default=True, required=False, metavar='')
@click.option('--num-hashlists', help='Number Of Hashlists To Get', default=15, show_default=True, required=False, metavar='')
@click.option('--priority', help='Set your new task to have the highest priority', is_flag=True, required=False, metavar='')

def main(action, hashtopolis, port, api_key, hashlist_id, superhashlist_id, hashlist_name, hashtype, hash_file, num_tasks, num_hashlists, priority):
    
    """
    hashie v1.3.0
    
    Available ACTIONs:
    
    \b
        list-tasks
        list-hashlists
        list-superhashlists
        create-task
        find-hashlist
        export-hashes
        export-superhashes
    """

    if os.path.exists("/root/.hashie/config.json"):
        config = open("/root/.hashie/config.json","r")
        data = json.load(config)
        hashie = Hashtopolis(str(data["hashtopolis"]), str(data["port"]), str(data["apiKey"]))
    else:
        hashie = Hashtopolis(hashtopolis, port, api_key)

    match action:
        case "list-tasks":
            hashie.listTasks(num_tasks)
        case "list-hashlists":
            hashie.listHashlists(num_hashlists)
        case "list-superhashlists":
            hashie.listSuperhashlists(num_hashlists)
        case "create-task":
            hashtypeNum = 0
            superhashNum = 0
            if hashlist_name is None:
                cprint('\n[-] Need a name for your hashlist. Use -n/--hashlist-name flag.\n', 'red')
                exit()
            if hashtype is None:
                cprint('\n[-] Need a hashtype for your hashlist. Use -t/--hashtype flag.\n\nChoose from ntlm, ntlmv2, kerbtgt23\n', 'red')
                exit()
            if hash_file is None:
                cprint('\n[-] Need a file containing your hashes. Use -f/--hash-file flag.\n', 'red')
                exit()

            if hashtype == 'ntlm':
                hashtypeNum = 1000
                superhashNum = 20
            elif hashtype == 'ntlmv2':
                hashtypeNum = 5600
                superhashNum = 19
            elif hashtype == 'kerbtgt23':
                hashtypeNum = 13100
                superhashNum = 19

            with open(hash_file, 'rb') as textFile:
                convert = base64.b64encode(textFile.read())
            datablob = convert.decode('utf-8')

            hashlistId = hashie.createHashlist(hashlist_name, hashtypeNum, datablob)
            if hashlistId is not False:
                cprint('\n[+] Created hashlist ' + str(hashlist_name) + '!', 'blue')
                runResult = hashie.runSupertask(hashlistId, superhashNum)
            else:
                cprint('\n[-] Failed to create hashlist ' + str(hashlist_name) + '. See error below:\n', 'red')
                print(hashlistId)
            if runResult is True:
                cprint('[+] Started a supertask for hashlist ' + str(hashlistId) + '!', 'blue')
            else:
                cprint('\n[-] Failed to start supertask for hashlist ' + str(hashlistId) + '. See error below:\n', 'red')
                print(runResult)

            if priority:
                highPriority = hashie.getHighestPriority()
                highPriority += 1
                highPriority = highPriority - (highPriority % -10)
                supertaskId = hashie.getSupertaskId(hashlistId)
                setPriority = hashie.setSupertaskPriority(supertaskId, highPriority)
            if setPriority is True:
                cprint('[+] Set supertask priority to ' + str(highPriority) + '!', 'blue')
            else:
                cprint('\n[-] Failed to set supertask priority for supertaskId ' + str(supertaskId) + '. See error below:\n', 'red')
                print(setPriority)
        case "find-hashlist":
            if hashlist_name is None:
                cprint('\n[-] Need hashlist name to search for. Use -n/--hashlist-name flag.\n', 'red')
                exit()
            else:
                hashie.listHashlistFromName(hashlist_name)
        case "export-hashes":
            if hashlist_id is None:
                cprint('\n[-] Need hashlist ID to export hashes to file. Use -i/--hashlist-id flag.\n', 'red')
                cprint('    Try python3 hashie.py find-hashlist -n [hashlist_name] to get your hashlist ID.\n', 'yellow')
                exit()
            else:
                cprint('\n[*] Getting cracked hashes from hashlist ' + str(hashlist_id), 'yellow')
                crackedHashes = hashie.exportCracked(hashlist_id)
                file = open('crackedHashes.potfile', 'w')
                for hashes in crackedHashes:
                    file.write(str(hashes) + "\n")
                file.close()
                cprint('\n[+] All done, check out crackedHashes.potfile!', 'blue')
        case "export-superhashes":
            if superhashlist_id is None:
                cprint("\n[-] Need superhashlist ID. Use -s/--superhashlist-id flag.\n", 'red')
                cprint('    Try python3 hashie.py find-hashlist -n [hashlist_name] to get your (super)hashlist ID.\n', 'yellow')
                exit()
            else:
                hashlistIds = hashie.getHashlistsFromSuperhashlist(superhashlist_id)
                cprint('\n[*] Superhashlist ' + str(superhashlist_id) + ' has ' + str(len(hashlistIds)) + ' hashlists\n', 'green')
                file = open('crackedHashes.potfile','w')
                crackedHashes = []
                for hashlistId in hashlistIds:
                    cprint('[*] Getting cracked hashes from hashlist ' + str(hashlistId), 'yellow')
                    currentHashlist = hashie.exportCracked(str(hashlistId))
                    for hash in currentHashlist:
                        crackedHashes.append(hash)
                for hashes in crackedHashes:
                    file.write(str(hashes) + '\n')
                file.close()
                cprint('\n[+] All done, check out crackedHashes.potfile!', 'blue')
        case default:
            cprint('\n[-] ' + action + " is not a valid action.\n", 'red')
            print('Available ACTIONs:\n')
            print("list-tasks            List highest priority tasks\n" +
                  "list-hashlists        List recently added hashlists\n" +
                  "list-superhashlists   List recently added superhashlists\n" +
                  "create-task           Create a new hashlist and start a supertask for it\n" +
                  "find-hashlist         Find matching hashlists from name\n" +
                  "export-hashes         Export cracked hashes for given hashlist ID\n" +
                  "export-superhashes    Export cracked hashes for given superhashlist ID\n"
                  )
            exit()


if __name__ == "__main__":
    main()