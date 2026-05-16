---
name: comfyui-skill
description: ComfyUI 一键执行器 — 自动配置，零隐私，极省 token
trigger: user says run comfyui, 跑图, process image, upscale
tags: [comfyui, image-processing, low-token, automation]
version: 2.0.0
---

# ComfyUI Skill

由用户上传的 API 格式工作流自动配置，实现 **零浏览器、零 JSON 入上下文** 的 ComfyUI 图片处理。

## 行为模式

### 模式 A：配置工作流（用户主动）

用户发送任意 ComfyUI 工作流的 API 格式导出 JSON 文件，并说「配置工作流」。

Agent 行为：
1. 接收用户上传的 JSON 文件
2. 扫描 JSON，找到 `"class_type": "LoadImage"` 所在的节点 ID
3. 剥离 `_meta` 字段缩小体积
4. 存入 skill 自有目录的 `config.json`，记录：
   - `workflow_path` — 工作流文件路径
   - `load_image_id` — LoadImage 节点 ID
5. 回复：配置完成

**注意事项：**
- 如果 JSON 中找不到 LoadImage 节点，提示用户该工作流没有图片输入节点
- 如果找到多个 LoadImage 节点，让用户指定使用哪一个
- 如果 JSON 中包含 `_meta` / `nodes` / `links` 等字段（标准格式），提示「需要 API 格式导出」
- 引导用户：在 ComfyUI 中点「保存 → 保存（API 格式）」

### 模式 A2：更换工作流

用户发送新的 API 格式 JSON 文件，并说「换工作流」或「切换工作流」。

等同于模式 A，但覆盖已有 `config.json` 文件。

### 模式 B：自动导出工作流（实验性）

用户说「导出工作流」或「帮我配置 ComfyUI」。

Agent 用浏览器访问 ComfyUI，利用前端 API 自动导出并配置：

```
browser_navigate → http://127.0.0.1:8188/
browser_console(expression="JSON.stringify(await app.graphToPrompt().then(r=>r.output))")
```

从 console 输出中提取 API 格式 JSON，存入 config.json。自动检测 LoadImage 节点 ID。

**仅一次 setup 操作可用浏览器模式，后续跑图零浏览器。**

### 模式 C：跑图（日常操作）

用户发送图片，说「跑 ComfyUI」或「跑图」或「处理这张图」。

#### 前置检查
- 如果 `config.json` 不存在，回复「请先导出工作流并发给我配置」
- 如果存在，加载配置进行后续操作

#### 第1步：上传图片
```bash
curl -s -X POST "${comfyui_url}/upload/image" \
  -F "image=@/path/to/img.jpg" -F "overwrite=true"
```

#### 第2步：改图名+提交 Prompt
```bash
"${python}" -c "
import json, requests
d = json.load(open('${workflow_path}'))
d['${load_image_id}']['inputs']['image'] = '${uploaded_name}'
r = requests.post('${comfyui_url}/prompt', json={'prompt': d})
print(f'PID:{r.json().get(\"prompt_id\", \"ERR\")}')
"
```

#### 第3步：等待+取结果
```bash
sleep 300
curl -s ${comfyui_url}/history | "${python}" -c "
import sys,json,os
h=json.load(sys.stdin)
for pid in list(h.keys())[-1:]:
    for out in h[pid].get('outputs',{}).values():
        for img in out.get('images',[]):
            p = '${output_dir}/'+img['filename']
            if os.path.exists(p): print(f'MEDIA:{p}')
"
```

## Token 预算

| 项目 | 传统方案 | 本 skill |
|------|----------|----------|
| 缓存命中 | ~600万 | **≤80万** |
| 未命中 | ~25万 | **≤3万** |
| terminal 调用 | 6-8次 | **3次** |
| 浏览器（日常） | 6-8次DOM | **0** |
| JSON 进上下文 | 33KB-70KB | **0** |

## 故障排查

- **「找不到 LoadImage 节点」** — 工作流可能没有图片输入，或导出格式不对（需 API 格式）
- **「PID:ERR」** — ComfyUI 未运行或端口不对
- **「无输出图片」** — 睡眠时间不够，增大 sleep 值
- **「图片还是原图」** — LoadImage 节点 ID 配置错误，请检查 config.json 中的 load_image_id
- **浏览器导出失败** — ComfyUI 版本可能不支持 `app.graphToPrompt()`，手动导出后发 JSON 给 Agent
