#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Populate _content_specs_languages.py with all 212 language module specs."""

SPECS = r'''
# ===================== C 语言 =====================
_add("C语言", "C语言基础", "C 程序从 main 经预处理、编译、汇编、链接生成 ELF/PE；翻译单元独立编译，链接器解析符号。",
     "GCC/Clang 前端生成 AST→GIMPLE/LLVM IR；CRT 初始化 BSS 后跳转 main。",
     intro="C 是面向过程的系统级语言，理解编译模型与 ABI 是阅读任何 C 代码的基础。",
     mechanism="预处理 #include/#define → 编译器生成 .o → 链接器合并符号与 libc → 加载器映射并执行。",
     workflow="编写 .c/.h → gcc -std=c17 -Wall -O2 → 运行；多文件用 Makefile/CMake。",
     performance="PGO/LTO 跨单元优化；-O2 内联热点函数。",
     security="启用 -fstack-protector、FORTIFY_SOURCE；禁用 gets。",
     case_study="嵌入式 startup.s 设 SP、清 BSS 后跳转 main。",
     configuration="CFLAGS/LDFLAGS；-D 宏；-I/-L 路径。",
     debugging="gdb；Valgrind；ASan -fsanitize=address。",
     comparison="C ABI 最稳定；无 GC/泛型，适合 OS/驱动/FFI。",
     concepts=[("翻译单元", "每 .c 独立编译；static 内部链接。"), ("main 启动", "argc/argv；CRT 初始化。"),
               ("标准版本", "C17/C23；实现扩展需条件编译。"), ("可移植类型", "stdint.h 固定宽度。")],
     pitfalls=[("忽略警告", "-Wall 应视为错误。"), ("头文件定义变量", "多重定义链接错误。"), ("依赖 UB", "有符号溢出可被优化掉。")],
     practices=["CI -Werror", "include guard", "Doxygen API", "stdint 跨平台"],
     references=["ISO C17", "K&R C 程序设计语言", "GCC Manual"])

_add("C语言", "数据类型", "C 类型决定内存布局；sizeof/_Alignof 影响 padding 与序列化。",
     "整数提升与 usual arithmetic conversions；位域布局实现定义。",
     intro="基本类型、指针、数组、结构体与联合构成 C 类型系统；对齐影响性能与硬件访问。",
     mechanism="编译器为类型分配大小对齐；表达式类型由转换规则推导。",
     concepts=[("整数提升", "char/short→int。"), ("指针 decay", "数组名常变 T*。"), ("对齐 padding", "重排字段减空洞。"), ("typedef", "别名非新类型。")],
     pitfalls=[("假设 int 32 位", "用 stdint。"), ("memcpy 含 padding", "逐字段复制。"), ("符号混用", "-1>0U。")])

_add("C语言", "运算符与表达式", "优先级与结合性决定求值；逻辑短路；位运算用于标志位。",
     "除法截断向零；移位≥位宽 UB；volatile 禁止优化重排。",
     concepts=[("优先级", "算术>移位>关系>逻辑。"), ("短路", "&& || 不评估右操作数。"), ("序列点", "同表达式多次改同一对象顺序未指定。"), ("位运算", "掩码与标志。")])

_add("C语言", "流程控制", "if/switch/for/while/do-while；switch 跳转表；goto cleanup 释放资源。",
     "setjmp/longjmp 跳过析构；C23 增强 switch。",
     concepts=[("switch fall-through", "需 break 或注释 intentional。"), ("goto cleanup", "集中释放。"), ("状态机", "enum+switch。"), ("循环不变式", "文档化正确性。")])

_add("C语言", "函数", "原型声明；static 内部；inline/LTO；函数指针回调。",
     "调用约定决定入栈；x86-64 System V 寄存器传参。",
     concepts=[("原型", "无原型调用废弃。"), ("static", "隐藏符号。"), ("函数指针", "qsort 回调。"), ("可变参数", "stdarg.h。")])

_add("C语言", "数组与指针", "a[i] 等价 *(a+i)；restrict 无别名；strict aliasing 规则。",
     "decay：sizeof(array)≠sizeof(pointer)。",
     concepts=[("decay", "数组参数实为指针。"), ("指针算术", "仅同对象数组内。"), ("const 位置", "const T* vs T* const。"), ("void*", "通用指针。")])

_add("C语言", "结构体与联合", "struct 聚合；union 共享存储；位域与柔性数组 FAM。",
     "offsetof；#pragma pack 改变布局。",
     concepts=[("padding", "对齐插入空洞。"), ("union pun", "type punning 用 memcpy。"), ("位域", "实现定义。"), ("FAM", "末尾 [] 变长。")])

_add("C语言", "内存管理", "malloc/calloc/realloc/free；谁分配谁释放；jemalloc/tcmalloc。",
     "ptmalloc arena；mmap 大块；double-free/UAF。",
     concepts=[("堆栈", "栈自动；堆手动。"), ("realloc", "可能移动块。"), ("内存池", "对象复用。"), ("ASan", "检测越界。")])

_add("C语言", "文件IO", "stdio FILE* 与 POSIX fd；缓冲模式；errno。",
     "page cache；O_DIRECT 绕过 cache。",
     concepts=[("stdio", "fread/fwrite 缓冲。"), ("fd", "open/read/write。"), ("errno", "线程局部。"), ("二进制", "endian 处理。")])

_add("C语言", "预处理", "#include/#define/#if；宏词法替换；X 宏。",
     "预编译 .i；#line 保留行号。",
     concepts=[("include", "<> 系统 \"\" 本地。"), ("函数宏", "参数括号保护。"), ("条件编译", "平台分支。"), ("pragma", "once/pack。")])

_add("C语言", "高级特性", "C99/C11/C23：指定初始化、_Generic、stdatomic、threads.h。",
     "_Static_assert 编译期断言。",
     concepts=[("指定初始化", ".field=value。"), ("_Generic", "类型选择。"), ("stdatomic", "memory_order。"), ("C23 #embed", "二进制嵌入。")])

_add("C语言", "C标准库", "stdio/stdlib/string/math；glibc vs musl 差异。",
     "printf 格式；reentrant _r 后缀。",
     concepts=[("stdio.h", "格式化 IO。"), ("stdlib.h", "malloc/exit。"), ("string.h", "str*/mem*。"), ("线程安全", "查 man 表。")])

_add("C语言", "C语言最佳实践", "MISRA/CERT C；模块边界；Unity/CMocka 测试；Coverity。",
     "Linux kernel style；goto cleanup 错误处理。",
     concepts=[("编码规范", "团队一致。"), ("静态分析", "CI cppcheck。"), ("Fuzz", "AFL/libFuzzer。"), ("ADR", "架构决策记录。")])
'''

# Write append script - this is just the C language section
# Full script continues in file

if __name__ == "__main__":
    base = "/workspace/article_generator/manual/_content_specs_languages.py"
    with open(base, "a", encoding="utf-8") as f:
        f.write(SPECS)
    print("Appended C language specs")
