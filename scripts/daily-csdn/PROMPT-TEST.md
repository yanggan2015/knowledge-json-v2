# 单次测试：主题合并 → 发布 1 篇合并长文

执行 `PROMPT.md` 的全部规则，但**仅处理 1 个主题包、发布 1 篇**（今日测试额度）。

## 指定主题包（若源文件存在且未在登记表中）

**Linux 内核 · 内存管理** — 合并以下源 chapter（跳过已在登记表的路径）：

- `Linux内核/chapters/041-内存管理核心概念与原理.md`
- `Linux内核/chapters/042-内存管理的实现机制详解.md`
- `Linux内核/chapters/043-内存管理的关键技术点.md`
- `Linux内核/chapters/045-内存管理的配置与使用.md`
- `Linux内核/chapters/046-内存管理的常见问题与解决方案.md`
- `Linux内核/chapters/047-内存管理的性能优化技巧.md`

成稿输出：`articles/csdn-merged/Linux内核-内存管理完整篇.md`

标题示例（可优化）：`Linux 内核内存管理完整篇：伙伴系统、SLUB、缺页、OOM 与调优实战`

合并后必须覆盖：伙伴系统/SLUB/VMA/page cache/OOM/cgroup/THP/缺页路径/观测命令/常见坑/Checklist。

完成后：发布 → 登记表追加（备注列列出全部源路径）→ git commit & push → 汇报 URL。
