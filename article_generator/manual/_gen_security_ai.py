#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate content_security_ai.py with complete Chinese tutorial content."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from domains_100_config import DOMAINS_CONFIG

OUTPUT = Path(__file__).parent / "content_security_ai.py"

TARGET_DOMAINS = [
    "网络安全", "Web安全", "密码学", "渗透测试", "逆向工程", "漏洞挖掘", "移动安全", "云安全",
    "数据结构与算法", "机器学习", "深度学习", "自然语言处理", "计算机视觉", "强化学习",
    "数据挖掘", "知识图谱", "大语言模型", "AIGC",
    "区块链", "游戏开发", "计算机图形学", "音视频处理", "物联网", "低代码开发", "量子计算",
    "Rust系统编程",
]

SECURITY_NOTE = (
    "本教程内容仅供合法授权的安全测试、防御加固与学术研究使用。"
    "未经授权对他人系统进行扫描、入侵或破坏属于违法行为。"
)

# ---------------------------------------------------------------------------
# Domain overviews
# ---------------------------------------------------------------------------

DOMAIN_OVERVIEWS_RAW: dict[str, dict] = {
    "网络安全": {
        "intro": (
            "网络安全是保障信息系统在存储、传输与处理过程中机密性、完整性与可用性的综合学科。"
            "它横跨网络协议、边界防护、入侵检测、安全审计与应急响应，"
            "是 DevSecOps 与零信任架构的理论与实践基础。"
        ),
        "positioning": "面向安全工程师与网络运维人员，侧重防御体系设计与合规落地，而非攻击技巧。",
        "prerequisites": ["计算机网络", "TCP/IP 协议", "Linux 基础", "防火墙基本概念"],
        "outcomes": [
            "理解 OSI/TCP-IP 各层常见威胁与对应防御手段",
            "能设计分层网络防御架构并配置防火墙与 IDS/IPS",
            "掌握 VPN、网络隔离与 DDoS 缓解的基本策略",
            "能在授权范围内开展安全审计与应急响应",
        ],
        "ecosystem": "iptables/nftables, Snort/Suricata, Wireshark, Zeek, pfSense, Cisco ASA",
    },
    "Web安全": {
        "intro": (
            "Web 安全聚焦浏览器、HTTP 协议与应用层逻辑的安全风险。"
            "OWASP Top 10 列出了注入、失效的访问控制、安全配置错误等高频问题，"
            "现代防御需结合输入校验、安全编码、WAF 与安全响应头。"
        ),
        "positioning": "面向 Web 开发者与安全工程师，从防御视角讲解常见漏洞原理与加固方案。",
        "prerequisites": ["HTTP/HTTPS", "HTML/CSS/JavaScript", "后端框架基础", "数据库基础"],
        "outcomes": [
            "识别并修复 XSS、CSRF、SQL 注入等 OWASP 高频漏洞",
            "设计安全的认证、会话与权限控制方案",
            "配置 CSP、HSTS 等安全响应头与 WAF 规则",
            "建立代码审计与安全测试流程（仅限授权环境）",
        ],
        "ecosystem": "OWASP, Burp Suite(防御测试), ModSecurity, CSP Evaluator, Semgrep",
    },
    "密码学": {
        "intro": (
            "密码学为数字世界提供机密性、完整性、认证与不可否认性。"
            "对称加密（AES）、非对称加密（RSA/ECC）、哈希（SHA-256）与数字签名构成 TLS、"
            "JWT、区块链等技术的数学基础。"
        ),
        "positioning": "面向开发者与安全工程师，侧重算法选型、协议理解与工程实现，非密码分析攻击。",
        "prerequisites": ["离散数学基础", "计算机网络", "编程基础"],
        "outcomes": [
            "正确选择对称/非对称算法与密钥长度",
            "理解 TLS 握手、证书链与 PKI 体系",
            "避免 MD5/SHA-1/DES 等已弃用算法",
            "安全实现随机数、密钥管理与数字签名",
        ],
        "ecosystem": "OpenSSL, libsodium, Bouncy Castle, Let's Encrypt, HashiCorp Vault",
    },
    "渗透测试": {
        "intro": (
            "渗透测试是在获得书面授权前提下，模拟攻击者评估系统安全性的方法论。"
            "PTES（Penetration Testing Execution Standard）定义了前期交互、情报收集、"
            "威胁建模、漏洞分析、漏洞验证、后渗透与报告编写七个阶段。"
            "本教程强调流程、范围界定与报告，不提供未授权攻击指导。"
        ),
        "positioning": "面向持证安全测试人员，聚焦 PTES 方法论、授权流程与专业报告编写。",
        "prerequisites": ["计算机网络", "Web 安全基础", "Linux 命令行", "安全法律法规"],
        "outcomes": [
            "制定渗透测试范围声明（SOW）与授权文件",
            "按 PTES 阶段规划测试活动与交付物",
            "使用扫描工具进行授权范围内的漏洞发现",
            "编写含风险评级与修复建议的专业报告",
        ],
        "ecosystem": "PTES, OWASP Testing Guide, Nmap, Nessus/OpenVAS, Burp Suite Pro",
    },
    "逆向工程": {
        "intro": (
            "逆向工程是通过分析二进制或固件理解程序行为的技术，"
            "合法用途包括恶意软件分析、漏洞研究与兼容性开发。"
            "本教程侧重 PE/ELF 结构、静态/动态分析与调试器使用，"
            "强调在授权样本与自有软件范围内开展研究。"
        ),
        "positioning": "面向安全研究员与恶意软件分析师，侧重分析方法论与防御洞察。",
        "prerequisites": ["汇编语言", "C/C++ 基础", "操作系统原理", "调试基础"],
        "outcomes": [
            "阅读 x86/x64 与 ARM 汇编理解控制流",
            "使用 IDA Pro/Ghidra 进行静态分析",
            "配置调试器进行动态行为观察",
            "识别常见混淆与加壳并制定分析策略",
        ],
        "ecosystem": "Ghidra, IDA Pro, x64dbg, radare2, Binary Ninja, PE-bear",
    },
    "漏洞挖掘": {
        "intro": (
            "漏洞挖掘是系统性地发现软件缺陷的过程，涵盖 Fuzzing、代码审计与二进制分析。"
            "发现漏洞后应遵循负责任披露流程，向厂商报告并等待修复后再公开。"
            "本教程侧重挖掘方法论与报告，不提供武器化利用代码。"
        ),
        "positioning": "面向安全研究员，聚焦漏洞分类、Fuzzing 与代码审计方法论。",
        "prerequisites": ["C/C++ 编程", "操作系统", "调试器使用", "安全基础"],
        "outcomes": [
            "理解 CVE/CWE 分类体系与 CVSS 评分",
            "使用 Fuzzing 框架发现内存与逻辑缺陷",
            "开展白盒代码审计并记录发现",
            "编写符合负责任披露规范的漏洞报告",
        ],
        "ecosystem": "AFL++, libFuzzer, CodeQL, Coverity, CVE, MITRE CWE",
    },
    "移动安全": {
        "intro": (
            "移动安全涵盖 Android 与 iOS 平台的应用安全、数据保护与通信安全。"
            "Android 基于 Linux 与 ART 虚拟机，iOS 基于沙箱与代码签名。"
            "防御重点包括权限最小化、安全存储、证书锁定与代码混淆。"
        ),
        "positioning": "面向移动开发者与安全工程师，侧重平台安全机制与防御加固。",
        "prerequisites": ["Java/Kotlin 或 Swift", "移动开发基础", "HTTP/TLS", "密码学基础"],
        "outcomes": [
            "理解 Android/iOS 沙箱与权限模型",
            "实施安全数据存储与通信加密",
            "配置应用加固与完整性校验",
            "在授权范围内分析应用安全风险",
        ],
        "ecosystem": "Android Studio, Xcode, MobSF, Frida(授权分析), OWASP MASVS",
    },
    "云安全": {
        "intro": (
            "云安全遵循共享责任模型：云厂商保障基础设施，客户负责配置、数据与访问控制。"
            "容器、Kubernetes 与 Serverless 引入新的攻击面，"
            "身份管理（IAM）、网络策略与密钥管理是核心防御层。"
        ),
        "positioning": "面向云架构师与 DevSecOps 工程师，侧重 AWS/阿里云/K8s 安全配置。",
        "prerequisites": ["云计算基础", "Docker/Kubernetes", "网络基础", "IAM 概念"],
        "outcomes": [
            "理解云共享责任模型与各服务安全边界",
            "配置 IAM 最小权限与 MFA",
            "加固容器镜像与 K8s RBAC/NetworkPolicy",
            "满足等保、SOC2 等合规要求",
        ],
        "ecosystem": "AWS Security Hub, Azure Defender, CIS Benchmarks, Falco, OPA/Gatekeeper",
    },
    "数据结构与算法": {
        "intro": (
            "数据结构与算法是程序效率与问题求解能力的基石。"
            "从数组、链表到树、图，从排序、查找到动态规划与图算法，"
            "系统掌握后可应对工程优化与技术面试中的复杂问题。"
        ),
        "positioning": "面向所有程序员，建立从基础结构到高级算法的完整知识体系。",
        "prerequisites": ["一门编程语言", "基本数学", "逻辑思维"],
        "outcomes": [
            "分析时间/空间复杂度并选择合适数据结构",
            "实现常见排序、查找与图算法",
            "运用动态规划、贪心与回溯解决优化问题",
            "在工程中识别可算法优化的热点路径",
        ],
        "ecosystem": "LeetCode, CLRS, 《算法导论》, Python/Java 标准库",
    },
    "机器学习": {
        "intro": (
            "机器学习让计算机从数据中学习模式，无需显式编程规则。"
            "监督学习（分类/回归）、无监督学习（聚类/降维）与集成方法是核心内容，"
            "scikit-learn 提供经典算法实现，是入门与实践的首选工具。"
        ),
        "positioning": "面向数据分析师与工程师，侧重算法原理、特征工程与模型评估。",
        "prerequisites": ["Python", "线性代数", "概率统计", "NumPy/Pandas"],
        "outcomes": [
            "选择并训练适合的监督/无监督模型",
            "完成特征工程与超参数调优",
            "使用交叉验证与指标评估模型泛化能力",
            "部署模型并监控数据漂移",
        ],
        "ecosystem": "scikit-learn, XGBoost, LightGBM, Jupyter, MLflow",
    },
    "深度学习": {
        "intro": (
            "深度学习以多层神经网络自动学习层次化特征表示。"
            "CNN 处理图像，RNN/LSTM/Transformer 处理序列，"
            "PyTorch 与 TensorFlow 是训练与部署的主流框架。"
        ),
        "positioning": "面向 AI 工程师，从神经网络基础到 Transformer 与工程部署。",
        "prerequisites": ["Python", "线性代数", "机器学习基础", "微积分"],
        "outcomes": [
            "理解反向传播、激活函数与优化器原理",
            "构建 CNN/RNN/Transformer 模型并完成训练",
            "应用迁移学习、正则化与批归一化",
            "使用 PyTorch/TensorFlow 完成端到端项目",
        ],
        "ecosystem": "PyTorch, TensorFlow, Hugging Face, CUDA, TensorBoard",
    },
    "自然语言处理": {
        "intro": (
            "自然语言处理（NLP）使计算机理解、生成与翻译人类语言。"
            "从分词、词向量到 BERT/GPT 大语言模型，"
            "Transformer 架构彻底改变了 NLP 的技术范式。"
        ),
        "positioning": "面向 NLP 工程师，覆盖传统方法与预训练语言模型应用。",
        "prerequisites": ["Python", "机器学习", "概率统计", "深度学习基础"],
        "outcomes": [
            "完成文本预处理、分词与向量化",
            "训练文本分类、NER 与情感分析模型",
            "使用预训练模型进行微调与推理",
            "构建问答、翻译等 NLP 应用",
        ],
        "ecosystem": "Hugging Face Transformers, spaCy, jieba, NLTK, LangChain",
    },
    "计算机视觉": {
        "intro": (
            "计算机视觉让机器从图像与视频中提取语义信息。"
            "从传统特征（SIFT/ORB）到深度学习（YOLO、Faster R-CNN、分割网络），"
            "CV 在安防、医疗、自动驾驶等领域广泛应用。"
        ),
        "positioning": "面向 CV 工程师，从图像处理基础到目标检测与分割实战。",
        "prerequisites": ["Python", "线性代数", "深度学习基础", "NumPy/OpenCV"],
        "outcomes": [
            "使用 OpenCV 进行图像预处理与特征提取",
            "训练图像分类与目标检测模型",
            "理解 YOLO、Faster R-CNN 等检测架构",
            "完成 OCR、人脸识别等应用部署",
        ],
        "ecosystem": "OpenCV, PyTorch, torchvision, YOLO, MMDetection",
    },
    "强化学习": {
        "intro": (
            "强化学习通过智能体与环境的交互学习最优策略，"
            "以累积奖励最大化为目标。MDP、Q-Learning、策略梯度与 DQN/PPO "
            "是核心算法，广泛应用于游戏 AI 与机器人控制。"
        ),
        "positioning": "面向 AI 研究员，从 MDP 基础到深度强化学习算法。",
        "prerequisites": ["Python", "概率论", "机器学习", "深度学习基础"],
        "outcomes": [
            "形式化 MDP 并理解值函数与策略",
            "实现 Q-Learning、DQN、PPO 等算法",
            "使用 OpenAI Gym 进行环境交互实验",
            "分析探索-利用权衡与训练稳定性",
        ],
        "ecosystem": "OpenAI Gym/Gymnasium, Stable-Baselines3, PyTorch, RLlib",
    },
    "数据挖掘": {
        "intro": (
            "数据挖掘从大规模数据中发现隐藏模式与知识。"
            "关联规则（Apriori）、聚类、分类、异常检测与推荐算法是核心方法，"
            "广泛应用于电商、金融与互联网运营分析。"
        ),
        "positioning": "面向数据分析师，侧重算法原理与业务场景应用。",
        "prerequisites": ["Python/SQL", "统计学", "机器学习基础", "数据库"],
        "outcomes": [
            "完成数据清洗、转换与探索性分析",
            "挖掘关联规则与频繁项集",
            "应用聚类与异常检测发现业务洞察",
            "构建推荐系统并评估效果",
        ],
        "ecosystem": "Pandas, scikit-learn, Apriori, Spark MLlib, Weka",
    },
    "知识图谱": {
        "intro": (
            "知识图谱以图结构组织实体及其关系，支持语义搜索与推理。"
            "本体建模、知识抽取、融合与图数据库存储构成完整链路，"
            "在搜索引擎、智能问答与企业知识管理中应用广泛。"
        ),
        "positioning": "面向知识工程师，覆盖从本体设计到 Neo4j 应用的全流程。",
        "prerequisites": ["Python", "NLP 基础", "图论基础", "数据库"],
        "outcomes": [
            "设计领域本体与实体关系 schema",
            "从文本中抽取实体与关系",
            "使用 Neo4j 存储与查询知识图谱",
            "构建基于图谱的问答与推荐应用",
        ],
        "ecosystem": "Neo4j, Apache Jena, OpenKE, spaCy, Cypher",
    },
    "大语言模型": {
        "intro": (
            "大语言模型（LLM）基于 Transformer 架构，通过大规模预训练习得语言理解与生成能力。"
            "微调、RLHF、Prompt 工程、RAG 与 Agent 是当前应用落地的关键技术，"
            "GPT、LLaMA、Qwen 等模型推动 AI 应用范式变革。"
        ),
        "positioning": "面向 AI 应用工程师，覆盖 LLM 原理、微调、部署与应用开发。",
        "prerequisites": ["Python", "深度学习", "NLP 基础", "PyTorch"],
        "outcomes": [
            "理解 Transformer 与预训练-微调范式",
            "完成指令微调与 RLHF 流程",
            "设计 Prompt 与 RAG 检索增强方案",
            "部署量化模型并构建 Agent 应用",
        ],
        "ecosystem": "Hugging Face, vLLM, LangChain, LlamaIndex, OpenAI API",
    },
    "AIGC": {
        "intro": (
            "AIGC（AI Generated Content）涵盖文本、图像、视频、音频与 3D 内容的 AI 生成。"
            "Diffusion 模型（Stable Diffusion）、GPT 类文本生成与多模态模型是核心技术，"
            "在创意设计、内容生产与娱乐领域快速普及。"
        ),
        "positioning": "面向创作者与 AI 工程师，覆盖主流生成模型原理与应用。",
        "prerequisites": ["Python", "深度学习", "PyTorch", "基础美术/设计概念"],
        "outcomes": [
            "理解 Diffusion 与 GAN 生成原理",
            "使用 Stable Diffusion 进行图像生成与微调",
            "评估生成内容质量与安全风险",
            "构建多模态 AIGC 应用工作流",
        ],
        "ecosystem": "Stable Diffusion, ComfyUI, Midjourney API, Runway, ElevenLabs",
    },
    "区块链": {
        "intro": (
            "区块链是以密码学保障的去中心化分布式账本。"
            "共识机制（PoW/PoS）、智能合约与 DApp 构成 Web3 技术栈，"
            "以太坊与 Solidity 是智能合约开发的主流平台。"
        ),
        "positioning": "面向区块链开发者，从密码学基础到智能合约与 DApp 开发。",
        "prerequisites": ["密码学基础", "JavaScript/Python", "计算机网络", "数据结构"],
        "outcomes": [
            "理解区块链架构与共识机制",
            "使用 Solidity 编写与测试智能合约",
            "开发 DApp 并连接 MetaMask 钱包",
            "评估 DeFi/NFT 项目的安全风险",
        ],
        "ecosystem": "Ethereum, Solidity, Hardhat, Web3.js, MetaMask, IPFS",
    },
    "游戏开发": {
        "intro": (
            "游戏开发融合编程、美术、物理与 AI 等多学科。"
            "Unity 与 Unreal 是主流引擎，游戏循环、场景管理、物理碰撞与网络同步是核心系统。"
        ),
        "positioning": "面向游戏程序员，从引擎基础到性能优化与网络多人。",
        "prerequisites": ["C#/C++", "面向对象", "线性代数", "基本物理概念"],
        "outcomes": [
            "理解游戏循环与组件化架构",
            "实现碰撞检测、动画与粒子系统",
            "优化渲染与内存性能",
            "设计客户端-服务器网络同步方案",
        ],
        "ecosystem": "Unity, Unreal Engine, Godot, Blender, Photon",
    },
    "计算机图形学": {
        "intro": (
            "计算机图形学研究生成与渲染视觉图像的算法与系统。"
            "从光栅化管线、着色器到光线追踪与全局光照，"
            "OpenGL/Vulkan 是底层图形 API 标准。"
        ),
        "positioning": "面向图形程序员，从线性代数到现代渲染管线。",
        "prerequisites": ["线性代数", "C/C++", "微积分", "基本物理光学"],
        "outcomes": [
            "理解 MVP 变换与渲染管线各阶段",
            "编写 GLSL/HLSL 着色器",
            "实现 Phong/Blinn 光照与纹理映射",
            "了解光线追踪与全局光照原理",
        ],
        "ecosystem": "OpenGL, Vulkan, DirectX, Three.js, Blender",
    },
    "音视频处理": {
        "intro": (
            "音视频处理涵盖采集、编码、传输与播放全链路。"
            "H.264/H.265 视频编码、AAC 音频编码与 FFmpeg 工具链是工业标准，"
            "WebRTC 与 HLS 支撑实时与点播流媒体。"
        ),
        "positioning": "面向流媒体工程师，从编码原理到 FFmpeg 实战与 WebRTC。",
        "prerequisites": ["C/Python", "信号处理基础", "计算机网络", "数字媒体概念"],
        "outcomes": [
            "理解音视频采样、编码与封装格式",
            "使用 FFmpeg 进行转码、剪辑与流媒体",
            "配置 HLS/RTMP 直播与 WebRTC 通话",
            "解决音视频同步与延迟问题",
        ],
        "ecosystem": "FFmpeg, GStreamer, WebRTC, OBS, HLS, DASH",
    },
    "物联网": {
        "intro": (
            "物联网（IoT）将传感器、嵌入式设备与云平台连接，实现万物互联。"
            "MQTT、CoAP 等轻量协议适合受限设备，"
            "边缘计算与设备安全是规模化部署的关键挑战。"
        ),
        "positioning": "面向 IoT 工程师，从传感器到云平台的全栈开发。",
        "prerequisites": ["C/Python", "嵌入式基础", "计算机网络", "Linux"],
        "outcomes": [
            "选择适合的 IoT 通信协议与硬件平台",
            "开发嵌入式固件并对接 MQTT  broker",
            "设计边缘计算与云端数据处理架构",
            "实施设备认证与固件安全更新",
        ],
        "ecosystem": "MQTT, ESP32, Raspberry Pi, AWS IoT, ThingsBoard",
    },
    "低代码开发": {
        "intro": (
            "低代码/无代码平台通过可视化建模加速应用交付。"
            "表单设计、流程编排、数据建模与 API 集成是核心能力，"
            "适合企业内部系统与快速原型，但需关注可维护性与安全。"
        ),
        "positioning": "面向业务开发者与技术负责人，评估低代码平台选型与治理。",
        "prerequisites": ["基本编程概念", "数据库基础", "HTTP/API 概念", "业务流程理解"],
        "outcomes": [
            "使用低代码平台构建表单与审批流程",
            "设计数据模型并集成外部 API",
            "配置权限与多环境部署",
            "评估低代码项目的长期可维护性",
        ],
        "ecosystem": "OutSystems, Mendix, 钉钉宜搭, 飞书多维表格, Power Apps",
    },
    "量子计算": {
        "intro": (
            "量子计算利用量子比特的叠加与纠缠特性进行并行计算。"
            "Shor 与 Grover 算法展示了量子优势，"
            "IBM Q、Google Sycamore 等硬件与 Qiskit 等软件栈推动领域发展。"
        ),
        "positioning": "面向对量子计算感兴趣的开发者，从量子比特到算法与编程。",
        "prerequisites": ["线性代数", "概率论", "Python", "基本物理概念"],
        "outcomes": [
            "理解量子比特、量子门与量子电路",
            "使用 Qiskit 编写并模拟量子程序",
            "了解 Shor/Grover 算法的原理与影响",
            "认识 NISQ 时代量子计算的局限与前景",
        ],
        "ecosystem": "Qiskit, Cirq, IBM Quantum, Google Cirq, PennyLane",
    },
    "Rust系统编程": {
        "intro": (
            "Rust 系统编程将内存安全与零成本抽象结合，"
            "适合操作系统、嵌入式、WebAssembly 与高性能服务。"
            "所有权、生命周期与 unsafe 块是系统级开发的核心概念。"
        ),
        "positioning": "面向有系统编程经验的开发者，深入 Rust 内存模型与 FFI。",
        "prerequisites": ["Rust 语言基础", "C 语言", "操作系统", "计算机体系结构"],
        "outcomes": [
            "在系统级代码中正确使用 unsafe 与 FFI",
            "开发嵌入式 Rust 应用与驱动接口",
            "编译 WebAssembly 模块供浏览器调用",
            "参与操作系统或底层库的开源贡献",
        ],
        "ecosystem": "cargo, no_std, bindgen, wasm-pack, tokio, embedded-hal",
    },
}


