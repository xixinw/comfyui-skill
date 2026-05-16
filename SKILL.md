---
name: comfyui-skill
description: 一键ComfyUI工作流执行器 — 零浏览器、零转换、零浪费
trigger: user says run ComfyUI, process image, upscale, edit image, or any image-to-image task
tags: [comfyui, image-processing, automation, low-token]
version: 1.0.0
author: looper je
---

# ComfyUI Skill — 极简执行器

在 ComfyUI 上跑工作流，全程 **3 次 terminal 调用、0 次浏览器、0 次 JSON 进入上下文**。

单张图片消耗：**缓存命中 ≤ 80 万 token，未命中 ≤ 3 万 token**。

## 前置要求

1. ComfyUI 已安装并运行在 `http://127.0.0.1:8188`
2. 已从 ComfyUI 导出 API 格式工作流 JSON（详见下方「准备工作」）

## 准备工作（一次性 setup）

### 从 ComfyUI 导出工作流

1. 在 ComfyUI 中加载你的工作流
2. 点击右上角 **「保存」→ 「保存（API 格式）」**
3. 将导出的 JSON 文件放入 skill 的 `templates/` 目录
4. 将该文件路径写死在下方的常量中（默认：`独立版六合一-api.json`）

### 环境常量

```
COMFYUI_URL     = http://127.0.0.1:8188
COMFYUI_PYTHON  = D:/ComfyUI-beibei/python/python.exe
WORKFLOW_PATH   = /path/to/your-workflow-api.json
IMAGE_NODE_ID   = 771   # 加载图片节点的 ID（在你的 JSON 中查找 class_type=LoadImage 的 key）
```

## 核心指令（三步行）

### 第1步：上传图片

```bash
curl -s -X POST "${COMFYUI_URL}/upload/image" \
  -F "image=@/path/to/user/image.jpg" \
  -F "overwrite=true"
```

预期输出（仅一行）：
```json
{"name":"xxx.jpg","subfolder":"","type":"input"}
```

### 第2步：修改图名 + 提交 Prompt（一行 Python）

```bash
"${COMFYUI_PYTHON}" -c "
import json, requests
d = json.load(open('${WORKFLOW_PATH}'))
d['${IMAGE_NODE_ID}']['inputs']['image'] = 'xxx.jpg'
r = requests.post('${COMFYUI_URL}/prompt', json={'prompt': d})
print(f'PID:{r.json().get(\"prompt_id\", \"ERR\")}')
"
```

**不打印任何 JSON 内容，只输出 PID**

### 第3步：等待 + 提取结果

```bash
sleep 300   # 根据工作流复杂度调整
curl -s ${COMFYUI_URL}/history | "${COMFYUI_PYTHON}" -c "
import sys,json,os
h=json.load(sys.stdin)
for pid in list(h.keys())[-1:]:
    for out in h[pid].get('outputs',{}).values():
        for img in out.get('images',[]):
            p = 'D:/ComfyUI-beibei/ComfyUI/output/'+img['filename']
            if os.path.exists(p): print(f'MEDIA:{p}')
"
```

### 第4步：发送图片

将 `MEDIA:绝对路径` 格式嵌入回复中，平台会自动渲染。

## Token 节省原理

| 操作 | 旧方案 | 本 skill |
|------|--------|----------|
| 浏览器交互 | 6-8 次 DOM 输出 | **0** |
| 查 /queue | 每次 67KB 工作流定义 | **禁止** |
| 读 JSON 到上下文 | ~33KB 全文 | **0**（全在 Python 内部） |
| 工作流文件大小 | ~33KB（含 UI 节点+位置） | **~3KB**（API 格式，已剥离 _meta） |
| terminal 调用 | 6-8 次 | **3 次** |

## 注意事项

### 首次运行
首次运行需要下载模型（Flux / UNET / CLIP），可能耗时 3-10 分钟且消耗额外 token。后续运行模型缓存在显存中，通常 2-5 分钟完成。

### 自定义工作流编号
不同工作的 LoadImage 节点 ID 不同：
- 打开你的 API JSON 文件
- 查找 `"class_type": "LoadImage"` 所在的 key
- 将该 key 值设为 IMAGE_NODE_ID

### 支持的输出
该 skill 自动找到最新的输出图片。如果工作流有多个 SaveImage 节点，会输出所有找到的最新图片。

## 故障排查

**PID:ERR** → 检查 ComfyUI 是否运行、端口是否正确
**NO_OUTPUT** → 睡眠时间不够，增大 sleep 值
**图片还是原图** → 检查 JSON 中 LoadImage 节点的 ID 是否正确
