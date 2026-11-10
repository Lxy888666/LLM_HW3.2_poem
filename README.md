# 唐诗宋词英译提示设计实验

本项目考察不同提示设计对唐诗宋词英译的影响，并检验开发阶段选定的提示能否用于未参与提示选择的作品。

## 项目结构

- `report/poetry_translation_report.md`：实验报告。
- `src/run_experiment.py`：实验运行脚本。
- `data/development_outputs.jsonl`、`data/test_outputs.jsonl`：开发集和测试集的原文、提示及译文记录。
- `data/development_meta.json`、`data/test_meta.json`：运行阶段、模型及生成参数等元数据。

## 运行环境

- Python 3.10 或更高版本。
- 可调用 Chat Completions 接口的 API 密钥。
- 脚本仅使用 Python 标准库，无需安装额外依赖。

PowerShell 示例：

```powershell
$env:DEEPSEEK_API_KEY = "<你的API密钥>"
$env:DEEPSEEK_BASE_URL = "https://api.deepseek.com"
$env:DEEPSEEK_MODEL = "deepseek-flash"
```

## 运行实验

在项目根目录执行：

```powershell
python .\src\run_experiment.py --stage development
python .\src\run_experiment.py --stage test --condition P1_task_standard
```

开发集用于比较提示版本并选定方案；测试集仅用于检验选定方案在新作品上的表现。本实验在开发阶段后锁定 P1，因此测试阶段应使用 `P1_task_standard`。
