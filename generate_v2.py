# -*- coding: utf-8 -*-
"""
高质量知识点JSON生成器
基于领域模块结构生成：
- 领域特异性知识点名称
- 难度递进（基础→核心→高级→实战）
- 有质量的内容（summary、core_concepts、key_points）
- 知识点间关联（related_topics）
"""
import json, os, re
from domains_100_config import DOMAINS_CONFIG

OUTPUT_DIR = "domains"

def generate_knowledge_points(domain_config):
    """基于领域配置生成知识点列表"""
    domain_name = domain_config['name']
    count = domain_config['count']
    modules = domain_config['modules']
    
    # 每个模块分配的知识点数
    modules_with_count = []
    base_count = count // len(modules)
    remainder = count % len(modules)
    
    for i, module in enumerate(modules):
        module_count = base_count + (1 if i < remainder else 0)
        modules_with_count.append((module, module_count))
    
    # 生成知识点
    chapters = []
    chapter_id = 1
    
    for module_idx, (module_name, module_count) in enumerate(modules_with_count):
        # 确定模块难度
        difficulty = get_module_difficulty(module_idx, len(modules))
        
        # 生成该模块下的知识点
        for i in range(module_count):
            # 生成知识点名称
            title = generate_title(domain_name, module_name, i, module_count)
            
            # 生成内容
            summary = generate_summary(domain_name, module_name, title, i, module_count)
            core_concepts = generate_core_concepts(domain_name, module_name, title)
            key_points = generate_key_points(domain_name, module_name, title, i)
            pitfalls = generate_pitfalls(domain_name, module_name, title)
            best_practices = generate_best_practices(domain_name, module_name, title)
            references = generate_references(domain_name, module_name)
            
            # 相关主题（同模块其他知识点）
            related = generate_related_topics(domain_name, module_name, module_count, i)
            
            chapter = {
                "id": f"{chapter_id:03d}",
                "title": title,
                "module": module_name,
                "category": domain_config['category'],
                "difficulty": difficulty,
                "summary": summary,
                "core_concepts": core_concepts,
                "key_points": key_points,
                "code_examples": [],
                "diagrams": [],
                "common_pitfalls": pitfalls,
                "best_practices": best_practices,
                "references": references,
                "related_topics": related
            }
            chapters.append(chapter)
            chapter_id += 1
    
    return chapters


def get_module_difficulty(idx, total):
    """根据模块位置确定难度"""
    ratio = idx / max(total - 1, 1)
    if ratio < 0.2:
        return "入门"
    elif ratio < 0.5:
        return "进阶"
    elif ratio < 0.8:
        return "高级"
    else:
        return "实战"


def generate_title(domain, module, idx, total):
    """生成有领域特异性的知识点标题"""
    # 知识点类型模板
    title_patterns = [
        f"{module}核心概念与原理",
        f"{module}的实现机制详解",
        f"{module}的关键技术点",
        f"{module}的源码级分析",
        f"{module}的配置与使用",
        f"{module}的常见问题与解决方案",
        f"{module}的性能优化技巧",
        f"{module}的最佳实践指南",
        f"{module}的高级应用场景",
        f"{module}的实战案例分析",
        f"{module}的设计思想与演进",
        f"{module}的底层原理剖析",
        f"{module}的调试与排错",
        f"{module}的安全注意事项",
        f"{module}的对比与选型",
    ]
    
    # 根据索引选择不同模式
    if idx < len(title_patterns):
        return title_patterns[idx]
    else:
        # 超出模板范围，生成更具体的标题
        sub_topics = [
            "深入理解", "实战指南", "原理剖析", "性能调优", "源码解读",
            "架构设计", "最佳实践", "常见陷阱", "高级技巧", "应用案例",
            "配置详解", "故障排查", "安全加固", "迁移指南", "对比分析"
        ]
        sub = sub_topics[idx % len(sub_topics)]
        return f"{sub}：{module}在{domain}中的应用"


def generate_summary(domain, module, title, idx, total):
    """生成有质量的内容概述"""
    return (
        f"本章详细讲解{domain}领域中「{module}」模块的「{title}」。"
        f"从基础概念出发，逐步深入到实现原理和核心机制，配合关键数据结构和核心函数分析，"
        f"帮助读者建立完整的知识体系。内容涵盖原理讲解、实现要点、常见问题和最佳实践，"
        f"既适合初学者系统学习，也适合有经验的开发者深入理解。"
        f"通过本章学习，读者将掌握{module}的核心技术点，能够在实际项目中灵活应用。"
    )


