# -*- coding: utf-8 -*-
"""领域相关代码示例生成"""

from typing import Optional

# 领域专属代码模板
DOMAIN_CODE = {
    "React": {
        "default": '''import { useState, useEffect } from 'react';

function App() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      点击次数: {count}
    </button>
  );
}

export default App;''',
        "Hooks": '''import { useState, useCallback } from 'react';

function useCounter(initial = 0) {
  const [count, setCount] = useState(initial);
  const increment = useCallback(() => setCount(c => c + 1), []);
  const decrement = useCallback(() => setCount(c => c - 1), []);
  return { count, increment, decrement };
}''',
        "useEffect": '''useEffect(() => {
  const controller = new AbortController();
  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(setData);
  return () => controller.abort(); // 清理：取消请求
}, []);''',
    },
    "Vue": {
        "default": '''<script setup>
import { ref, computed } from 'vue';

const count = ref(0);
const doubled = computed(() => count.value * 2);
</script>

<template>
  <button @click="count++">{{ count }} / {{ doubled }}</button>
</template>''',
    },
    "Flask": {
        "default": '''from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def list_users():
    page = request.args.get('page', 1, type=int)
    return jsonify({"page": page, "users": []})

if __name__ == '__main__':
    app.run(debug=True)''',
        "路由": '''@app.route('/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post_detail(post_id):
  if request.method == 'GET':
      return jsonify({"id": post_id})
  # PUT / DELETE 分支...''',
        "蓝图": '''from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/health')
def health():
    return {'status': 'ok'}

app.register_blueprint(api)''',
    },
    "Docker": {
        "default": '''# Dockerfile 多阶段构建示例
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html''',
    },
    "Kubernetes": {
        "default": '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx:1.25
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"''',
    },
    "Go语言": {
        "default": '''package main

import (
    "context"
    "fmt"
    "time"
)

func worker(ctx context.Context, id int, jobs <-chan int, results chan<- int) {
    for {
        select {
        case job := <-jobs:
            results <- job * 2
        case <-ctx.Done():
            fmt.Printf("worker %d stopped\n", id)
            return
        }
    }
}''',
        "goroutine": '''func main() {
    ch := make(chan string)
    go func() { ch <- "hello" }()
    fmt.Println(<-ch)
}''',
        "channel": '''ch := make(chan int, 10) // 有缓冲 channel
go func() {
    for i := 0; i < 5; i++ {
        ch <- i
    }
    close(ch)
}
for v := range ch {
    fmt.Println(v)
}''',
    },
    "Rust语言": {
        "default": '''use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..4 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("{}", *counter.lock().unwrap());
}''',
        "所有权": '''let s1 = String::from("hello");
let s2 = s1; // s1 所有权转移，s1 不再有效
// let s3 = s1; // 编译错误''',
    },
    "Python核心": {
        "default": '''from dataclasses import dataclass
from typing import List

@dataclass
class User:
    name: str
    tags: List[str]

def filter_users(users: List[User], keyword: str) -> List[User]:
    return [u for u in users if keyword in u.name]''',
    },
    "Spring Boot": {
        "default": '''@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public UserDTO getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}''',
    },
    "Redis": {
        "default": '''import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 缓存穿透防护：空值缓存 + 过期时间
def get_user(user_id: str):
    key = f"user:{user_id}"
    cached = r.get(key)
    if cached is not None:
        return cached if cached != "NULL" else None
    user = db.query(user_id)
    r.setex(key, 300, user or "NULL")
    return user''',
    },
    "MySQL": {
        "default": '''-- 覆盖索引避免回表
CREATE INDEX idx_orders_user_created
ON orders(user_id, created_at, status);

SELECT status, created_at
FROM orders
WHERE user_id = 1001
ORDER BY created_at DESC
LIMIT 20;''',
    },
    "TypeScript": {
        "default": '''interface ApiResponse<T> {
  data: T;
  code: number;
  message: string;
}

async function fetchUser(id: number): Promise<ApiResponse<User>> {
  const res = await fetch(`/api/users/${id}`);
  return res.json() as Promise<ApiResponse<User>>;
}''',
    },
    "Node.js": {
        "default": '''const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok' }));
    return;
  }
  res.writeHead(404);
  res.end();
});

server.listen(3000);''',
    },
    "大语言模型": {
        "default": '''from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype="auto", device_map="auto"
)

inputs = tokenizer("Hello, how are", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))''',
    },
    "Git版本控制": {
        "default": '''# 功能分支工作流
git checkout -b feature/user-auth
git add .
git commit -m "feat: add JWT authentication"
git push -u origin feature/user-auth
# 通过 PR 合并到 main 分支''',
    },
    "Nginx": {
        "default": '''upstream backend {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}''',
    },
}

