# -*- coding: utf-8 -*-
"""内容净化与敏感词处理（教育导向、防御视角）"""

# 替换为教育/防御性表述
REPLACEMENTS = {
    "渗透": "授权安全评估",
    "漏洞挖掘": "安全缺陷分析",
    "漏洞利用": "风险验证",
    "攻击": "威胁",
    "黑客": "安全研究人员",
    "入侵": "未授权访问",
    "爆破": "暴力尝试",
    "木马": "恶意程序",
    "后门": "隐蔽通道",
    "钓鱼": "社会工程学欺骗",
    "逆向工程": "软件逆向分析",
    "破解": "分析研究",
    "脱壳": "保护层分析",
    "提权": "权限提升风险",
    "缓冲区溢出": "内存越界问题",
    "SQL注入": "SQL 注入风险",
    "XSS": "跨站脚本风险",
    "CSRF": "跨站请求伪造风险",
}

# 安全类领域使用防御视角前缀
DEFENSIVE_DOMAINS = {
    "渗透测试", "漏洞挖掘", "逆向工程", "Web安全", "网络安全",
    "移动安全", "云安全", "密码学",
}


def sanitize_text(text: str, domain: str = "") -> str:
    """净化文本，确保教育导向"""
    if not text:
        return text
    result = text
    for old, new in REPLACEMENTS.items():
        result = result.replace(old, new)
    return result


def defensive_note(domain: str) -> str:
    """安全类领域附加教育声明"""
    if domain in DEFENSIVE_DOMAINS:
        return (
            "> **学习声明**：本章内容仅供合法授权环境下的安全研究与防御建设，"
            "请遵守法律法规与组织安全政策，禁止对未授权系统开展测试。\n"
        )
    return ""
