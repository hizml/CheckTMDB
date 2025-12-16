# CheckTMDB

每日自动更新TMDB、IMDb、TheTVDB 等影视数据库域名在国内可正常连接的 IP 地址，解决 DNS 污染问题，为 tinyMediaManager、Plex、Emby、Jellyfin 等影视削刮器提供可用的 hosts 配置。

## 一、项目概述

CheckTMDB 自动检测和更新 TMDB、IMDb、TheTVDB 等影视数据库域名的最佳 IP 地址。主要解决 DNS 污染导致的访问问题，确保各种影视削刮器能够正常获取影片信息和海报数据。

**本项目无需安装任何程序**，通过修改本地或路由器的 hosts 文件即可使用。

### 核心特性

- **多种解析方式**: 支持系统 DNS 解析和 Cloudflare DoH 备用解析
- **延迟测试**: 自动测试每个 IP 的连接延迟，选择最快的地址
- **自动化更新**: 通过 GitHub Actions 每日自动更新
- **多域名支持**: 涵盖 TMDB、IMDb、TheTVDB 等主流影视数据库
- **IPv4/IPv6 双栈**: 同时提供 IPv4 和 IPv6 地址支持

## 二、获取 hosts 文件

### 2.1 直接下载地址

- TMDB IPv4 hosts：`https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv4` ，[链接](https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv4)
- TMDB IPv6 hosts：`https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv6` ，[链接](https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv6)

### 2.2 脚本说明

项目提供两种主要的检测脚本：

1. **check_tmdb_dns.py**（推荐）
   - 使用系统 DNS 解析
   - 无需外部依赖，仅使用 Python 标准库
   - 最稳定可靠，适合大多数使用场景

2. **check_tmdb_doh.py**（备用方案）
   - 优先使用系统 DNS，失败时自动切换 Cloudflare DoH
   - 需要 requests 库
   - 适合网络环境复杂的情况