# ---------------------------------------------------------------------------
# Module-specific knowledge snippets (domain, module) -> rich paragraphs
# ---------------------------------------------------------------------------

def _concepts(*items: tuple[str, str]) -> list[dict]:
    return [{"title": t, "body": b} for t, b in items]


def _pitfalls(*items: tuple[str, str]) -> list[dict]:
    return [{"title": t, "body": b} for t, b in items]


def _sec(domain: str) -> str:
    if domain in ("网络安全", "Web安全", "密码学", "渗透测试", "逆向工程", "漏洞挖掘", "移动安全", "云安全"):
        return SECURITY_NOTE + " 所有测试活动必须在书面授权范围内进行。"
    return ""


# Per-module handcrafted content keyed by (domain, module)
MODULE_SNIPPETS: dict[tuple[str, str], dict] = {}


def _add(domain: str, module: str, **kwargs):
    MODULE_SNIPPETS[(domain, module)] = kwargs


# ===== 网络安全 =====
_add("网络安全", "网络安全概述",
    intro="网络安全（Network Security）保护数据在网络上传输与交换时的机密性、完整性与可用性。CIA 三要素是评估安全方案的基本框架：机密性防止未授权读取，完整性防止篡改，可用性保障服务持续运行。现代网络面临 APT、勒索软件与供应链攻击等复杂威胁，需要纵深防御（Defense in Depth）策略。",
    concepts=_concepts(
        ("CIA 三要素", "机密性（Confidentiality）通过加密与访问控制实现；完整性（Integrity）通过哈希、MAC 与数字签名保障；可用性（Availability）通过冗余、负载均衡与 DDoS 防护维持。三者缺一不可。"),
        ("纵深防御", "不依赖单一防护点，在网络边界、内部隔离、主机加固、应用安全各层叠加控制。任一层被突破时，后续层仍能提供保护。"),
        ("威胁建模", "识别资产、攻击面与潜在攻击者，按 STRIDE 模型分类威胁（欺骗、篡改、否认、信息泄露、拒绝服务、权限提升），优先处理高风险项。"),
        ("合规框架", "等保 2.0、ISO 27001、NIST CSF 等框架提供安全控制基线，企业应结合自身业务选择适用标准。"),
    ),
    mechanism="网络安全的实现依赖分层控制：物理层防窃听与设备安全，链路层 MAC 过滤与 VLAN 隔离，网络层 ACL 与 IPSec，传输层 TLS，应用层 WAF 与 API 网关。各层协同形成完整防护链。",
    workflow="1. 资产盘点与网络拓扑梳理 → 2. 威胁建模与风险评估 → 3. 制定安全策略与基线 → 4. 部署边界防护与监控 → 5. 定期审计与演练 → 6. 持续改进。",
    security=_sec("网络安全"),
)

