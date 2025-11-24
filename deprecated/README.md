# 已弃用的脚本 (Deprecated Scripts)

本文件夹包含由于第三方 API 失效而无法正常工作的脚本。

## 文件列表

### 1. check_tmdb_github.py
**状态**: ❌ 已失效  
**失效原因**: dnschecker.org 返回 403 Forbidden，网站加强了反爬虫措施  
**错误信息**: `获取CSRF Token失败，HTTP状态码: 403`  
**依赖**: 
- requests
- retry
- pythonping
- ping3

**原理**:
- 通过 dnschecker.org 的 API 获取指定国家/地区（如日本）的 DNS 查询结果
- 需要先获取 CSRF Token 才能进行查询
- 使用 TCP ping 测试延迟并选择最快的 IP

**失效时间**: 约 2025 年 11 月（具体时间未知）

---

### 2. check_tmdb_github_dnschecked.py
**状态**: ❌ 已失效  
**失效原因**: api.dnschecked.com API 失效或返回空结果  
**错误信息**: `程序出错：未获取任何domain及对应IP，请检查接口~`  
**依赖**: 
- requests
- retry
- pythonping
- ping3

**原理**:
- 通过 api.dnschecked.com 的 API 查询指定 DNS 服务器的解析结果
- 使用韩国或日本的 DNS 服务器进行查询
- 使用 TCP ping 测试延迟并选择最快的 IP

**失效时间**: 约 2025 年 11 月（具体时间未知）

---

## 替代方案

请使用以下脚本替代：

### 推荐方案（按优先级）:

1. **check_tmdb_simple.py** ⭐⭐⭐⭐⭐
   - 最稳定，只使用系统 DNS 解析
   - 无外部依赖，不会因 API 失效而无法使用
   - 适合 99% 的使用场景

2. **check_tmdb_fixed.py** ⭐⭐⭐⭐
   - 三重备用机制（dnschecked API → 系统 DNS → Cloudflare DoH）
   - 更高的成功率和 IP 质量
   - 依赖 requests 库

## 为什么保留这些文件？

1. **历史参考**: 了解项目的演进过程
2. **代码复用**: 其中的延迟测试、文件写入等逻辑可以参考
3. **学习价值**: 展示了如何与第三方 API 交互（虽然现在失效了）

## 如果想修复这些脚本

### check_tmdb_github.py 的修复思路:
1. 使用无头浏览器（Selenium/Playwright）模拟真实浏览器
2. 添加 Cookie 管理和 JavaScript 执行
3. 使用代理池避免 IP 被封
4. **不推荐**: 成本高，维护难度大，不如直接用系统 DNS

### check_tmdb_github_dnschecked.py 的修复思路:
1. 检查 API 是否有新的端点或参数格式
2. 联系 dnschecked.com 获取官方 API 文档
3. 使用其他类似服务（如 DNS.SB、AdGuard DNS）
4. **不推荐**: API 服务不稳定，随时可能再次失效

## 最佳实践

⚠️ **重要提示**: 不要依赖第三方免费 API 作为唯一方案

建议的架构:
1. **主方案**: 使用稳定的本地方法（系统 DNS）
2. **备用方案**: 使用知名的公共服务（Cloudflare DoH、Google DoH）
3. **最后方案**: 第三方小众 API（容易失效）

---

*最后更新: 2025-11-24*
