# ComfyUI Skill 🎨

> 零浏览器、零转换、零浪费 — 3 次 terminal 调用跑完一张图

应用场景：本地或服务器同时安装**Hermes Agent**和**ComfyUI** 需远程生图

Hermes Agent 的 ComfyUI 技能包。把 ComfyUI 工作流执行从 3000 万 token 降到 **百万内 一次生图仅需3分钱**。

## 效果对比

| | 传统做法 | 本 skill |
|---|---|---|
| 浏览器操作 | 6-8 次 DOM 读取 | **0** |
| JSON 进入上下文 | ~33KB (全文) | **0** |
| terminal 调用 | 6-8 次 | **3 次** |
| 缓存命中 token | ~600 万 | **≤80 万** |
| 未命中 token | ~25 万 | **≤3 万** |

## 安装

```bash
# 从 GitHub 安装
hermes skill install https://github.com/<your-username>/comfyui-skill

# 或本地安装
git clone https://github.com/<your-username>/comfyui-skill.git
hermes skill install ./comfyui-skill
```

## 使用

发送图片给 Hermes，然后说「跑 ComfyUI」即可。

自动加载 `独立版六合一` 工作流，处理完成后返回结果图片。

## 前置要求

- ComfyUI 已安装并运行（默认端口 8188）
- 已从 ComfyUI 导出 API 格式的工作流 JSON

### 如何导出工作流

1. 在 ComfyUI 加载你的工作流
2. 点击右上角 **保存 → 保存（API 格式）**
3. 将导出的 JSON 放入 `templates/` 目录
4. 修改 SKILL.md 中的 `WORKFLOW_PATH` 路径

## 自定义

### 切换工作流

将你的 API 格式工作流放入 `templates/`，然后更新 SKILL.md 中的路径和 `IMAGE_NODE_ID`。

### 查找 LoadImage 节点 ID

```bash
grep -A2 '"LoadImage"' your-workflow-api.json
# 输出上一行的 key 就是节点 ID
```

## 原理

详见 [SKILL.md](SKILL.md)。

## License

MIT
