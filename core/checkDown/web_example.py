import requests

def check(target_ip, target_port):
    """web_example"""
    try:
        # print(target_ip+":"+target_port)
        res = requests.get('http://{}:{}'.format(target_ip,target_port))
        if res.status_code == 200:
            return True
        return False
    except Exception as e:
        print(e)
        return False


def test():
    print("hi!")
    return "check down yes"

if __name__ == '__main__':
    target_ip, target_port = '127.0.0.1', 8801
    check(target_ip, target_port)
