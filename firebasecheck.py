import subprocess
import re
import requests
import sys
import json
import os
from termcolor import colored

def extract_info_from_apk(apk_path):
    result = subprocess.run(['strings', apk_path], capture_output=True, text=True)
    strings_output = result.stdout
    app_id_match = re.search(r'1:(\d+):android:([a-f0-9]+)', strings_output)
    firebase_url_match = re.search(r'https://[a-zA-Z0-9-]+\.firebaseio\.com', strings_output)
    google_api_key_match = re.search(r'AIza[0-9A-Za-z-_]{35}', strings_output)
    app_id = app_id_match.group(0) if app_id_match else None
    firebase_url = firebase_url_match.group(0) if firebase_url_match else None
    google_api_key = google_api_key_match.group(0) if google_api_key_match else None
    return app_id, firebase_url, google_api_key

def send_alert(message):
    os.system(f'echo "{message}" | notify')

def check_firebase_vulnerability(firebase_url, google_api_key, app_id, apk_name):
    vulnerabilities = []
    curl_command = None
    curl_output = None
    if firebase_url:
        try:
            response = requests.get(f"{firebase_url}/.json", timeout=5)
            if response.status_code == 200:
                vulnerabilities.append("Open Firebase database detected")
                send_alert(f"ALERT: Open Firebase database detected in {apk_name}. URL: {firebase_url}")
                curl_command = f"curl {firebase_url}/.json"
                curl_output = subprocess.run(curl_command, shell=True, capture_output=True, text=True).stdout
            else:
                vulnerabilities.append("Firebase database is not openly accessible")
        except requests.RequestException:
            vulnerabilities.append("Failed to check Firebase database")
    if google_api_key and app_id:
        project_id = app_id.split(':')[1]
        url = f"https://firebaseremoteconfig.googleapis.com/v1/projects/{project_id}/namespaces/firebase:fetch?key={google_api_key}"
        body = {"appId": app_id, "appInstanceId": "required_but_unused_value"}
        try:
            response = requests.post(url, json=body, timeout=5)
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get("state") == "NO_TEMPLATE":
                    vulnerabilities.append("Firebase Remote Config is disabled")
                else:
                    vulnerabilities.append("Firebase Remote Config is enabled")
                    send_alert(f"ALERT: Firebase Remote Config enabled in {apk_name}. URL: {url}")
                    curl_command = f"curl -X POST '{url}' -H 'Content-Type: application/json' -d '{json.dumps(body)}'"
                    curl_output = subprocess.run(curl_command, shell=True, capture_output=True, text=True).stdout
            else:
                vulnerabilities.append(f"Firebase Remote Config check failed: {response.status_code}")
        except requests.RequestException as e:
            vulnerabilities.append(f"Failed to check Firebase Remote Config: {str(e)}")
    return vulnerabilities, curl_command, curl_output

def process_apks_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.apk'):
            apk_path = os.path.join(folder_path, file_name)
            print(colored(f"\nProcessing APK: {file_name}", 'cyan'))
            app_id, firebase_url, google_api_key = extract_info_from_apk(apk_path)
            print(f"App ID: {colored(app_id, 'green')}")
            print(f"Firebase URL: {colored(firebase_url, 'green')}")
            print(f"Google API Key: {colored(google_api_key, 'green')}")
            vulnerabilities, curl_command, curl_output = check_firebase_vulnerability(firebase_url, google_api_key, app_id, file_name)
            print(colored("\nVulnerability Check Results:", 'yellow'))
            for vuln in vulnerabilities:
                print(f"- {colored(vuln, 'red' if 'detected' in vuln else 'green')}")
            if curl_command and curl_output:
                print(colored("\nCurl Command:", 'blue'))
                print(curl_command)
                print(colored("\nCurl Output:", 'magenta'))
                print(curl_output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_folder>")
        sys.exit(1)
    folder_path = sys.argv[1]
    process_apks_in_folder(folder_path)
