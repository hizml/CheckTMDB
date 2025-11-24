#!/usr/bin/env python3
"""
测试 dnschecked.com API 是否可用
"""
import requests
import json

def test_dnschecked_api():
    """测试 dnschecked API"""
    print("=== 测试 dnschecked.com API ===\n")
    
    url = 'https://api.dnschecked.com/query_dns'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "origin": "https://dnschecked.com",
        "referer": "https://dnschecked.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 测试用的参数
    test_cases = [
        {
            "domain": "tmdb.org",
            "record_type": "A",
            "dns_server": "202.248.37.74"  # 日本 DNS
        },
        {
            "domain": "tmdb.org",
            "record_type": "A",
            "dns_server": "8.8.8.8"  # Google DNS
        }
    ]
    
    for i, params in enumerate(test_cases, 1):
        print(f"\n--- 测试 {i}: {params['domain']} ({params['record_type']}) via {params['dns_server']} ---")
        try:
            response = requests.post(url, headers=headers, json=params, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            print(f"响应内容: {response.text[:500]}")  # 只显示前500字符
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"JSON 数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                except:
                    print("⚠️  无法解析为 JSON")
            else:
                print(f"❌ 请求失败")
                
        except Exception as e:
            print(f"❌ 发生错误: {e}")
        
        print("-" * 60)

def test_alternative_method():
    """测试备用方法 - 直接使用 DNS 查询"""
    print("\n\n=== 测试备用方案: 使用 socket.getaddrinfo ===\n")
    import socket
    
    test_domains = ["tmdb.org", "api.tmdb.org", "themoviedb.org"]
    
    for domain in test_domains:
        try:
            print(f"\n查询 {domain}:")
            # IPv4
            try:
                ipv4_results = socket.getaddrinfo(domain, None, socket.AF_INET)
                ipv4_ips = list(set([x[4][0] for x in ipv4_results]))
                print(f"  IPv4: {ipv4_ips}")
            except Exception as e:
                print(f"  IPv4 查询失败: {e}")
            
            # IPv6
            try:
                ipv6_results = socket.getaddrinfo(domain, None, socket.AF_INET6)
                ipv6_ips = list(set([x[4][0] for x in ipv6_results]))
                print(f"  IPv6: {ipv6_ips}")
            except Exception as e:
                print(f"  IPv6 查询失败: {e}")
                
        except Exception as e:
            print(f"  整体查询失败: {e}")

if __name__ == "__main__":
    test_dnschecked_api()
    test_alternative_method()
