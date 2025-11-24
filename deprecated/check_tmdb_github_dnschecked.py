import requests
from time import sleep
import random
import time
import os
import sys
from datetime import datetime, timezone, timedelta
from retry import retry
import socket

# DNS服务器的字典
dns_server = {
    "south-korea-dns": ["202.46.34.75", "168.126.63.1"],
    "japan-dns": ["202.248.37.74", "202.248.20.133"]
}

DOMAINS = [
    'tmdb.org',
    'api.tmdb.org',
    'files.tmdb.org',
    'themoviedb.org',
    'api.themoviedb.org',
    'www.themoviedb.org',
    'auth.themoviedb.org',
    'image.tmdb.org',
    'images.tmdb.org',
    'imdb.com',
    'www.imdb.com',
    'secure.imdb.com',
    's.media-imdb.com',
    'us.dd.imdb.com',
    'www.imdb.to',
    'origin-www.imdb.com',
    'ia.media-imdb.com',
    'thetvdb.com',
    'api.thetvdb.com',
    'ia.media-imdb.com',
    'f.media-amazon.com',
    'imdb-video.media-imdb.com'
]

Tmdb_Host_TEMPLATE = """# Tmdb Hosts Start
{content}
# Update time: {update_time}
# IPv4 Update url: https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/cnwikee/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/cnwikee/CheckTMDB
# Tmdb Hosts End\n"""

def write_file(ipv4_hosts_content: str, ipv6_hosts_content: str, update_time: str) -> bool:
    output_doc_file_path = os.path.join(os.path.dirname(__file__), "README.md")
    template_path = os.path.join(os.path.dirname(__file__), "README_template.md")
    
    if os.path.exists(output_doc_file_path):
        with open(output_doc_file_path, "r", encoding='utf-8') as old_readme_md:
            old_readme_md_content = old_readme_md.read()            
            if old_readme_md_content:
                old_ipv4_block = old_readme_md_content.split("```bash")[1].split("```")[0].strip()
                old_ipv4_hosts = old_ipv4_block.split("# Update time:")[0].strip()

                old_ipv6_block = old_readme_md_content.split("```bash")[2].split("```")[0].strip()
                old_ipv6_hosts = old_ipv6_block.split("# Update time:")[0].strip()
                
                if ipv4_hosts_content != "":
                    new_ipv4_hosts = ipv4_hosts_content.split("# Update time:")[0].strip()
                    if old_ipv4_hosts == new_ipv4_hosts:
                        print("ipv4 host not change")
                        w_ipv4_block = old_ipv4_block
                    else:
                        w_ipv4_block = ipv4_hosts_content
                        write_host_file(ipv4_hosts_content, 'ipv4')
                else:
                    print("ipv4_hosts_content is null")
                    w_ipv4_block = old_ipv4_block

                if ipv6_hosts_content != "":
                    new_ipv6_hosts = ipv6_hosts_content.split("# Update time:")[0].strip()
                    if old_ipv6_hosts == new_ipv6_hosts:
                        print("ipv6 host not change")
                        w_ipv6_block = old_ipv6_block
                    else:
                        w_ipv6_block = ipv6_hosts_content
                        write_host_file(ipv6_hosts_content, 'ipv6')
                else:
                    print("ipv6_hosts_content is null")
                    w_ipv6_block = old_ipv6_block
                
                with open(template_path, "r", encoding='utf-8') as temp_fb:
                    template_str = temp_fb.read()
                    hosts_content = template_str.format(ipv4_hosts_str=w_ipv4_block, ipv6_hosts_str=w_ipv6_block, update_time=update_time)

                    with open(output_doc_file_path, "w", encoding='utf-8') as output_fb:
                        output_fb.write(hosts_content)
                return True
        return False
               
                

def write_host_file(hosts_content: str, filename: str) -> None:
    output_file_path = os.path.join(os.path.dirname(__file__), "Tmdb_host_" + filename)
    if len(sys.argv) >= 2 and sys.argv[1].upper() == '-G':
        print("\n~追加Github ip~")
        hosts_content = hosts_content + "\n" + (get_github_hosts() or "")
    with open(output_file_path, "w", encoding='utf-8') as output_fb:
        output_fb.write(hosts_content)
        print("\n~最新TMDB" + filename + "地址已更新~")

