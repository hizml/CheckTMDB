# CODEBUDDY.md

This file provides guidance to CodeBuddy Code when working with code in this repository.

## 项目概述

CheckTMDB 是一个自动检测和更新 TMDB、IMDb、TheTVDB 等影视数据库域名最佳 IP 地址的工具。主要解决 DNS 污染导致的访问问题,为影视削刮器(如 TinyMediaManager、Plex、Emby、Jellyfin 等)提供可用的 hosts 配置。

## 常用命令

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行脚本
```bash
# 使用系统 DNS 方式（推荐，最稳定）
python3 check_tmdb_dns.py

# 使用系统 DNS + Cloudflare DoH 备用方式（成功率更高）
python3 check_tmdb_doh.py
```

### 手动测试
```bash
# 直接运行主脚本
python check_tmdb_github.py

# 测试单个域名的延迟
# 脚本内部使用 TCP 连接测试,不支持独立测试
```

## 核心架构

### 主要文件说明

- **check_tmdb_dns.py**: 系统 DNS 方式（推荐）
  - 使用 `socket.getaddrinfo()` 进行系统 DNS 查询
  - 无外部依赖，只使用 Python 标准库
  - 最稳定可靠，不受第三方 API 影响
  - 适合大多数使用场景

- **check_tmdb_doh.py**: 系统 DNS + Cloudflare DoH 备用
  - 优先使用系统 DNS 解析
  - 失败时自动切换到 Cloudflare DNS-over-HTTPS
  - 提高成功率，适合网络环境复杂的情况
  - 需要 requests 库

- **deprecated/**: 已弃用的脚本
  - check_tmdb_github.py: 使用 dnschecker.org API（已失效，403错误）
  - check_tmdb_github_dnschecked.py: 使用 dnschecked.com API（已失效）

- **README_template.md**: README 模板文件
  - 包含占位符: `{ipv4_hosts_str}`, `{ipv6_hosts_str}`, `{update_time}`
  - 脚本会用实际数据填充并生成 README.md

- **Tmdb_host_ipv4**: IPv4 hosts 输出文件
- **Tmdb_host_ipv6**: IPv6 hosts 输出文件

### 工作流程

**check_tmdb_dns.py (系统 DNS 方式):**

1. **获取域名列表**: 从 `DOMAINS` 常量读取需要查询的域名
2. **查询 IP 地址**: 使用 `socket.getaddrinfo()` 进行系统 DNS 查询
3. **测试延迟**: 使用 `ping_ip()` 通过 TCP 连接测试每个 IP 的延迟
4. **选择最快 IP**: `find_fastest_ip()` 返回延迟最低的 IP
5. **生成 hosts 内容**: 格式化为 hosts 文件格式
6. **更新文件**: 更新 `Tmdb_host_ipv4` / `Tmdb_host_ipv6` 和 `README.md`

**check_tmdb_doh.py (系统 DNS + DoH 备用):**

1. **获取域名列表**: 从 `DOMAINS` 常量读取需要查询的域名
2. **查询 IP 地址**: 
   - 方法1: 使用 `socket.getaddrinfo()` 进行系统 DNS 查询
   - 方法2: 如果方法1失败，使用 Cloudflare DNS-over-HTTPS
3. **测试延迟**: 使用 `ping_ip()` 通过 TCP 连接测试每个 IP 的延迟
4. **选择最快 IP**: `find_fastest_ip()` 返回延迟最低的 IP
5. **生成 hosts 内容**: 格式化为 hosts 文件格式
6. **更新文件**: 更新 `Tmdb_host_ipv4` / `Tmdb_host_ipv6` 和 `README.md`

### GitHub Actions 自动化

- **触发时机**: 
  - 每天 10:00 和 22:00 (UTC) 定时执行
  - 手动触发 (workflow_dispatch)
- **执行流程**:
  1. 检出代码
  2. 设置 Python 3.10 环境
  3. 安装依赖 (`requirements.txt`)
  4. 运行脚本（建议使用 `check_tmdb_dns.py` 或 `check_tmdb_doh.py`）
  5. 提交并推送更新后的文件 (README.md, Tmdb_host_ipv4, Tmdb_host_ipv6)

**注意**: 原 workflow 使用的 `check_tmdb_github_dnschecked.py` 已失效，建议改用 `check_tmdb_dns.py` 或 `check_tmdb_doh.py`

### 关键配置变量

- **DOMAINS**: 需要查询的域名列表
  - TMDB: tmdb.org, api.tmdb.org, themoviedb.org 等
  - IMDb: imdb.com, www.imdb.com 等
  - TheTVDB: thetvdb.com, api.thetvdb.com

### 延迟测试机制

- 使用 TCP socket 连接测试 (非 ICMP ping)
- 端口: 80 (HTTP)
- 超时时间: 2 秒
- 返回值: 毫秒 (ms) 或 `float('inf')` (失败)

### 错误处理

- 使用 `@retry(tries=3)` 装饰器重试网络请求
- 获取 IP 失败时跳过该域名
- 所有域名都失败时,程序以错误码退出
- 内容未变化时不会重复写入文件

## 注意事项

- 修改 `country_code` 会影响获取到的 IP 地址质量
- `-G` 参数会从多个源获取 GitHub hosts 并附加到输出文件
- GitHub Actions 使用 `check_tmdb_github_dnschecked.py` 而非主脚本
- 所有时间戳使用东八区时区 (UTC+8)