_add("网络安全", "网络攻击",
    intro="理解网络攻击类型是设计有效防御的前提。本模块从防御视角分类讲解常见攻击手法及其检测与缓解措施，不提供攻击实施指导。",
    concepts=_concepts(
        ("被动攻击", "嗅探、流量分析等不修改数据的攻击，通过加密通信（TLS）与网络分段降低风险。"),
        ("主动攻击", "篡改、重放、中间人攻击等修改或注入数据的攻击，需结合认证、完整性校验与 IDS 检测。"),
        ("DoS/DDoS", "通过耗尽带宽或连接资源使服务不可用。缓解手段包括流量清洗、限速、Anycast 与 CDN 分散。"),
        ("中间人攻击", "攻击者插入通信路径窃听或篡改。防御依赖证书验证、HSTS 与证书锁定（Certificate Pinning）。"),
    ),
    mechanism="攻击通常遵循侦察→武器化→投递→利用→安装→命令控制→行动（Cyber Kill Chain）模型。防御方应在各阶段部署检测点：流量异常、IOC 匹配、行为分析。",
    security="仅分析已公开的攻击案例与威胁情报，在隔离实验环境复现以验证防御规则有效性。",
)

_add("网络安全", "网络防御",
    intro="网络防御是主动保护网络基础设施的策略与技术集合，包括边界防护、入侵检测、访问控制与安全监控。",
    concepts=_concepts(
        ("最小权限原则", "用户与系统仅授予完成任务所需的最小网络访问权限，减少攻击面。"),
        ("网络分段", "将网络划分为安全区域（DMZ、内网、管理网），区域间通过防火墙控制流量。"),
        ("零信任", "「永不信任，始终验证」，每次访问都需身份认证与授权，不依赖网络位置。"),
        ("安全基线", "统一配置标准（关闭不必要端口、禁用弱协议、启用日志），通过自动化工具合规检查。"),
    ),
    mechanism="防御体系包含预防（防火墙/ACL）、检测（IDS/IPS/SIEM）、响应（SOAR/应急预案）三层。SIEM 聚合日志进行关联分析，SOAR 自动化响应已知威胁。",
    workflow="制定策略 → 部署控制 → 配置监控 → 建立告警 → 定期演练 → 复盘改进。",
)

