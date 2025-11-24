#!/usr/bin/env python3
"""
简化版本：直接使用系统 DNS 解析，不依赖任何第三方 API
适用于无法访问 dnschecker.org 和 dnschecked.com 的情况
"""
import socket
import time
import os
import sys
from datetime import datetime, timezone, timedelta
from time import sleep

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
# IPv4 Update url: https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/hizml/CheckTMDB
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
                        print("IPv4 hosts 未变化")
                        w_ipv4_block = old_ipv4_block
                    else:
                        w_ipv4_block = ipv4_hosts_content
                        write_host_file(ipv4_hosts_content, 'ipv4')
                else:
                    print("IPv4 内容为空，保留旧内容")
                    w_ipv4_block = old_ipv4_block

                if ipv6_hosts_content != "":
                    new_ipv6_hosts = ipv6_hosts_content.split("# Update time:")[0].strip()
                    if old_ipv6_hosts == new_ipv6_hosts:
                        print("IPv6 hosts 未变化")
                        w_ipv6_block = old_ipv6_block
                    else:
                        w_ipv6_block = ipv6_hosts_content
                        write_host_file(ipv6_hosts_content, 'ipv6')
                else:
                    print("IPv6 内容为空，保留旧内容")
                    w_ipv6_block = old_ipv6_block

                with open(template_path, "r", encoding='utf-8') as temp_fb:
                    template_str = temp_fb.read()
                    hosts_content = template_str.format(
                        ipv4_hosts_str=w_ipv4_block,
                        ipv6_hosts_str=w_ipv6_block,
                        update_time=update_time
                    )

                    with open(output_doc_file_path, "w", encoding='utf-8') as output_fb:
                        output_fb.write(hosts_content)
                return True
        return False

def write_host_file(hosts_content: str, filename: str) -> None:
    output_file_path = os.path.join(os.path.dirname(__file__), "Tmdb_host_" + filename)
    with open(output_file_path, "w", encoding='utf-8') as output_fb:
        output_fb.write(hosts_content)
        print(f"\n✓ Tmdb_host_{filename} 已更新")

def get_domain_ips(domain, ip_version='ipv4'):
    """
    使用系统 DNS 解析获取域名的 IP 地址

    Args:
        domain: 域名
        ip_version: 'ipv4' 或 'ipv6'

    Returns:
        IP 地址列表
    """
    ips = []

    try:
        if ip_version == 'ipv4':
            # 获取 IPv4 地址
            results = socket.getaddrinfo(domain, None, socket.AF_INET)
            ips = list(set([x[4][0] for x in results]))
        elif ip_version == 'ipv6':
            # 获取 IPv6 地址
            try:
                results = socket.getaddrinfo(domain, None, socket.AF_INET6)
                ips = list(set([x[4][0] for x in results]))
            except socket.gaierror:
                # 某些域名可能没有 IPv6 地址
                pass

        if ips:
            print(f"  ✓ {domain} ({ip_version}): {ips}")
        else:
            print(f"  ✗ {domain} ({ip_version}): 无法解析")

    except socket.gaierror as e:
        print(f"  ✗ {domain} ({ip_version}): DNS 解析失败 - {e}")
    except Exception as e:
        print(f"  ✗ {domain} ({ip_version}): 错误 - {e}")

    return ips

def ping_ip(ip, port=80, timeout=2):
    """
    使用 TCP 连接测试 IP 延迟

    Args:
        ip: IP 地址
        port: 端口（默认 80）
        timeout: 超时时间（秒）

    Returns:
        延迟（毫秒）或 float('inf')
    """
    try:
        start_time = time.time()
        sock = socket.socket(socket.AF_INET if ':' not in ip else socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.close()
        latency = (time.time() - start_time) * 1000
        return latency
    except Exception as e:
        return float('inf')

def find_fastest_ip(ips):
    """
    从 IP 列表中找出延迟最低的 IP

    Args:
        ips: IP 地址列表

    Returns:
        延迟最低的 IP 地址
    """
    if not ips:
        return None

    # 如果只有一个 IP，直接返回
    if len(ips) == 1:
        return ips[0]

    fastest_ip = None
    min_latency = float('inf')

    print(f"    测试 {len(ips)} 个IP的延迟...")

    for ip in ips:
        ip = ip.strip()
        if not ip:
            continue

        latency = ping_ip(ip)

        if latency < min_latency:
            min_latency = latency
            fastest_ip = ip

        if latency == float('inf'):
            print(f"      {ip}: 超时")
        else:
            print(f"      {ip}: {latency:.2f}ms")

        sleep(0.2)

    if fastest_ip and min_latency != float('inf'):
        print(f"    → 最快: {fastest_ip} ({min_latency:.2f}ms)")

    return fastest_ip

def main():
    print("="*60)
    print("开始检测 TMDB 相关域名的 IP 地址")
    print("方法: 系统 DNS 解析 + TCP 延迟测试")
    print("="*60)

    ipv4_results = []
    ipv6_results = []

    total_domains = len(DOMAINS)

    for idx, domain in enumerate(DOMAINS, 1):
        print(f"\n[{idx}/{total_domains}] 正在处理: {domain}")

        # 获取 IPv4 地址
        ipv4_ips = get_domain_ips(domain, 'ipv4')
        if ipv4_ips:
            if len(ipv4_ips) > 1:
                fastest_ipv4 = find_fastest_ip(ipv4_ips)
            else:
                fastest_ipv4 = ipv4_ips[0]

            if fastest_ipv4:
                ipv4_results.append([fastest_ipv4, domain])

        # 获取 IPv6 地址
        ipv6_ips = get_domain_ips(domain, 'ipv6')
        if ipv6_ips:
            if len(ipv6_ips) > 1:
                fastest_ipv6 = find_fastest_ip(ipv6_ips)
            else:
                fastest_ipv6 = ipv6_ips[0]

            if fastest_ipv6:
                ipv6_results.append([fastest_ipv6, domain])

        # 避免请求过快
        if idx < total_domains:
            sleep(0.5)

    print("\n" + "="*60)
    print(f"检测完成！")
    print(f"成功获取 {len(ipv4_results)} 个 IPv4 地址")
    print(f"成功获取 {len(ipv6_results)} 个 IPv6 地址")
    print("="*60)

    # 检查是否有结果
    if not ipv4_results and not ipv6_results:
        print("\n❌ 错误: 未能获取任何 IP 地址")
        print("可能原因:")
        print("1. 网络连接问题")
        print("2. DNS 服务器无响应")
        print("3. 系统 DNS 配置问题")
        sys.exit(1)

    # 生成更新时间
    update_time = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

    # 生成 hosts 内容
    ipv4_hosts_content = Tmdb_Host_TEMPLATE.format(
        content="\n".join(f"{ip:<27} {domain}" for ip, domain in ipv4_results),
        update_time=update_time
    ) if ipv4_results else ""

    ipv6_hosts_content = Tmdb_Host_TEMPLATE.format(
        content="\n".join(f"{ip:<50} {domain}" for ip, domain in ipv6_results),
        update_time=update_time
    ) if ipv6_results else ""

    # 写入文件
    write_file(ipv4_hosts_content, ipv6_hosts_content, update_time)

    print("\n✓ 所有文件已更新完成！")

if __name__ == "__main__":
    main()
