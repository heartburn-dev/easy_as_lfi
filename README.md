# EASY AS LFI! 
## Automated Local File Inclusion Discovery

Local File Inclusion occurs when an attacker can trick a web application to include files on the web server that should be innaccessible. It occurs when a developer fails to sanitized user input and allows the inclusion of any page. 

For example, the developer might be expecting the input to be "EN" to provide an English welcome page, which could look like  http://example.com?language=EN this. In this scenario, if there is an inclusion of the EN page in the file system, it will display the requested language. However, if input is not sanitized and checked, it may lead to an attacker requesting different pages using a path traversal: http://example.com?language=../../../../../../etc/passwd.

# Instructions

When you've found a vulnerable parameter, plug the url into the tool by opening the script in a text editor and replacing the url string up to the '=' sign. If necessary, edit the number of ../../../ that the script uses manually.

When that's been set, run the script with either a single file or wordlist, specifying if you want to try and convert from base64 or just using standard html. The former is useful when files contain server side languages that do not get interpreted in the browser, such as php, to read sensitive data that the standard LFI would not provide. 

The website must be vulnerable to the php://filter to use the base64 setting.

```bash
python3 easy_as_lfi.py b64 file /etc/passwd
```

```bash
python3 easy_as_lfi.py b64 wordlist common_files.txt
```
![image](https://user-images.githubusercontent.com/59886240/121222307-56a4af80-c87e-11eb-8a40-f91024c33a4a.png)

# Notes

- I've left a wordlist "common_files.txt" in the git repository to use as a wordlist. It is by no means comprehensive.
- You will need to manually adjust the tool to your needs by adding your own URL to the script. 
- Make sure the directory you are running it from is writeable so results can be saved.
- I'd advise running it from a different directory for each test so your files don't get confusing.