_add("网络安全", "防火墙",
    intro="防火墙是网络边界的第一道防线，通过规则集过滤进出流量。状态防火墙跟踪连接状态，下一代防火墙（NGFW）还集成应用识别与 IPS。",
    concepts=_concepts(
        ("包过滤防火墙", "基于 IP、端口、协议的五元组规则过滤，无状态，速度快但无法识别应用层。"),
        ("状态防火墙", "维护连接状态表，只允许属于已建立连接的返回流量，安全性更高。"),
        ("NGFW", "集成 DPI、应用识别、URL 过滤、IPS 与 VPN，可基于用户/应用而非仅 IP 制定策略。"),
        ("规则设计原则", "默认拒绝（Default Deny），白名单放行；规则从具体到通用排序；定期审计冗余规则。"),
    ),
    mechanism="数据包到达 → 匹配 ACL 规则（自上而下）→ 状态检查 → 应用层检测（NGFW）→ 允许/拒绝/记录。",
    configuration="iptables/nftables（Linux）、pfSense、Cisco ASA 配置示例：先定义对象组，再编写 ACL，最后启用日志与告警。",
    debugging="使用 tcpdump/Wireshark 在防火墙两侧抓包对比，确认规则是否按预期过滤；检查连接跟踪表（conntrack）。",
)

