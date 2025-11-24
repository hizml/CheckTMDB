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
# 使用 dnschecker.org API 方式(推荐)
python check_tmdb_github.py

# 使用指定 DNS 服务器查询方式
python check_tmdb_github_dnschecked.py

# 附加 GitHub hosts(添加 -G 参数)
python check_tmdb_github.py -G
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

- **check_tmdb_github.py**: 主脚本,通过 dnschecker.org API 查询域名 IP
  - 获取 CSRF token 和动态 udp 参数
  - 支持 IPv4 (A记录) 和 IPv6 (AAAA记录) 查询
  - 使用 TCP socket 连接测试 IP 延迟
  - 可选附加 GitHub hosts (-G 参数)

- **check_tmdb_github_dnschecked.py**: 备用脚本,通过韩国/日本 DNS 服务器查询
  - 使用 `dns.resolver` 进行 DNS 查询
  - 逻辑与主脚本基本一致

- **README_template.md**: README 模板文件
  - 包含占位符: `{ipv4_hosts_str}`, `{ipv6_hosts_str}`, `{update_time}`
  - 脚本会用实际数据填充并生成 README.md

- **Tmdb_host_ipv4**: IPv4 hosts 输出文件
- **Tmdb_host_ipv6**: IPv6 hosts 输出文件

### 工作流程

1. **获取域名列表**: 从 `DOMAINS` 常量读取需要查询的域名
2. **查询 IP 地址**: 
   - `check_tmdb_github.py`: 调用 dnschecker.org API
   - `check_tmdb_github_dnschecked.py`: 使用 DNS 解析器
3. **测试延迟**: 使用 `ping_ip()` 通过 TCP 连接测试每个 IP 的延迟
4. **选择最快 IP**: `find_fastest_ip()` 返回延迟最低的 IP
5. **生成 hosts 内容**: 格式化为 hosts 文件格式
6. **更新文件**: 
   - 对比旧内容,仅在有变化时更新
   - 更新 `Tmdb_host_ipv4` / `Tmdb_host_ipv6`
   - 基于模板更新 `README.md`

### GitHub Actions 自动化

- **触发时机**: 
  - 每天 10:00 和 22:00 (UTC) 定时执行
  - 手动触发 (workflow_dispatch)
- **执行流程**:
  1. 检出代码
  2. 设置 Python 3.10 环境
  3. 安装依赖 (`requirements.txt`)
  4. 运行 `check_tmdb_github_dnschecked.py`
  5. 提交并推送更新后的文件 (README.md, Tmdb_host_ipv4, Tmdb_host_ipv6)

### 关键配置变量

- **country_code** (`check_tmdb_github.py`): 
  - 当前设置为 `'jp'` (日本节点)
  - 控制从哪个国家/地区获取 IP

- **dns_server** (`check_tmdb_github_dnschecked.py`):
  - 韩国 DNS: `["202.46.34.75", "168.126.63.1"]`
  - 日本 DNS: `["202.248.37.74", "202.248.20.133"]`

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
