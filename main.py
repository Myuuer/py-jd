# main.py
import requests
import base64
import json
from Crypto.Cipher import AES  # 修改后的加密模块导入
import binascii
from datetime import datetime
import os
import yaml

# 控制台艺术字输出（保持原有样式不变）
print("      H͜͡E͜͡L͜͡L͜͡O͜͡ ͜͡W͜͡O͜͡R͜͡L͜͡D͜͡ ͜͡E͜͡X͜͡T͜͡R͜͡A͜͡C͜͡T͜͡ ͜͡S͜͡S͜͡ ͜͡N͜͡O͜͡D͜͡E͜͡")
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟")
print("Author : 𝐼𝑢")
print(f"Date   : {datetime.today().strftime('%Y-%m-%d')}")
print("Version: 2.1")  # 更新版本号
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟")
print("𝐼𝑢:")
# ... [保持原有艺术字图案不变] ...

# API配置常量（保持不变）
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

# ... [保持原有generate_clash_config、generate_ss_links、update_gist函数不变] ...

def main():
    try:
        # 获取API数据（保持不变）
        response = requests.post(API_URL, headers=HEADERS, data=PAYLOAD)
        response.raise_for_status()

        # 解密处理（使用修改后的解密函数）
        encrypted_data = binascii.unhexlify(response.text.strip())
        decrypted_data = aes_decrypt(encrypted_data, AES_KEY, AES_IV)
        servers = json.loads(decrypted_data)['data']

        # 生成配置文件（保持不变）
        clash_config = generate_clash_config(servers)
        ss_config = generate_ss_links(servers)

        # 更新Gist（保持不变）
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