_add("网络安全", "IDS/IPS",
    intro="入侵检测系统（IDS）监控网络或主机流量发现可疑活动；入侵防御系统（IPS）可主动阻断攻击。Snort 与 Suricata 是开源主流方案。",
    concepts=_concepts(
        ("检测方法", "签名检测匹配已知攻击特征；异常检测建立基线识别偏离；启发式检测识别攻击行为模式。"),
        ("IDS vs IPS", "IDS 旁路部署仅告警；IPS 串联部署可阻断，但存在误报导致业务中断的风险。"),
        ("规则管理", "Snort/Suricata 规则需定期更新（Emerging Threats 等），自定义规则应对内部威胁。"),
        ("告警疲劳", "过多误报导致告警被忽略，需调优阈值、关联分析与优先级分级。"),
    ),
    mechanism="流量镜像/串联 → 协议解析 → 规则/ML 匹配 → 生成告警 → SIEM 关联 → 响应（IPS 阻断）。",
    configuration="Suricata 配置：HOME_NET/EXTERNAL_NET 定义、规则文件路径、输出到 EVE JSON 供 ELK 分析。",
)

_add("网络安全", "VPN",
    intro="虚拟专用网（VPN）在公共网络上建立加密隧道，实现远程安全接入。IPSec 与 SSL/TLS VPN 是两种主流技术。",
    concepts=_concepts(
        ("IPSec VPN", "网络层加密，支持站点到站点与远程接入，IKE 协商 SA，ESP 封装加密数据。"),
        ("SSL VPN", "基于 TLS 的应用层 VPN，浏览器即可接入，适合移动办公。"),
        ("WireGuard", "现代轻量 VPN 协议，代码简洁、性能高，内核级实现。"),
        ("Split Tunnel", "仅企业流量走 VPN，互联网直连。全隧道更安全但增加带宽压力。"),
    ),
    mechanism="IKE 阶段一协商加密算法与认证 → 阶段二建立 IPSec SA → 数据经 ESP/AH 封装传输 → 对端解密验证。",
    security="使用 AES-256-GCM 与 ECDH 密钥交换；禁用 PPTP/L2TP 等弱协议；启用 MFA 认证。",
)

