#!/usr/bin/env python3
"""
ComfyUI Skill — 一键初始化工具

1. 从 ComfyUI 工作流目录中找到所有可用的工作流
2. 让用户选择要绑定的工作流
3. 导出 API 格式并写入 templates/
4. 检测 LoadImage 节点 ID
"""

import json, os, shutil, sys

COMFYUI_WORKFLOWS_DIR = os.path.expanduser(
    "~/D:/ComfyUI-beibei/ComfyUI/user/default/workflows"
)
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(SKILL_DIR, "templates")


def find_workflows():
    """查找 ComfyUI 工作流目录下的 .json 文件"""
    if not os.path.isdir(COMFYUI_WORKFLOWS_DIR):
        print(f"✗ ComfyUI 工作流目录不存在: {COMFYUI_WORKFLOWS_DIR}")
        print(" 请修改脚本顶部的 COMFYUI_WORKFLOWS_DIR 路径")
        sys.exit(1)

    files = [f for f in os.listdir(COMFYUI_WORKFLOWS_DIR) if f.endswith(".json")]
    return sorted(files)


def is_api_format(data):
    """判断 JSON 是否是 API 格式（key 为节点 ID 字符串）"""
    if not isinstance(data, dict):
        return False
    for k, v in data.items():
        if isinstance(v, dict) and "class_type" in v and "inputs" in v:
            return True
    return False


def find_load_image_id(data):
    """查找 LoadImage 节点的 ID"""
    for nid, node in data.items():
        if node.get("class_type") == "LoadImage":
            return nid
    return None


def strip_meta(data):
    """剥离 _meta 字段以减少文件大小"""
    for node in data.values():
        node.pop("_meta", None)
    return data


def main():
    print("=" * 50)
    print("  ComfyUI Skill — 初始化工具")
    print("=" * 50)

    workflows = find_workflows()
    if not workflows:
        print("✗ 未找到工作流文件")
        sys.exit(1)

    print(f"\n找到 {len(workflows)} 个工作流:\n")
    for i, wf in enumerate(workflows, 1):
        fpath = os.path.join(COMFYUI_WORKFLOWS_DIR, wf)
        size = os.path.getsize(fpath)
        print(f"  [{i}] {wf} ({size/1024:.1f} KB)")

    try:
        choice = int(input("\n选择要绑定的工作流编号: ")) - 1
        selected = workflows[choice]
    except (ValueError, IndexError):
        print("✗ 无效选择")
        sys.exit(1)

    src = os.path.join(COMFYUI_WORKFLOWS_DIR, selected)
    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 检查格式
    if is_api_format(data):
        print("✓ 已经是 API 格式，直接使用")
    else:
        print("! 检测到标准格式（含位置/UI 数据）")
        print("  请手动从 ComfyUI 导出 API 格式:")
        print("    保存 → 保存（API 格式）")
        sys.exit(1)

    # 查找 LoadImage 节点
    img_id = find_load_image_id(data)
    if img_id:
        print(f"✓ LoadImage 节点 ID: {img_id}")
    else:
        print("! 未找到 LoadImage 节点，请手动设置 IMAGE_NODE_ID")

    # 剥离 _meta
    data = strip_meta(data)
    cleaned = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    # 写入模板
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    dst = os.path.join(TEMPLATES_DIR, f"{os.path.splitext(selected)[0]}-api.json")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"✓ 已保存: {dst} ({len(cleaned)/1024:.1f} KB)")
    print(f"\n{'='*50}")
    print(f"  完成！请更新 SKILL.md 中的以下常量:")
    print(f"    WORKFLOW_PATH = {dst}")
    if img_id:
        print(f"    IMAGE_NODE_ID = {img_id}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