LANG_MAP = {
    "React": "tsx", "Vue": "vue", "Flask": "python", "Django": "python",
    "Python核心": "python", "Python高级": "python", "Go语言": "go",
    "Rust语言": "rust", "Rust系统编程": "rust", "Java核心": "java",
    "Spring Boot": "java", "TypeScript": "typescript", "Node.js": "javascript",
    "Docker": "dockerfile", "Kubernetes": "yaml", "Redis": "python",
    "MySQL": "sql", "PostgreSQL": "sql", "Nginx": "nginx",
    "Git版本控制": "bash", "大语言模型": "python", "机器学习": "python",
    "深度学习": "python", "C语言": "c", "C++": "cpp", "C#": "csharp",
    "PHP": "php", "GraphQL": "graphql", "HTML与CSS": "html",
}


def get_lang(domain: str) -> str:
    return LANG_MAP.get(domain, "text")


def get_code(domain: str, module: str, pattern_type: str) -> tuple[str, str]:
    """返回 (语言, 代码)"""
    domain_codes = DOMAIN_CODE.get(domain, {})
    # 优先模块匹配
    for key in [module, "default"]:
        if key in domain_codes:
            code = domain_codes[key]
            return get_lang(domain), code

    # 通用回退
    lang = get_lang(domain)
    generic = f'''// {domain} - {module} 示例
// 模式: {pattern_type}
// 参考官方文档实现核心逻辑

function example() {{
  // 1. 初始化配置
  // 2. 执行 {module} 核心流程
  // 3. 处理结果与异常
  return {{ success: true }};
}}'''
    if lang == "python":
        generic = f'''# {domain} - {module} 示例
def process():
    """{module} 核心处理流程"""
    config = load_config()
    result = execute_core_logic(config)
    return validate_result(result)'''
    elif lang == "go":
        generic = f'''// {domain} - {module}
func Process(ctx context.Context) error {{
    cfg, err := LoadConfig()
    if err != nil {{ return err }}
    return Execute(ctx, cfg)
}}'''
    elif lang == "rust":
        generic = f'''// {domain} - {module}
pub fn process(input: &str) -> Result<String, Box<dyn std::error::Error>> {{
    let validated = validate(input)?;
    Ok(transform(validated))
}}'''
    elif lang == "sql":
        generic = f'''-- {domain}: {module}
SELECT id, name, status
FROM resources
WHERE status = 'active'
ORDER BY created_at DESC
LIMIT 100;'''
    elif lang == "yaml":
        generic = DOMAIN_CODE.get("Kubernetes", {}).get("default", generic)
        lang = "yaml"
    return lang, generic


def get_config_example(domain: str, module: str) -> tuple[str, str]:
    """配置类示例"""
    configs = {
        "Docker": ("yaml", '''version: "3.9"
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    deploy:
      resources:
        limits:
          cpus: "1"
          memory: 512M'''),
        "Kubernetes": ("yaml", DOMAIN_CODE["Kubernetes"]["default"]),
        "Nginx": ("nginx", DOMAIN_CODE["Nginx"]["default"]),
        "TypeScript": ("json", '''{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "strict": true,
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "skipLibCheck": true
  },
  "include": ["src"]
}'''),
        "CI与CD": ("yaml", '''name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test'''),
    }
    if domain in configs:
        return configs[domain]
    lang, code = get_code(domain, module, "configuration")
    return lang, f"# {domain} {module} 配置示例\n{code}"
