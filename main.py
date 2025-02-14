import os
import requests
import base64
import json
import pyaes
import binascii
import yaml
from datetime import datetime

print("      H͜͡E͜͡L͜͡L͜͡O͜͡ ͜͡W͜͡O͜͡R͜͡L͜͡D͜͡ ͜͡E͜͡X͜͡T͜͡R͜͡A͜͡C͜͡T͜͡ ͜͡S͜͡S͜͡ ͜͡N͜͡O͜͡D͜͡E͜͡")
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟")
print("Author : 𝐼𝑢")
print(f"Date   : {datetime.today().strftime('%Y-%m-%d')}")
print("Version: 2.0 (Clash Edition)")
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟")
print("𝐼𝑢:")
print(r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠁⠀⡰⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡎⢀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀
⣀⠀⠀⠀⠀⠀⠀⡠⠬⡡⠬⡋⠀⡄⠀⠀⠀⠀⠀⠀⠀
⡀⠁⠢⡀⠀⠀⢰⠠⢷⠰⠆⡅⠀⡇⠀⠀⠀⣀⠔⠂⡂
⠱⡀⠀⠈⠒⢄⡸⡑⠊⢒⣂⣦⠄⢃⢀⠔⠈⠀⠀⡰⠁
⠀⠱⡀⠀⠀⡰⣁⣼⡿⡿⢿⠃⠠⠚⠁⠀⠀⢀⠜⠀⠀
⠀⠀⠐⢄⠜⠀⠈⠓⠒⠈⠁⠀⠀⠀⠀⠀⡰⠃⠀⠀⠀
⠀⠀⢀⠊⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠾⡀⠀⠀⠀⠀
⠀⠀⢸⣄⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡇⠀⠀⠀⠀
⠀⠀⠸⢸⣳⠦⣍⣁⣀⣀⣀⣀⣠⠴⠚⠁⠇⠀⠀⠀⠀
⠀⠀⠀⢳⣿⠄⠸⠢⠍⠉⠉⠀⠀⡠⢒⠎⠀⠀⠀⠀⠀
⠀⠀⠀⠣⣀⠁⠒⡤⠤⢤⠀⠀⠐⠙⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠣⡀⡼⠀⠀⠈⠱⡒⠂⡸⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢒⠁⠀⠀⠀⠀⠀⠀⠀
""")

# 配置常量
API_URL = 'http://api.skrapp.net/api/serverlist'
HEADERS = {
    'accept': '/',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'appversion': '1.3.1',
    'user-agent': 'SkrKK/1.3.1 (iPhone; iOS 13.5; Scale/2.00)',
    'content-type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=fnffo1ivhvt0ouo6ebqn86a0d4'
}
POST_DATA = {'data': '4265a9c353cd8624fd2bc7b5d75d2f18b1b5e66ccd37e2dfa628bcb8f73db2f14ba98bc6a1d8d0d1c7ff1ef0823b11264d0addaba2bd6a30bdefe06f4ba994ed'}
AES_KEY = b'65151f8d966bf596'
AES_IV = b'88ca0f0ea1ecf975'

def aes_decrypt(ciphertext, key, iv):
    cipher = pyaes.AESModeOfOperationCBC(key, iv=iv)
    decrypted = b''
    for i in range(0, len(ciphertext), 16):
        decrypted += cipher.decrypt(ciphertext[i:i+16])
    return decrypted[:-decrypted[-1]].decode()

def generate_clash_config(nodes):
    return {
        'proxies': [{
            'name': node['title'],
            'type': 'ss',
            'server': node['ip'],
            'port': node['port'],
            'cipher': 'aes-256-cfb',
            'password': node['password'],
            'udp': True
        } for node in nodes],
        'proxy-groups': [{
            'name': 'PROXY',
            'type': 'select',
            'proxies': [n['title'] for n in nodes]
        }],
        'rules': [
            'GEOIP,CN,DIRECT',
            'MATCH,PROXY'
        ]
    }

def update_gist(content):
    gist_id = os.getenv('GIST_ID')
    pat = os.getenv('GIST_PAT')
    
    response = requests.patch(
        f"https://api.github.com/gists/{gist_id}",
        headers={
            'Authorization': f'Bearer {pat}',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={
            "files": {
                "clash.yaml": {
                    "content": yaml.safe_dump(content, allow_unicode=True, sort_keys=False)
                }
            }
        }
    )
    response.raise_for_status()
    return response.json()['files']['clash.yaml']['raw_url']

try:
    # 获取原始数据
    response = requests.post(API_URL, headers=HEADERS, data=POST_DATA)
    response.raise_for_status()
    
    # 解密数据
    encrypted_data = binascii.unhexlify(response.text.strip())
    decrypted_data = json.loads(aes_decrypt(encrypted_data, AES_KEY, AES_IV))
    
    # 生成订阅内容
    clash_config = generate_clash_config(decrypted_data['data'])
    
    # 更新Gist
    raw_url = update_gist(clash_config)
    
    # 输出结果
    print("\n成功生成Clash订阅：")
    print(f"https://sub.x2n.cc?url={raw_url}&emoji=true")
    
    print("\n原始SS节点：")
    for node in decrypted_data['data']:
        ss_url = f"aes-256-cfb:{node['password']}@{node['ip']}:{node['port']}"
        print(f"ss://{base64.b64encode(ss_url.encode()).decode()}#{node['title']}")

except Exception as e:
    print(f"错误发生：{str(e)}")
    exit(1)