_add("网络安全", "网络隔离",
    intro="网络隔离通过 VLAN、微隔离（Micro-segmentation）等技术限制横向移动，即使攻击者突破边界也难以访问核心资产。",
    concepts=_concepts(
        ("VLAN", "二层逻辑隔离，不同 VLAN 间需三层路由，ACL 控制跨 VLAN 流量。"),
        ("DMZ", "放置对外服务的缓冲区，与内网严格隔离，即使 Web 服务器被攻破也不直接暴露内网。"),
        ("微隔离", "在虚拟化/容器环境中按工作负载粒度隔离，Calico/Cilium 实现 K8s 网络策略。"),
        ("Air Gap", "物理隔离的极高安全网络，用于关键基础设施，数据交换需人工审批。"),
    ),
    mechanism="定义安全区域 → 绘制流量矩阵（谁可以访问谁）→ 部署 ACL/NetworkPolicy → 持续监控违规流量。",
)

_add("网络安全", "DDoS防护",
    intro="分布式拒绝服务（DDoS）攻击通过大量僵尸主机耗尽目标带宽或连接资源。防护需多层：本地限速、ISP 清洗、CDN 分散。",
    concepts=_concepts(
        ("攻击类型", " volumetric（UDP/ICMP 洪水）、protocol（SYN 洪水）、application（HTTP 慢速攻击）。"),
        ("SYN Cookie", "不分配连接资源，用密码学 cookie 验证 SYN，抵御 SYN 洪水。"),
        ("流量清洗", "云清洗中心识别并过滤恶意流量，仅转发合法流量到源站。"),
        ("Anycast", "将流量分散到全球多个节点，单点攻击被稀释。"),
    ),
    mechanism="检测异常流量模式 → 触发 BGP 引流至清洗中心 → 多层过滤（黑名单、速率限制、挑战验证）→ 回注干净流量。",
    case_study="某电商平台在促销期间遭遇 500Gbps UDP 洪水，通过 CDN Anycast + 云清洗在 3 分钟内恢复服务。",
)

