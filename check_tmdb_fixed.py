#!/usr/bin/env python3
"""
修复版本: 使用本地 DNS 解析 + 多种备用方案
"""
import requests
from time import sleep
import time
import os
import sys
from datetime import datetime, timezone, timedelta
from retry import retry
import socket

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
    with open(output_file_path, "w", encoding='utf-8') as output_fb:
        output_fb.write(hosts_content)
        print(f"\n~最新TMDB {filename} 地址已更新~")

@retry(tries=3)
def get_domain_ips_method1_dnschecked(domain, record_type, dns_servers):
    """
    方法1: 使用 dnschecked.com API (原方法)
    """
    all_ips = []
    
    if not isinstance(dns_servers, list):
        dns_servers = [dns_servers]

    for dns in dns_servers:
        print(f"  [方法1] 通过 dnschecked API + DNS {dns} 查询...")
        url = 'https://api.dnschecked.com/query_dns'
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://dnschecked.com",
            "referer": "https://dnschecked.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        params = {
            'domain': domain,
            'record_type': record_type,
            'dns_server': dns
        }

        try:
            response = requests.post(url, headers=headers, json=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict):
                    ips_str = data.get("results", [])
                    if ips_str:
                        all_ips.extend(ips_str)
                        print(f"    ✓ 成功获取: {ips_str}")
        except Exception as e:
            print(f"    ✗ 失败: {e}")
        
        time.sleep(0.5)

    return list(set(all_ips))

def get_domain_ips_method2_socket(domain, record_type):
    """
    方法2: 使用系统 DNS 解析 (socket.getaddrinfo)
    """
    print(f"  [方法2] 使用系统 DNS 解析...")
    ips = []
    
    try:
        if record_type == "A":
            results = socket.getaddrinfo(domain, None, socket.AF_INET)
            ips = list(set([x[4][0] for x in results]))
        elif record_type == "AAAA":
            results = socket.getaddrinfo(domain, None, socket.AF_INET6)
            ips = list(set([x[4][0] for x in results]))
        
        if ips:
            print(f"    ✓ 成功获取: {ips}")
        else:
            print(f"    ✗ 未获取到IP")
            
    except Exception as e:
        print(f"    ✗ 失败: {e}")
    
    return ips

def get_domain_ips_method3_cloudflare(domain, record_type):
    """
    方法3: 使用 Cloudflare DNS-over-HTTPS
    """
    print(f"  [方法3] 使用 Cloudflare DoH...")
    ips = []
    
    try:
        url = f"https://cloudflare-dns.com/dns-query?name={domain}&type={record_type}"
        headers = {"accept": "application/dns-json"}
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "Answer" in data:
                for answer in data["Answer"]:
                    if "data" in answer:
                        ips.append(answer["data"])
                
                if ips:
                    print(f"    ✓ 成功获取: {ips}")
                else:
                    print(f"    ✗ 响应中无数据")
        else:
            print(f"    ✗ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"    ✗ 失败: {e}")
    
    return list(set(ips))

def get_domain_ips(domain, record_type, dns_servers=None):
    """
    综合方法: 依次尝试多种方式获取 IP
    """
    print(f"\n正在获取 {domain} 的 {record_type} 记录...")
    
    all_ips = []
    
    # 尝试方法1: dnschecked API
    if dns_servers:
        ips = get_domain_ips_method1_dnschecked(domain, record_type, dns_servers)
        all_ips.extend(ips)
    
    # 如果方法1失败,尝试方法2: 系统DNS
    if not all_ips:
        ips = get_domain_ips_method2_socket(domain, record_type)
        all_ips.extend(ips)
    
    # 如果方法2失败,尝试方法3: Cloudflare DoH
    if not all_ips:
        ips = get_domain_ips_method3_cloudflare(domain, record_type)
        all_ips.extend(ips)
    
    # 去重
    all_ips = list(set(all_ips))
    
    if all_ips:
        print(f"✓ 最终获取到 {len(all_ips)} 个IP: {all_ips}")
    else:
        print(f"✗ 所有方法均失败，未获取到IP")
    
    return all_ips

def ping_ip(ip, port=80):
    """TCP 延迟测试"""
    try:
        start_time = time.time()
        with socket.create_connection((ip, port), timeout=2) as sock:
            latency = (time.time() - start_time) * 1000
            return latency
    except Exception as e:
        print(f"  Ping {ip} 失败: {e}")
        return float('inf')

def find_fastest_ip(ips):
    """找出延迟最低的IP地址"""
    if not ips:
        return None
    
    fastest_ip = None
    min_latency = float('inf')
    
    print(f"\n  开始测试 {len(ips)} 个IP的延迟...")
    
    for ip in ips:
        ip = ip.strip()
        if not ip:
            continue
        
        latency = ping_ip(ip)
        print(f"  {ip}: {latency:.2f}ms")
        
        if latency < min_latency:
            min_latency = latency
            fastest_ip = ip
        
        sleep(0.3)
    
    if fastest_ip:
        print(f"  → 最快IP: {fastest_ip} ({min_latency:.2f}ms)")
    
    return fastest_ip

def main():
    print("=== 开始检测 TMDB 相关域名的最快 IP ===\n")
    
    # 日本DNS服务器
    japan_dns = ["202.248.37.74", "202.248.20.133"]
    
    ipv4_results, ipv6_results = [], []

    for domain in DOMAINS:
        print(f"\n{'='*60}")
        print(f"处理域名: {domain}")
        print(f"{'='*60}")
        
        # 获取 IPv4
        ipv4_ips = get_domain_ips(domain, "A", japan_dns)
        if ipv4_ips:
            fastest_ipv4 = find_fastest_ip(ipv4_ips)
            if fastest_ipv4:
                ipv4_results.append([fastest_ipv4, domain])
            else:
                ipv4_results.append([ipv4_ips[0], domain])
        
        # 获取 IPv6
        ipv6_ips = get_domain_ips(domain, "AAAA", japan_dns)
        if ipv6_ips:
            fastest_ipv6 = find_fastest_ip(ipv6_ips)
            if fastest_ipv6:
                ipv6_results.append([fastest_ipv6, domain])
            else:
                ipv6_results.append([ipv6_ips[0], domain])
        
        sleep(1)
    
    # 检查结果
    if not ipv4_results and not ipv6_results:
        print("\n❌ 程序出错：未获取任何 domain 及对应 IP")
        print("可能原因:")
        print("1. dnschecked.com API 已失效或更改")
        print("2. 网络连接问题")
        print("3. DNS 服务器无响应")
        print("\n建议: 检查网络连接或尝试其他 DNS 服务器")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"汇总: 成功获取 {len(ipv4_results)} 个 IPv4, {len(ipv6_results)} 个 IPv6")
    print(f"{'='*60}")

    # 生成更新时间
    update_time = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
    
    ipv4_hosts_content = Tmdb_Host_TEMPLATE.format(
        content="\n".join(f"{ip:<27} {domain}" for ip, domain in ipv4_results), 
        update_time=update_time
    ) if ipv4_results else ""
    
    ipv6_hosts_content = Tmdb_Host_TEMPLATE.format(
        content="\n".join(f"{ip:<50} {domain}" for ip, domain in ipv6_results), 
        update_time=update_time
    ) if ipv6_results else ""

    write_file(ipv4_hosts_content, ipv6_hosts_content, update_time)
    
    print("\n✓ 完成！")

if __name__ == "__main__":
    main()
