# firebase-vuln-detect in APKs - JUST for quick checking of firebase vulns.
Script to check if Firebase Remote Config is enabled, and if enabled grab the contents required to make the POST request and o/p the data obtained

``USAGE : python3 firebasecheck.py /apk/path/folder ``

+ Also checks if .json appended to firebase url exposes any data & notifies about it


**no need of apktools or debugger. script uses strings command to fetch relevant data from the apk and then creates a GET & POST request then sends the request to show the o/p in the terminal**
((project discovery notify integrated)

![gallowaybabu](https://github.com/user-attachments/assets/c3c30026-6bd0-4632-9956-009ce90947e5)



the reason for checking this ::: if someone unknowinlgy leaks sensitive info accidentally in those files 
![image](https://github.com/user-attachments/assets/cad71457-c1ec-4ede-89d6-68eea5581c9b)