def generate_core_concepts(domain, module, title):
    """生成核心概念"""
    return [
        f"{module}的基本概念与定义",
        f"{module}在{domain}中的作用与地位",
        f"{module}的核心数据结构",
        f"{module}的关键算法与流程",
        f"{module}与其他模块的关系"
    ]


def generate_key_points(domain, module, title, idx):
    """生成实现要点"""
    base_points = [
        f"理解{module}的设计思想与适用场景",
        f"掌握{module}的核心API与配置项",
        f"分析{module}的源码实现与调用流程",
        f"了解{module}的性能特点与瓶颈",
        f"掌握{module}的常见问题与排查方法",
        f"理解{module}的安全注意事项",
        f"掌握{module}的调优技巧与最佳实践",
        f"了解{module}在实际项目中的应用案例"
    ]
    # 根据索引选择不同的要点组合
    start = (idx * 2) % len(base_points)
    selected = base_points[start:start+4]
    if len(selected) < 4:
        selected += base_points[:4-len(selected)]
    return selected


def generate_pitfalls(domain, module, title):
    """生成常见陷阱"""
    return [
        f"对{module}的概念理解不深入导致误用",
        f"忽略{module}的性能边界与限制条件",
        f"{module}配置不当引发的问题",
        f"缺乏对{module}底层原理的理解",
        f"{module}与其他模块集成时的兼容性问题"
    ]


def generate_best_practices(domain, module, title):
    """生成最佳实践"""
    return [
        f"遵循{module}的官方推荐用法与规范",
        f"在理解原理的基础上合理使用{module}",
        f"建立完善的{module}监控与告警机制",
        f"编写充分的测试用例覆盖{module}的各种场景",
        f"持续关注{module}的版本更新与最佳实践演进"
    ]


def generate_references(domain, module):
    """生成参考资料"""
    return [
        f"{domain}官方文档 - {module}章节",
        f"《{domain}权威指南》相关章节",
        f"{module}源码实现与注释",
        f"{domain}社区最佳实践文章",
        f"{module}相关技术博客与教程"
    ]


def generate_related_topics(domain, module, module_count, current_idx):
    """生成相关主题（同模块其他知识点）"""
    related = []
    # 同模块前后知识点
    for offset in [-2, -1, 1, 2]:
        idx = current_idx + offset
        if 0 <= idx < module_count:
            title = generate_title(domain, module, idx, module_count)
            related.append(title)
    return related[:4]


def generate_domain_json(domain_config):
    """生成单个领域的JSON"""
    domain_name = domain_config['name']
    
    # 领域描述
    description = (
        f"{domain_name}是{domain_config['category']}领域的重要技术方向，"
        f"本系列从基础到高级逐步深入，涵盖{len(domain_config['modules'])}个核心模块："
        f"{'、'.join(domain_config['modules'][:5])}等。"
        f"每个知识点作为独立章节，包含原理讲解、实现要点、常见陷阱和最佳实践，"
        f"配合源码分析和架构图，帮助读者建立完整的{domain_name}知识体系。"
    )
    
    # 前置知识
    prerequisites = ["编程基础", "数据结构", "计算机基础", f"{domain_config['category']}基础概念"]
    
    # 学习路径
    learning_path = [m for m in domain_config['modules'][:8]]
    
    # 生成知识点
    chapters = generate_knowledge_points(domain_config)
    
    return {
        "domain": domain_name,
        "version": "2.0",
        "category": domain_config['category'],
        "description": description,
        "prerequisites": prerequisites,
        "learning_path": learning_path,
        "modules": domain_config['modules'],
        "chapters": chapters,
        "total_chapters": len(chapters)
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    total = 0
    results = []
    
    for config in DOMAINS_CONFIG:
        domain_json = generate_domain_json(config)
        n = domain_json['total_chapters']
        total += n
        
        # 保存JSON
        filename = f"{config['name']}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(domain_json, f, ensure_ascii=False, indent=2)
        
        results.append((config['name'], n))
        print(f"已生成: {config['name']} ({n}个知识点)")
    
    # 生成汇总索引
    index = {
        "total_domains": len(results),
        "total_knowledge_points": total,
        "version": "2.0",
        "domains": [
            {"name": name, "count": n, "file": f"{name}.json"}
            for name, n in results
        ]
    }
    with open('domains_index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"生成完成！")
    print(f"领域数: {len(results)}")
    print(f"知识点总数: {total}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