_add("网络安全", "端口扫描",
    intro="端口扫描是授权安全评估中识别开放服务的基础手段。本模块讲解扫描原理与防御检测，强调仅在授权范围内使用。",
    concepts=_concepts(
        ("扫描类型", "TCP SYN 扫描（半开）、全连接扫描、UDP 扫描、ACK 扫描等，各有适用场景。"),
        ("Nmap 基础", "Nmap 是标准扫描工具，-sS SYN 扫描、-sV 版本探测、-O 操作系统识别（仅限授权目标）。"),
        ("防御检测", "IDS 识别扫描特征（短时间内大量 SYN、端口顺序探测），触发告警或自动封禁。"),
        ("端口最小化", "仅开放业务必需端口，关闭不必要服务，定期审计开放端口清单。"),
    ),
    security="端口扫描仅可在获得书面授权的目标上进行。未授权扫描可能违反《网络安全法》等法规。",
    workflow="1. 确认授权范围 → 2. 选择扫描策略 → 3. 执行扫描并记录 → 4. 分析开放服务 → 5. 纳入风险评估报告。",
)

_add("网络安全", "嗅探",
    intro="网络嗅探捕获流经网卡的数据包用于故障排查或安全分析。在交换网络中需端口镜像；防御依赖加密通信。",
    concepts=_concepts(
        ("混杂模式", "网卡接收所有帧而非仅目标地址帧，Wireshark/tcpdump 依赖此模式抓包。"),
        ("交换网络限制", "交换机仅转发目标 MAC 帧，需 SPAN/RSPAN 端口镜像才能嗅探其他端口流量。"),
        ("加密防御", "TLS 1.3 使嗅探者只能看到密文，无法读取应用层内容。"),
        ("ARP 欺骗检测", "攻击者通过 ARP 欺骗成为中间人，DHCP Snooping 与 DAI 可防御。"),
    ),
    mechanism="设置镜像端口 → 启动抓包 → 过滤协议/地址 → 分析异常（明文密码、异常 DNS 查询）。",
    security="嗅探仅限自有网络或授权评估；捕获的数据含敏感信息，需加密存储并限定访问。",
)

_add("网络安全", "协议安全",
    intro="网络协议设计时的安全假设在现代环境中常不成立。DNS、BGP、SNMP 等协议需额外加固或使用安全替代方案。",
    concepts=_concepts(
        ("DNS 安全", "DNSSEC 防止 DNS 欺骗；DoH/DoT 加密 DNS 查询；限制区域传送。"),
        ("BGP 安全", "RPKI 验证路由起源，防止路由劫持。"),
        ("SNMP 安全", "使用 SNMPv3 认证加密，禁用默认 community string。"),
        ("禁用弱协议", "Telnet、FTP、HTTP 应替换为 SSH、SFTP、HTTPS。"),
    ),
    mechanism="协议审计 → 识别明文/弱认证协议 → 制定迁移计划 → 部署安全替代 → 监控残留使用。",
)

_add("网络安全", "无线安全",
    intro="无线网络（Wi-Fi）因广播特性面临窃听、 rogue AP 与破解风险。WPA3 是当前推荐标准。",
    concepts=_concepts(
        ("WPA3", "SAE（Dragonfly）替代 PSK，抵御离线字典攻击；192-bit 安全模式用于企业。"),
        ("企业认证", "802.1X + EAP-TLS 证书认证，每台设备独立凭证。"),
        ("Rogue AP 检测", "WIDS 扫描未授权接入点，对比 MAC 白名单。"),
        ("访客网络隔离", "访客 Wi-Fi 与内网 VLAN 隔离，仅提供互联网访问。"),
    ),
    configuration="配置 WPA3-Enterprise、启用 PMF（Protected Management Frames）、隐藏 SSID 非必要不启用。",
)

_add("网络安全", "安全审计",
    intro="安全审计系统性地检查网络配置、日志与合规状态，发现偏离基线的风险。",
    concepts=_concepts(
        ("审计范围", "网络设备配置、ACL 规则、用户权限、日志完整性、补丁状态。"),
        ("自动化审计", "Nessus/OpenSCAP 等工具自动扫描配置合规性，生成差距报告。"),
        ("日志审计", "检查防火墙/IDS 日志是否完整、时间同步、保留策略符合合规要求。"),
        ("审计频率", "关键系统每季度审计，变更后立即审计，年度全面审计。"),
    ),
    workflow="制定审计计划 → 收集配置与日志 → 对照基线检查 → 编写发现项 → 跟踪整改 → 验证关闭。",
)

