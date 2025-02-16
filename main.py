# main.py
import requests
import base64
import json
from Crypto.Cipher import AES
import binascii
from datetime import datetime
import os
import yaml

# 控制台艺术字输出
print("      H͜͡E͜͡L͜͡L͜͡O͜͡ ͜͡W͜͡O͜͡R͜͡L͜͡D͜͡ ͜͡E͜͡X͜͡T͜͡R͜͡A͜͡C͜͡T͜͡ ͜͡S͜͡S͜͡ ͜͡N͜͡O͜͡D͜͡E͜͡")
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟")
print("Author : 𝐼𝑢")
print(f"Date   : {datetime.today().strftime('%Y-%m-%d')}")
print("Version: 2.1")
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

# API配置常量
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

def aes_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """使用pycryptodome实现的AES-CBC解密"""
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(ciphertext)
        padding_length = decrypted[-1]
        return decrypted[:-padding_length]
    except (ValueError, IndexError) as e:
        raise ValueError(f"AES解密失败: {str(e)}")

def generate_clash_config(servers: list) -> str:
    """生成Clash配置文件"""
    config = {
        'proxies': [{
            'name': s['title'],
            'type': 'ss',
            'server': s['ip'],
            'port': s['port'],
            'cipher': 'aes-256-cfb',
            'password': s['password'],
            'udp': True
        } for s in servers],
        'proxy-groups': [
            {
                'name': '🔮 选择节点',
                'type': 'select',
                'proxies': ['🚀 自动选择', '🔀 负载均衡'] + [s['title'] for s in servers]
            },
            {
                'name': '🚀 自动选择',
                'type': 'url-test',
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300,
                'tolerance': 50,
                'proxies': [s['title'] for s in servers]
            },
            {
                'name': '🔀 负载均衡',
                'type': 'load-balance',
                'url': 'http://www.gstatic.com/generate_204',
                'interval': 300,
                'proxies': [s['title'] for s in servers]
            }
        ],
        'rules': [
            'GEOIP,CN,DIRECT',
            'DOMAIN-SUFFIX,google.com,🚀 自动选择',
            'DOMAIN-SUFFIX,youtube.com,🔀 负载均衡',
            'MATCH,🔮 选择节点'
        ]
    }
    return yaml.dump(config, allow_unicode=True, sort_keys=False)

def generate_ss_links(servers: list) -> str:
    """生成SS节点文本"""
    links = []
    for s in servers:
        proxy_str = f"aes-256-cfb:{s['password']}@{s['ip']}:{s['port']}"
        b64_str = base64.b64encode(proxy_str.encode()).decode()
        links.append(f"ss://{b64_str}#{s['title']}")
    return "\n".join(links)

def update_gist(clash_content: str, ss_content: str, gist_id: str, pat: str) -> bool:
    """更新Gist文件"""
    try:
        url = f"https://api.github.com/gists/{gist_id}"
        headers = {
            "Authorization": f"token {pat}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "files": {
                "clash.yaml": {"content": clash_content},
                "ss-nodes.txt": {"content": ss_content}
            }
        }
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Gist更新失败: {str(e)}")
        return False

def main():
    try:
        # 获取API数据
        response = requests.post(API_URL, headers=HEADERS, data=PAYLOAD)
        response.raise_for_status()

        # 解密处理
        encrypted_data = binascii.unhexlify(response.text.strip())
        decrypted_data = aes_decrypt(encrypted_data, AES_KEY, AES_IV)
        servers = json.loads(decrypted_data)['data']

        # 生成配置文件
        clash_config = generate_clash_config(servers)
        ss_config = generate_ss_links(servers)

        # 更新Gist
        gist_id = os.environ.get('GIST_LINK')
        gist_pat = os.environ.get('GIST_PAT')
        if gist_id and gist_pat:
            if update_gist(clash_config, ss_config, gist_id, gist_pat):
                print("🎉 配置更新成功")
            else:
                print("❌ Gist更新失败")
        else:
            print("⚠️ 未配置GIST环境变量，跳过更新")

    except json.JSONDecodeError:
        print("❌ JSON解析失败，请检查数据格式")
        exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生未预期错误: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
