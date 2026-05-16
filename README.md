# ComfyUI Skill

> Hermes Agent 的 ComfyUI 极简执行器 — 自动配置，零隐私泄露，3000万token降到百万内

应用场景：本地或服务器同时安装 **Hermes Agent** 和 **ComfyUI** 需远程生图。

Hermes Agent 的 ComfyUI 技能包。把 ComfyUI 工作流执行从 3000 万 token 降到 **百万内，一次生图仅需3分钱**。

## 特性

- **零隐私** — 不包含任何个人路径、模型名、服务器信息
- **自动配置** — 导出 API 工作流发给你的 Hermes，一句话搞定
- **极省 token** — 单图 ≤80万缓存命中、≤3万未命中
- **零浏览器** — 日常跑图全程 terminal，不碰前端 DOM
- **可换工作流** — 随时发新的 API 工作流 JSON 切换

## 安装

```bash
hermes skills install https://github.com/xixinw/comfyui-skill
```

## 快速开始

### 第1步：导出工作流

在 ComfyUI 加载你的工作流，点击 **保存 → 保存（API 格式）**，得到一个 JSON 文件。

### 第2步：配置 Hermes

把导出的 JSON 文件发给你的 Hermes Agent，说：

> 「配置工作流」

Agent 会自动检测 LoadImage 节点、剥离冗余数据、保存配置。全程 < 1秒。

或者直接说：**「使用此API格式工作流配置生图」**

### 第3步：开始使用

发送图片给你的 Hermes，说：

> 「跑 ComfyUI」或「处理这张图」

等待几分钟，拿到结果。

### 更换工作流

导出新的 JSON 发给 Hermes，说：

> 「换工作流」

## 自动导出（实验性）

如果你的 Hermes 能访问 ComfyUI 的 Web 界面，直接说：

> 「导出工作流」

Hermes 会自动打开 ComfyUI、导出当前工作流、完成配置。

## 原理

详见 [SKILL.md](SKILL.md)。

## Token 节省效果

| | 传统做法 | 本 skill |
|---|---|---|
| 缓存命中 token | ~600万 | **≤80万** |
| 未命中 token | ~25万 | **≤3万** |
| 日常跑图浏览器 | 6-8次 | **0次** |
| 配置方式 | 手动改代码 | **发 JSON 一句话** |

## License

MIT
