# main.py
import requests
import base64
import json
import pyaes
import binascii
from datetime import datetime
import os
import yaml  # 新增PyYAML库

# 控制台输出（保持原有样式）
print("      H͜͡E͜͡L͜͡L͜͡O͜͡ ͜͡W͜͡O͜͡R͜͡L͜͡D͜͡ ͜͡E͜͡X͜͡T͜͡R͜͡A͜͡C͜͡T͜͡ ͜͡S͜͡S͜͡ ͜͡N͜͡O͜͡D͜͡E͜͡")
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟")
print("Author : 𝐼𝑢")
print(f"Date   : {datetime.today().strftime('%Y-%m-%d')}")
print("Version: 1.0")
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

# API请求配置（保持原有参数）
API_URL = 'http://api.skrapp.net/api/serverlist'
HEADERS = {
    'accept': '/',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'appversion': '1.3.1',
    'user-agent': 'SkrKK/1.3.1 (iPhone; iOS 13.5; Scale/2.00)',
    'content-type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=fnffo1ivhvt0ouo6ebqn86a0d4'
}
PAYLOAD = {'data': '4265a9c353cd8624fd2bc7b5d75d2f18b1b5e66ccd37e2dfa628bcb8f73db2f14ba98bc6a1d8d0d1c7ff1ef0823b11264d0addaba2bd6a30bdefe06f4ba994ed'}
AES_KEY = b'65151f8d966bf596'
AES_IV = b'88ca0f0ea1ecf975'

# AES解密函数（保持原有逻辑）
def aes_decrypt(ciphertext, key, iv):
    aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
    decrypted = b''.join(aes.decrypt(ciphertext[i:i+16]) for i in range(0, len(ciphertext), 16))
    padding_length = decrypted[-1]
    return decrypted[:-padding_length]

# Gist更新函数
def update_gist(content, gist_id, pat):
    url = f"https://api.github.com/gists/{gist_id}"
    headers = {"Authorization": f"token {pat}", "Accept": "application/vnd.github.v3+json"}
    data = {"files": {"clash.yaml": {"content": content}}}
    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 200

# 主逻辑
try:
    # 请求API并解密数据
    response = requests.post(API_URL, headers=HEADERS, data=PAYLOAD)
    if response.status_code != 200:
        print(f"API请求失败，状态码：{response.status_code}")
        exit(1)

    encrypted_data = binascii.unhexlify(response.text.strip())
    decrypted_data = aes_decrypt(encrypted_data, AES_KEY, AES_IV)
    servers = json.loads(decrypted_data)['data']

    # 构建Clash配置
    clash_config = {
        'proxies': [
            {
                'name': server['title'],
                'type': 'ss',
                'server': server['ip'],
                'port': server['port'],
                'cipher': 'aes-256-cfb',
                'password': server['password'],
                'udp': True
            } for server in servers
        ],
        # 新增策略组配置 ################################
        'proxy-groups': [
            {
                'name': '🔮 选择节点',
                'type': 'select',
                'proxies': ['🚀 自动选择', '🔀 负载均衡'] + [server['title'] for server in servers]
            },
            {
                'name': '🚀 自动选择',
                'type': 'url-test',
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300,
                'tolerance': 50,
                'proxies': [server['title'] for server in servers]  # 自动包含所有节点
            },
            {
                'name': '🔀 负载均衡',
                'type': 'load-balance',
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300,
                'proxies': [server['title'] for server in servers]  # 包含所有节点
            }
        ],
        # 更新规则配置 ################################
        'rules': [
            'GEOIP,CN,DIRECT',
            'DOMAIN-SUFFIX,google.com,🚀 自动选择',  # 指定 Google 走自动选择
            'DOMAIN-SUFFIX,youtube.com,🔀 负载均衡', # 视频走负载均衡
            'MATCH,选择节点'  # 默认规则
        ]
    }

    # 生成YAML
    yaml_content = yaml.dump(clash_config, allow_unicode=True, sort_keys=False)
    with open('clash.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print("本地文件 clash.yaml 生成成功")

    # 更新到Gist
    GIST_ID = os.environ.get('GIST_LINK')
    GIST_PAT = os.environ.get('GIST_PAT')
    if GIST_ID and GIST_PAT:
        if update_gist(yaml_content, GIST_ID, GIST_PAT):
            print("Gist更新成功")
        else:
            print("Gist更新失败")
    else:
        print("未配置GIST_LINK或GIST_PAT，跳过Gist更新")

except Exception as e:
    print(f"程序运行出错：{str(e)}")
    exit(1)