3. **deprecated/**（已弃用）
   - 包含旧的 API 方式脚本，已失效不建议使用

- TMDB IPv4 hosts：`https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv4` ，[链接](https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv4)
- TMDB IPv6 hosts：`https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv6` ，[链接](https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv6)

## 三、使用方法

### 3.1 手动方式

#### 3.1.1 IPv4地址复制下面的内容

```bash
# Tmdb Hosts Start
18.155.192.38               tmdb.org
18.238.192.90               api.tmdb.org
13.249.74.90                files.tmdb.org
18.155.202.127              themoviedb.org
18.244.214.44               api.themoviedb.org
18.155.202.61               www.themoviedb.org
18.155.192.128              auth.themoviedb.org
169.150.249.163             image.tmdb.org
143.244.49.178              images.tmdb.org
98.82.155.134               imdb.com
18.155.187.37               www.imdb.com
44.215.137.99               secure.imdb.com
18.155.187.37               s.media-imdb.com
98.82.155.134               us.dd.imdb.com
18.155.187.37               www.imdb.to
98.82.155.134               origin-www.imdb.com
151.101.201.16              ia.media-imdb.com
13.249.76.81                thetvdb.com
108.139.0.92                api.thetvdb.com
151.101.201.16              f.media-amazon.com
18.238.192.103              imdb-video.media-imdb.com
# Update time: 2025-12-17T06:12:22+08:00
# IPv4 Update url: https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/hizml/CheckTMDB
# Tmdb Hosts End

```

该内容会自动定时更新， 数据更新时间：2025-12-17T06:12:22+08:00

#### 3.1.2 IPv6地址复制下面的内容

```bash
# Tmdb Hosts Start
2600:9000:24bb:b800:10:db24:6940:93a1              tmdb.org
2600:9000:25f1:bc00:10:fb02:4000:93a1              api.tmdb.org
2600:9000:211f:9200:5:da10:7440:93a1               files.tmdb.org
2600:9000:24bc:7c00:e:5373:440:93a1                themoviedb.org
2600:9000:25f0:5200:c:174a:c400:93a1               api.themoviedb.org
2600:9000:24bc:5c00:e:5373:440:93a1                www.themoviedb.org
2600:9000:24bb:6200:16:e4a1:eb00:93a1              auth.themoviedb.org
2400:52e0:1a01::1114:1                             image.tmdb.org
2400:52e0:1a01::1114:1                             images.tmdb.org
tp.391b988c0-frontier.imdb.com.                    www.imdb.com
tp.391b988c0-frontier.imdb.com.                    s.media-imdb.com
d2bytcopxu066p.cloudfront.net.                     www.imdb.to
2a04:4e42:2f::272                                  ia.media-imdb.com
2a04:4e42:2f::272                                  f.media-amazon.com
d22ohr3ltkx6p.cloudfront.net.                      imdb-video.media-imdb.com
# Update time: 2025-12-17T06:12:22+08:00
# IPv4 Update url: https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv4
# IPv6 Update url: https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv6
# Star me: https://github.com/hizml/CheckTMDB
# Tmdb Hosts End

```

该内容会自动定时更新， 数据更新时间：2025-12-17T06:12:22+08:00

> [!NOTE]
> 由于项目搭建在Github Aciton，延时数据获取于Github Action 虚拟主机网络环境，请自行测试可用性，建议使用本地网络环境自动设置。

#### 3.1.3 修改 hosts 文件

hosts 文件在每个系统的位置不一，详情如下：

- Windows 系统：`C:\Windows\System32\drivers\etc\hosts`
- Linux 系统：`/etc/hosts`
- Mac（苹果电脑）系统：`/etc/hosts`
- Android（安卓）系统：`/system/etc/hosts`
- iPhone（iOS）系统：`/etc/hosts`

修改方法，把第一步的内容复制到文本末尾：

1. Windows 使用记事本。
2. Linux、Mac 使用 Root 权限：`sudo vi /etc/hosts`。
3. iPhone、iPad 须越狱、Android 必须要 root。

#### 3.1.4 激活生效

大部分情况下是直接生效，如未生效可尝试下面的办法，刷新 DNS：

1. Windows：在 CMD 窗口输入：`ipconfig /flushdns`

2. Linux 命令：`sudo nscd restart`，如报错则须安装：`sudo apt install nscd` 或 `sudo /etc/init.d/nscd restart`

3. Mac 命令：`sudo killall -HUP mDNSResponder`

**Tips：** 上述方法无效可以尝试重启机器。

### 3.2 自动方式

#### 3.2.1 安装 SwitchHosts

GitHub 发行版：https://github.com/oldj/SwitchHosts/releases/latest

#### 3.2.2 添加 hosts

点击左上角“+”，并进行以下配置：

- Hosts 类型：`远程`
- Hosts 标题：任意
- URL
    - IPv4：`https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv4`
    - IPv6：`https://raw.githubusercontent.com/hizml/CheckTMDB/refs/heads/main/Tmdb_host_ipv6`
- 自动刷新：`1 小时`

#### 3.2.3 启用 hosts

在左侧边栏启用 hosts，首次使用时软件会自动获取内容。如果无法连接到 GitHub，可以尝试用同样的方法添加 [GitHub520](https://github.com/521xueweihan/GitHub520) hosts。

## 四、脚本使用说明

### 4.1 本地运行

**推荐方式 - check_tmdb_dns.py（无需依赖）**
```bash
python3 check_tmdb_dns.py
```

**备用方式 - check_tmdb_doh.py（需要安装依赖）**
```bash
# 安装依赖
pip install -r requirements.txt

# 运行脚本
python3 check_tmdb_doh.py
```

### 4.2 支持的域名列表

脚本会自动检测以下域名的最佳 IP：

**TMDB 相关**：
- tmdb.org
- api.tmdb.org
- files.tmdb.org
- themoviedb.org
- api.themoviedb.org
- www.themoviedb.org
- auth.themoviedb.org
- image.tmdb.org
- images.tmdb.org

**IMDb 相关**：
- imdb.com
- www.imdb.com
- secure.imdb.com
- s.media-imdb.com
- us.dd.imdb.com
- www.imdb.to
- origin-www.imdb.com
- ia.media-imdb.com

**TheTVDB 相关**：
- thetvdb.com
- api.thetvdb.com

**Amazon 相关**：
- f.media-amazon.com
- imdb-video.media-imdb.com

### 4.3 自动化部署

项目使用 GitHub Actions 进行自动化更新，每天 10:00 和 22:00 (UTC+8) 自动执行更新。如需修改更新频率，可编辑 `.github/workflows/main.yml` 文件中的 cron 表达式。

## 五、常见问题

### 5.1 如何验证 hosts 是否生效？

可以通过以下命令验证：
```bash
# Windows
ping tmdb.org

# Linux/Mac
ping -c 4 tmdb.org
```

如果返回的 IP 地址与 hosts 文件中的地址一致，说明配置已生效。

### 5.2 更新后仍然无法访问？

可能的原因及解决方案：
1. **DNS 缓存**：尝试清除 DNS 缓存（见激活生效部分）
2. **浏览器缓存**：清除浏览器缓存或使用无痕模式
3. **防火墙/安全软件**：检查是否被防火墙或安全软件拦截
4. **代理设置**：检查系统代理设置是否影响 hosts 生效

### 5.3 如何回退到原始状态？

删除 hosts 文件中添加的相关内容即可，或恢复原始 hosts 文件。

## 六、项目贡献

### 6.1 技术实现

- **DNS 解析**: 使用 Python 标准库 `socket.getaddrinfo` 进行系统 DNS 解析
- **DoH 备用**: Cloudflare DNS-over-HTTPS 作为备用解析方案
- **延迟测试**: TCP 连接测试选择最优 IP
- **自动化**: GitHub Actions 定时执行更新

### 6.2 致谢

- [x] Fork 自 [CheckTMDB](https://github.com/cnwikee/CheckTMDB)，感谢原作者 [cnwikee](https://github.com/cnwikee) 的贡献
- [x] README 格式参考 [GitHub520](https://github.com/521xueweihan/GitHub520) 项目
- [x] 使用 Cloudflare DNS-over-HTTPS API 作为备用解析方案
- [x] 本项目已在本机及 GitHub Actions 环境测试通过

### 6.3 问题反馈

如有问题欢迎提 [issues](https://github.com/hizml/CheckTMDB/issues/new) 或提交 pull request。

### 6.4 免责声明

本项目仅供学习和研究使用，请遵守相关法律法规。使用本项目产生的任何后果由使用者自行承担。