_add("网络安全", "应急响应",
    intro="网络安全应急响应在事件发生时快速遏制、根除威胁并恢复业务。NIST 框架定义准备、检测分析、遏制、根除恢复、事后总结五阶段。",
    concepts=_concepts(
        ("事件分类", "按严重级别（P1-P4）分类，P1 为核心业务中断需立即响应。"),
        ("遏制策略", "短期：隔离受影响主机；长期：封堵攻击入口、修改凭证。"),
        ("证据保全", "镜像磁盘、导出日志、记录时间线，满足取证与合规要求。"),
        ("沟通机制", "明确事件指挥官、技术团队、法务、公关的职责与升级路径。"),
    ),
    workflow="检测告警 → 初步分析确认事件 → 启动应急预案 → 遏制与根除 → 恢复服务 → 事后复盘（Lessons Learned）。",
    case_study="勒索软件事件：立即断网隔离 → 确认备份完整性 → 从干净备份恢复 → 修补入口漏洞 → 提交 IOC 至威胁情报平台。",
)

_add("网络安全", "网络安全最佳实践",
    intro="汇总网络安全领域的工程最佳实践，帮助建立可持续的安全运营体系。",
    practices=[
        "默认拒绝策略，最小权限开放端口与服务",
        "全流量加密（TLS 1.3），禁用弱密码套件",
        "网络分段 + 微隔离，限制横向移动",
        "集中日志（SIEM）+ 7×24 监控告警",
        "定期漏洞扫描（授权）与渗透测试",
        "制定并演练应急响应预案",
        "持续威胁情报订阅与 IOC 更新",
    ],
    references=["NIST SP 800-53", "CIS Controls v8", "等保 2.0 网络安全要求", "OWASP ASVS"],
)


def _finalize_module(base: dict, domain: str, module: str, category: str, idx: int, total: int) -> dict:
    """Merge snippet with fallback fields."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_security_ai_builder",
        Path(__file__).parent / "_security_ai_builder.py",
    )
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    build_from_kb = builder.build_from_kb
    build_generic = builder.build_generic

    if not base:
        base = build_from_kb(domain, module, category)
    if base is None:
        base = build_generic(domain, module, category, idx, total)
    else:
        defaults = build_generic(domain, module, category, idx, total)
        for k, v in defaults.items():
            if k not in base or not base[k]:
                base[k] = v
        if not base.get("concepts"):
            base["concepts"] = defaults["concepts"]
        if not base.get("pitfalls"):
            base["pitfalls"] = defaults["pitfalls"]
        if not base.get("practices"):
            base["practices"] = defaults["practices"]
        if not base.get("references"):
            base["references"] = defaults["references"]
    return base


def generate_all_modules() -> dict:
    """Generate MODULE_CONTENT for all target domains."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_security_ai_builder",
        Path(__file__).parent / "_security_ai_builder.py",
    )
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    build_from_kb = builder.build_from_kb
    build_generic = builder.build_generic

    content: dict = {}
    for cfg in DOMAINS_CONFIG:
        domain = cfg["name"]
        if domain not in TARGET_DOMAINS:
            continue
        category = cfg["category"]
        modules = cfg["modules"]
        total = len(modules)
        for idx, module in enumerate(modules):
            key = (domain, module)
            if key in MODULE_SNIPPETS:
                content[key] = _finalize_module(dict(MODULE_SNIPPETS[key]), domain, module, category, idx, total)
            else:
                kb = build_from_kb(domain, module, category)
                if kb:
                    content[key] = _finalize_module(kb, domain, module, category, idx, total)
                else:
                    content[key] = build_generic(domain, module, category, idx, total)
    return content


def _py_repr(obj, indent=0) -> str:
    """Render Python literal with nice formatting."""
    sp = "    " * indent
    if isinstance(obj, str):
        return repr(obj)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        if all(isinstance(x, str) for x in obj):
            items = ",\n".join(f"{sp}    {repr(x)}" for x in obj)
            return f"[\n{items},\n{sp}]"
        if all(isinstance(x, dict) and "title" in x for x in obj):
            parts = []
            for x in obj:
                parts.append(
                    f"{sp}    {{\"title\": {x['title']!r}, \"body\": {x['body']!r}}}"
                )
            return "[\n" + ",\n".join(parts) + f",\n{sp}]"
        items = ",\n".join(f"{sp}    {_py_repr(x, indent+1)}" for x in obj)
        return f"[\n{items},\n{sp}]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = []
        for k, v in obj.items():
            lines.append(f"{sp}    {k!r}: {_py_repr(v, indent+1)},")
        return "{\n" + "\n".join(lines) + f"\n{sp}}}"
    if isinstance(obj, tuple):
        inner = ", ".join(_py_repr(x, indent) for x in obj)
        return f"({inner})"
    return repr(obj)


def write_output():
    modules = generate_all_modules()
    lines = [
        '# -*- coding: utf-8 -*-',
        '"""安全、AI 与其他领域手工教程内容库"""',
        '',
        'MODULE_CONTENT = {',
    ]
    for (domain, module), data in sorted(modules.items()):
        lines.append(f'    ({domain!r}, {module!r}): {{')
        for k, v in data.items():
            lines.append(f'        {k!r}: {_py_repr(v, 2)},')
        lines.append('    },')
    lines.append('}')
    lines.append('')
    lines.append('DOMAIN_OVERVIEWS = {')
    for domain in TARGET_DOMAINS:
        if domain not in DOMAIN_OVERVIEWS_RAW:
            continue
        d = DOMAIN_OVERVIEWS_RAW[domain]
        lines.append(f'    {domain!r}: {{')
        for k, v in d.items():
            lines.append(f'        {k!r}: {_py_repr(v, 2)},')
        lines.append('    },')
    lines.append('}')
    lines.append('')

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(modules)} modules and {len(DOMAIN_OVERVIEWS_RAW)} overviews")


if __name__ == "__main__":
    write_output()
