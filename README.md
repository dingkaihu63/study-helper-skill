# 🎓 study-helper-skill

### 终端里的“最强助教”：从海量教材到精编复习指南，只需一个指令。

[](https://www.google.com/search?q=https://github.com/dingkaihu63/study-helper-skill/stargazers)
[](https://www.google.com/search?q=https://www.python.org/)
[](https://www.google.com/search?q=%23)
[](https://www.google.com/search?q=%23)

> **“离考试还有 24 小时，而你面前有 500 页没划重点的 PDF？”**
>
> 别再对着对话框疯狂复制粘贴了。**study-helper-skill** 是一套专为 **Claude Code / OpenClaw / OpenHands** 等顶级 AI Agent 打造的“工程级”复习自动化工具链。它能让你的 AI 助手瞬间化身为“拥有 10 年教学经验的命题组老教授”，为你产出能直接打印进考场的专业复习指南。

-----

## 🔥 核心痛点终结者

市面上 99% 的 AI 总结工具只是简单的“长文缩写”，而本项目彻底解决了 AI 在处理复杂学术资料时的三大“死穴”：

| 传统对话式 AI 的局限 | **study-helper-skill 的降维打击** |
| :--- | :--- |
| ❌ 遇到整本教材直接报错或触发上下文截断 | ✅ **自研智能分块引擎**：无视文件大小，实现全书深度结构化扫描。 |
| ❌ 敷衍的“摘要”，不理会你的实际进度 | ✅ **交互式诊断**：主动询问剩余时间与薄弱点，实现量身定制的考点倾斜。 |
| ❌ 凌乱的终端文本，无法脱离屏幕复用 | ✅ **工业级 `.docx` 产出**：带目录、公式与多级标题的专业排版，一键出图出表。 |

-----

## 🛠️ 三位一体的自动化架构

本项目采用高内聚、低耦合的模块化设计，完美契合 Tool-use 范式。它由三个核心高性能组件构成：

### 1️⃣ 📂 结构化预处理引擎 (`文件预处理.py`)

支持 `PDF` / `DOCX` / `PPT` / `MD` / `HTML` 全格式解析。内置智能 Chunking 算法（默认 50,000 字分块），自动清洗冗余信息，按章节逻辑切分数据，确保 AI 拿到的每一行字都是高密度“干货”。

### 2️⃣ 🧠 专家级思维中枢 (`analyze_summarize.md`)

非通用 Prompt，而是注入了命题逻辑的跨模型专家模板。强制 LLM 按严格的 4 层 Markdown 结构输出，自动建立“前置依赖 -\> 核心定理 -\> 典型避坑”的深度知识网络。

### 3️⃣ 📄 自动化排版重构器 (`资料文件生成.py`)

基于 `python-docx` 的底层渲染引擎。自动处理中英文字体隔离、多级标题嵌套、列表排版。**生成的复习大纲，拿去打印店就能直接印。**

-----

## 🤖 快速接入 (Agent 适配指南)

它不是一个封闭的软件，而是你的 AI 的“物理外挂”。

### 方案 A：Claude Code 原生用户 (开箱即用)

```bash
# 1. 克隆项目并安装依赖
git clone https://github.com/dingkaihu63/study-helper-skill.git
cd study-helper-skill
pip install -r requirements.txt

# 2. 触发工作流
claude skill run study-helper-skill --materials_path="./控制工程基础.pdf" --course_name="自动控制"
```

### 方案 B：OpenClaw / 通用 Agent 开发者

直接将本仓库作为 Tool 挂载，只需给 Agent 下达自然语言指令：

> *"请使用 `文件预处理.py` 读取我桌面的《离散数学.pdf》，然后遵循 `analyze_summarize.md` 的逻辑进行考点梳理，最后调用 `资料文件生成.py` 给我输出一份 Word 文档。"*

### 方案 C：纯 Python 自动化 Pipeline

你完全可以脱离 Agent，将其作为独立的脚本工具链运行（详见代码内部注释）。

-----

## 🛡️ 加入“拯救 GPA 计划”

**study-helper-skill** 不仅仅是一个代码仓库，我们正在发起一场利用技术对抗“无效复习”的运动。我们坚信：**AI 不应替代思考，而应消除那些阻碍思考的低效劳动。**

参与计划：

  * **Star 🌟 本项目**：你的每一次点赞，都是对熬夜学子的一份火力支援！
  * **提交 PR**：欢迎贡献针对特定学科（如：医学、法学、CS底层架构）的专属 Prompt 模板或 OCR 解析模块。
  * **传播火种**：如果它帮你保住了绩点，请把这个项目分享给那个还在手动划重点的室友。

-----

> **“把时间留给深度的逻辑推演，把枯燥的资料整理交给 study-helper-skill。”**

[**🐛 提交 Issue**](https://www.google.com/search?q=https://github.com/dingkaihu63/study-helper-skill/issues) | [**💡 探讨新 Feature**](https://www.google.com/search?q=https://github.com/dingkaihu63/study-helper-skill/pulls)
