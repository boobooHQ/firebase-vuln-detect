# firebase-vuln-detect
Script to check if Firebase Remote Config is enabled, and if enabled grab the contents required to make the POST request and o/p the data obtained

``USAGE : python3 firebasecheck.py /apk/path/folder ``

> this also sends notification using notify command.
> setup notify before use 

``no need of apktools or debugger. it uses strings to fetch relevant data from the apk and then creates a request and send the request to show the o/p in the terminal``
