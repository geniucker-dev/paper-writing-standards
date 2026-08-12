# paper-writing-standards

一个跨 agent 通用的 Agent Skill，把一套具体的论文写作规范变成可执行的起草流程和自检清单。

规范内容来自《论文注意事项与写法要点》与「5W 法阅读及写作法」，覆盖两块：**写作中常见的一些问题**（术语与符号、句式、实验主线、图表公式）和**结构分节与写法要点**（Abstract 到 Reference 八节）。

Skill 本体是纯 Markdown + 标准库 Python，不依赖任何特定 agent 的私有格式，Cursor、Codex CLI、Claude Code 都能直接读。

Skill 内容为英文（模型读英文更省 token 也更准），但描述里带了中文触发词，用中文提问照样能命中，回复语言跟随你的提问语言。

## 能做什么

**起草模式** — 给它想法、实验结果或草稿，它先定位这一节在 5W 中的位置，列出每段主题句让你确认骨架，再按分节要点填充成文。

**自检模式** — 给它已有稿件，它先判断最致命的问题在哪，跑机械检查，再对照高频错误表和分节要点逐条过，最后输出带「可直接替换句子」的问题清单。

## 目录结构

```
paper-writing-standards/
├── SKILL.md                        # 入口：模式判定、四条主线、两种模式的工作流、终检清单
├── references/
│   ├── common-pitfalls.md          # 写作中常见的一些问题 + 常见高频错误对照表
│   ├── section-guide.md            # 八个章节的分节写法要点
│   └── 5w-framework.md             # 5W 法 + Contribution 的三段写法
├── scripts/
│   └── audit_manuscript.py         # 机械自检脚本（仅标准库）
└── assets/                         # 规范原图
```

`SKILL.md` 只放每次都要用到的内容，细则按需从 `references/` 读取。

## 安装

克隆到本地后，把整个目录放进（或软链到）对应 agent 的 skills 目录：

```bash
git clone https://github.com/GaAs9000/paper-writing-standards.git

# Cursor
ln -s "$PWD/paper-writing-standards" ~/.cursor/skills/paper-writing-standards

# Codex CLI
ln -s "$PWD/paper-writing-standards" ~/.codex/skills/paper-writing-standards

# Claude Code
ln -s "$PWD/paper-writing-standards" ~/.claude/skills/paper-writing-standards
```

目录不存在时先 `mkdir -p`。用软链的好处是三端共用同一份，`git pull` 一次全部更新。

若某个 agent 已经能读取其它 agent 的 skills 目录，只装一处即可，重复安装会出现同名条目。

不想装也可以直接用：把 `SKILL.md` 的内容贴进对话，或让 agent 读取仓库里的文件。

## 使用

装好后正常提要求即可，agent 会自动匹配：

```
帮我按论文规范检查一下 intro.tex
这段实验结果帮我写成 Experiments 小节
我的 contribution 这么写行吗
投稿前帮我过一遍全文
```

也可以显式点名：`用 paper-writing-standards 检查 paper.tex`。

## 机械自检脚本

```bash
python3 scripts/audit_manuscript.py paper.tex
python3 scripts/audit_manuscript.py paper.tex --topic-sentences
python3 scripts/audit_manuscript.py paper.tex --terms "power grid=power network"
python3 scripts/audit_manuscript.py paper.tex --json
```

支持 `.tex` / `.md` / `.txt`，中英文混排，只依赖 Python 3.9+ 标准库。会自动跳过 LaTeX 注释、公式环境、`\cite` 与 `\ref`。

| 检查 | 说明 |
| --- | --- |
| 未解释的缩写 | 首次出现处没有全称或括号定义 |
| 术语不统一 | 同一概念出现多种写法，内置 13 组常见混用，可用 `--terms` 追加 |
| 句子过长 | 英文超过 40 词 / 中文超过 90 字 |
| 逗号连串 | 英文 3 个以上 / 中文 4 个以上 |
| 从句过多 | 3 处以上从句引导词 |
| 绝对化措辞 | the key、the only、for the first time、首次提出 等 |
| 正文中的数学符号 | 独立出现的 `+` `&` `=` |
| 图表公式编号顺序 | 首次引用顺序是否为 1, 2, 3… |
| 无统计支撑的「显著」 | 同句没有 p 值或置信区间 |
| 连接词过度使用 | 按全文词数给预算 |

参数：`--ignore` 跳过指定缩写，`--strict` 有问题时退出码为 1（便于接 CI 或 pre-commit）。

脚本只报候选，不做判断——它不知道哪些缩写在你的领域属于常识，也不知道某个长句是否确有必要。**贡献是否空泛、有没有强基线、讨论是否讲清机制、图注能否独立阅读，这些必须人工或由模型对照 `references/` 核对。**

## 与其它写作 skill 的关系

这是一套独立、自成体系的规范，不引用也不依赖其它 skill。如果你同时装了通用的润色或作图类 skill，本 skill 的规则优先级更高——它是具体课题组的成文要求，不是通用建议。

## License

MIT
