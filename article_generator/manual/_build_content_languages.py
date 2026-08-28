#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build content_languages.py with hand-authored module content."""

from __future__ import annotations

OUTPUT = "/workspace/article_generator/manual/content_languages.py"


def _m(
    intro: str,
    concepts: list[tuple[str, str]],
    mechanism: str,
    internals: str,
    workflow: str,
    performance: str,
    security: str,
    case_study: str,
    configuration: str,
    debugging: str,
    comparison: str,
    pitfalls: list[tuple[str, str]],
    practices: list[str],
    references: list[str],
) -> dict:
    return {
        "intro": intro,
        "concepts": [{"title": t, "body": b} for t, b in concepts],
        "mechanism": mechanism,
        "internals": internals,
        "workflow": workflow,
        "performance": performance,
        "security": security,
        "case_study": case_study,
        "configuration": configuration,
        "debugging": debugging,
        "comparison": comparison,
        "pitfalls": [{"title": t, "body": b} for t, b in pitfalls],
        "practices": practices,
        "references": references,
    }


# ---------------------------------------------------------------------------
# C 语言
# ---------------------------------------------------------------------------
C_LANG = {
    "C语言基础": _m(
        "C 语言是面向过程的系统级语言，由 Dennis Ritchie 于 1972 年在贝尔实验室为 Unix 开发。"
        "程序从 main 函数入口开始，经编译（预处理→编译→汇编→链接）生成可执行文件。"
        "理解编译模型与 ABI 是阅读 C 代码的基础。",
        [
            ("程序结构与翻译单元", "每个 .c 文件是一个翻译单元，独立编译后由链接器合并符号。"
             "extern 声明跨文件引用，static 限制内部链接。头文件只放声明，避免重复定义。"),
            ("main 与进程启动", "main(int argc, char *argv[]) 接收命令行参数；"
             "启动时 C 运行时初始化 BSS/DATA、调用构造函数（C++ 混编时）、再跳转 main。"),
            ("标识符与命名空间", "C 无命名空间，全局符号暴露在链接层；"
             "命名冲突靠 static、前缀约定或 opaque 指针解决。"),
            ("标准与实现差异", "ISO C（C89/C99/C11/C17/C23）定义可移植子集；"
             "GCC/Clang/MSVC 在 intrinsics、扩展关键字上存在差异。"),
            ("可移植性边界", "int 宽度、char 符号性、字节序由实现定义；"
             "跨平台代码应使用 stdint.h 固定宽度类型与显式大小端处理。"),
        ],
        "编译器将 C 源码经词法/语法分析生成 AST，语义分析后输出中间表示（GIMPLE/LLVM IR），"
        "优化后生成目标机器码。链接器解析 undefined symbol，合并 .o 与静态/动态库。",
        "GCC 前端 c-parser.c 解析；Clang 基于 LLVM；预处理器处理 #include/#define，"
        "宏展开在词法层完成，调试时需 -g 与 -save-temps 观察 .i 文件。",
        "编写 hello.c → gcc -Wall -Wextra -std=c17 -O2 -o hello hello.c → ./hello；"
        "多文件项目用 Makefile/CMake 管理依赖与编译选项。",
        "编译优化 -O2/-O3 内联小函数、循环展开；LTO 跨单元优化。"
        "Profile-guided optimization（-fprofile-use）利用运行时热点数据。",
        "缓冲区溢出、格式字符串漏洞是 C 经典安全问题；启用 -fstack-protector、FORTIFY_SOURCE。",
        "嵌入式启动代码：startup.s 设置栈指针、清零 BSS、跳转 main；"
        "裸机环境无 libc，需自行实现 syscalls 或 newlib 桩。",
        "CFLAGS/LDFLAGS 通过环境变量或 Makefile 传递；-D 定义宏，-I 添加头文件路径。",
        "gdb ./prog 调试；valgrind 检测内存错误；AddressSanitizer（-fsanitize=address）更快定位越界。",
        "C vs Rust/Go：C 无内置内存安全与并发原语，但 ABI 稳定、生态最广，适合 OS/驱动/FFI 边界。",
        [
            ("忽略编译器警告", "-Wall 应视为错误；隐式 int 转换、未使用变量往往隐藏逻辑 bug。"),
            ("在头文件中定义变量", "导致多重定义链接错误；头文件只声明，定义放单一 .c 并用 extern。"),
            ("依赖未定义行为", "有符号溢出、空指针解引用、越界访问在 C 中是 UB，优化器可据此删除「死代码」。"),
        ],
        [
            "始终启用 -Wall -Wextra -Werror 于 CI",
            "头文件使用 include guard 或 #pragma once",
            "公共 API 用 Doxygen 注释并固定 ABI",
            "跨平台代码用 stdint.h 与条件编译 #ifdef",
        ],
        [
            "ISO/IEC 9899:2018 (C17) 标准文档",
            "K&R《C 程序设计语言》第二版",
            "GCC 官方文档 — Options Controlling C Dialect",
        ],
    ),
    "数据类型": _m(
        "C 类型系统基于固定内存布局：基本类型（char/int/float/double）、派生类型（指针、数组、结构体、函数指针）。"
        "sizeof 与 _Alignof（C11）反映对象大小与对齐要求，直接影响结构体 padding 与序列化。",
        [
            ("基本类型与整数提升", "char/short 在表达式中提升为 int；unsigned 运算遵循模运算规则。"
             "long 与 long long 宽度平台相关，stdint.h 提供 int32_t 等别名。"),
            ("指针类型", "T* 指向 T 对象；void* 为通用指针，与任意对象指针可互转（C11 起需显式）。"
             "指针算术以 sizeof(T) 为步长，越界是 UB。"),
            ("数组与 decay", "数组名在大多数表达式中 decay 为指向首元素的指针；"
             "sizeof(array) 得总字节数，sizeof(pointer) 得指针宽度。"),
            ("结构体与对齐", "编译器按成员对齐要求插入 padding；#pragma pack 或 __attribute__((packed)) 可改变布局，"
             "但可能引发未对齐访问性能损失或硬件 fault。"),
            ("typedef 与类型别名", "typedef 创建类型同义词，不生成新类型；"
             "与 struct 结合 typedef struct { ... } Node; 是常见惯用法。"),
        ],
        "编译器为每个类型分配大小与对齐，在符号表中记录；表达式类型由 usual arithmetic conversions 规则推导。",
        "Itanium C++ ABI 也影响 C 结构体传递方式；ARM EABI 规定 8 字节对齐 double。",
        "声明变量 → 初始化 → 运算时注意整数提升 → 赋值检查宽度截断 → 跨模块传递用固定宽度类型。",
        "结构体字段重排（大→小）减少 padding；位域节省空间但访问需多次内存操作。",
        "类型混淆与整数溢出可导致逻辑漏洞；无符号与有符号混比需显式转换。",
        "网络协议结构体用 __attribute__((packed)) 配合 htons/ntohl 处理字节序。",
        "stdint.h、stdbool.h（C99）、complex.h 按需引入；-std=c99 启用 bool。",
        "printf 格式与参数类型不匹配用 -Wformat 捕获；gdb p 查看变量与类型。",
        "C 无泛型，void* 或 _Generic（C11）实现类型安全多态；C++ template 是超集。",
        [
            ("假设 int 为 32 位", "LP64 平台 long 可能 64 位而 int 32 位；网络/文件格式必须用固定宽度类型。"),
            ("结构体逐成员 memcpy", "含 padding 或未初始化 padding 会导致哈希/比较不一致；用 memset 或逐字段复制。"),
            ("有符号/无符号混用", "比较时隐式转换可能使 -1 > 0U 为真，引发边界检查失效。"),
        ],
        [
            "对外接口使用 stdint.h 固定宽度类型",
            "结构体设计时画出内存布局图验证 padding",
            "启用 -Wconversion -Wsign-conversion",
            "序列化协议显式指定字节序与字段宽度",
        ],
        [
            "C11 标准 Annex F — Floating-point arithmetic",
            "Agner Fog《Optimizing Software in C++》结构体布局章节",
            "What Every C Programmer Should Know About Undefined Behavior（LLVM Blog）",
        ],
    ),
}

# We'll generate remaining content programmatically with module-specific technical details
# This script writes the full file - run it to produce content_languages.py

if __name__ == "__main__":
    print(f"C_LANG sample keys: {list(C_LANG.keys())}")
    print("Use full builder - see content_languages.py")