def get_github_hosts() -> None:
    github_hosts_urls = [
        "https://hosts.gitcdn.top/hosts.txt",
        "https://raw.githubusercontent.com/521xueweihan/GitHub520/refs/heads/main/hosts",
        "https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts",
        "https://raw.githubusercontent.com/ittuann/GitHub-IP-hosts/refs/heads/main/hosts_single"
    ]
    all_failed = True
    for url in github_hosts_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                github_hosts = response.text
                all_failed = False
                break
            else:
                print(f"\n从 {url} 获取GitHub hosts失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"\n从 {url} 获取GitHub hosts时发生错误: {str(e)}")
    if all_failed:
        print("\n获取GitHub hosts失败: 所有Url项目失败！")
        return
    else:
        return github_hosts

def is_ci_environment():
    ci_environment_vars = {
        'GITHUB_ACTIONS': 'true',
        'TRAVIS': 'true',
        'CIRCLECI': 'true'
    }
    for env_var, expected_value in ci_environment_vars.items():
        env_value = os.getenv(env_var)
        if env_value is not None and str(env_value).lower() == expected_value.lower():
            return True
    return False
    
@retry(tries=3)
def get_domain_ips(domain, record_type, dns_server):
    """
    从指定的DNS服务器列表中获取域名的IP列表
    确保遍历所有传入的DNS服务器
    """
    all_ips = []  # 存储所有DNS服务器返回的IP
    
    # 确保dns_server是列表格式
    if not isinstance(dns_server, list):
        dns_server = [dns_server]

    for dns in dns_server:
        print(f"正在从DNS服务器 {dns} 获取 {domain} 的{record_type}记录...")
        url = f'https://api.dnschecked.com/query_dns'
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",  # 关键：指定JSON格式负载
            "origin": "https://dnschecked.com",
            "referer": "https://dnschecked.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
        }

        params = {
            'domain': domain,
            'record_type': record_type,
            'dns_server': dns
        }

        # 初始化IP列表（默认空列表，确保后续使用安全）
        ips_str = []

        try:
            response = requests.post(url, headers=headers, json=params, timeout=10)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        ips_str = data.get("results", [])
                        print(f"请求成功，提取到IP列表：{ips_str}")
                        all_ips.extend(ips_str) if ips_str else []
                    else:
                        print(f"从DNS服务器 {dns} 获取 {domain} 的IP列表失败：返回数据不是字典格式")
                except ValueError:
                    print(f"错误：响应内容不是有效的JSON格式, 响应内容：{response.text}")
            else:
                print(f"请求失败，HTTP状态码：{response.status_code}，响应内容：{response.text}")
                continue
        except requests.exceptions.RequestException as e:
            # 捕获所有网络请求相关异常（如连接超时、DNS解析失败等）
            print(f"从DNS服务器 {dns} 获取数据时JSON解析失败: {e}")
        time.sleep(1)

    # 去重并返回所有IP
    return list(set(all_ips))

def ping_ip(ip, port=80):
    print(f"使用TCP连接测试IP地址的延迟（毫秒）")
    try:
        print(f"\n开始 ping {ip}...")
        start_time = time.time()
        with socket.create_connection((ip, port), timeout=2) as sock:
            latency = (time.time() - start_time) * 1000  # 转换为毫秒
            print(f"IP: {ip} 的平均延迟: {latency}ms")
            return latency
    except Exception as e:
        print(f"Ping {ip} 时发生错误: {str(e)}")
        return float('inf')
    
def find_fastest_ip(ips):
    """找出延迟最低的IP地址"""
    if not ips:
        return None
    
    fastest_ip = None
    min_latency = float('inf')
    ip_latencies = []  # 存储所有IP及其延迟
    
    for ip in ips:
        ip = ip.strip()
        if not ip:
            continue
            
        print(f"正在测试 IP: {ip}")
        latency = ping_ip(ip)
        ip_latencies.append((ip, latency))
        print(f"IP: {ip} 延迟: {latency}ms")
        
        if latency < min_latency:
            min_latency = latency
            fastest_ip = ip
            
        sleep(0.5) 
    
    print("\n所有IP延迟情况:")
    for ip, latency in ip_latencies:
        print(f"IP: {ip} - 延迟: {latency}ms")
    
    if fastest_ip:
        print(f"\n最快的IP是: {fastest_ip}，延迟: {min_latency}ms")
    
    return fastest_ip

def main():
    print("开始检测TMDB相关域名的最快IP...")

    ipv4_ips, ipv6_ips, ipv4_results, ipv6_results = [], [], [], []

    for domain in DOMAINS:
        print(f"\n正在处理域名: {domain}")       
        ipv4_ips = get_domain_ips(domain, "A", dns_server["japan-dns"])
        ipv6_ips = get_domain_ips(domain, "AAAA", dns_server["japan-dns"])

        if not ipv4_ips and not ipv6_ips:
            print(f"无法获取 {domain} 的IP列表，跳过该域名")
            continue
        
        # 处理 IPv4 地址
        if ipv4_ips:
            fastest_ipv4 = find_fastest_ip(ipv4_ips)
            if fastest_ipv4:
                ipv4_results.append([fastest_ipv4, domain])
                print(f"域名 {domain} 的最快IPv4是: {fastest_ipv4}")
            else:
                ipv4_results.append([ipv4_ips[0], domain])
        
        # 处理 IPv6 地址
        if ipv6_ips:
            fastest_ipv6 = find_fastest_ip(ipv6_ips)
            if fastest_ipv6:
                ipv6_results.append([fastest_ipv6, domain])
                print(f"域名 {domain} 的最快IPv6是: {fastest_ipv6}")
            else:
                # 兜底：可能存在无法正确获取 fastest_ipv6 的情况，则将第一个IP赋值
                ipv6_results.append([ipv6_ips[0], domain])
        
        sleep(1)  # 避免请求过于频繁
    
    # 保存结果到文件
    if not ipv4_results and not ipv6_results:
        print(f"程序出错：未获取任何domain及对应IP，请检查接口~")
        sys.exit(1)

    # 生成更新时间
    update_time = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
    
    ipv4_hosts_content = Tmdb_Host_TEMPLATE.format(content="\n".join(f"{ip:<27} {domain}" for ip, domain in ipv4_results), update_time=update_time) if ipv4_results else ""
    ipv6_hosts_content = Tmdb_Host_TEMPLATE.format(content="\n".join(f"{ip:<50} {domain}" for ip, domain in ipv6_results), update_time=update_time) if ipv6_results else ""

    write_file(ipv4_hosts_content, ipv6_hosts_content, update_time)


if __name__ == "__main__":
    main()
