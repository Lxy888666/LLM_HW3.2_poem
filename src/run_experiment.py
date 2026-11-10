# -*- coding: utf-8 -*-
"""Run the fixed development/test split for the Tang/Song poetry study."""
from __future__ import annotations

import json
import argparse
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-flash")
API_KEY = os.environ.get("DEEPSEEK_API_KEY")

DEV_IDS = {
    "01_xiangsi", "03_fengqiaoyebo", "04_zengbie", "05_jingyesi",
    "06_chunwang", "09_dingfengbo",
}

POEMS = [
    {
        "id": "01_xiangsi", "title": "相思", "author": "王维", "dynasty": "唐",
        "text": "红豆生南国，春来发几枝。\n愿君多采撷，此物最相思。",
        "notes": "红豆是相思意象；诗中没有明确说明具体恋爱故事。",
        "checks": "保留红豆、春天生长、采摘以及相思之间的关系；不要把红豆解释成普通食物。",
        "focus": "红豆的相思意象与赠予关系",
    },
    {
        "id": "02_dengguanquelou", "title": "登鹳雀楼", "author": "王之涣", "dynasty": "唐",
        "text": "白日依山尽，黄河入海流。\n欲穷千里目，更上一层楼。",
        "notes": "前两句写远景，后两句由登楼视野引出继续登高的愿望。",
        "checks": "保留夕阳依山而尽、黄河入海、想看尽千里景色以及再登一层楼的逻辑；不要把后两句改成泛泛的成功格言。",
        "focus": "远景、登楼和“更上一层楼”的逻辑",
    },
    {
        "id": "03_fengqiaoyebo", "title": "枫桥夜泊", "author": "张继", "dynasty": "唐",
        "text": "月落乌啼霜满天，江枫渔火对愁眠。\n姑苏城外寒山寺，夜半钟声到客船。",
        "notes": "姑苏、寒山寺为地名或专名；诗写夜泊客船时所见所闻。",
        "checks": "保留月落、乌啼、霜、江边枫树、渔火、愁眠、寒山寺和半夜钟声传到客船的关系；不要补写未经原文支持的旅行经历。",
        "focus": "夜泊场景、地名和声音意象",
    },
    {
        "id": "04_zengbie", "title": "赠别二首·其二", "author": "杜牧", "dynasty": "唐",
        "text": "多情却似总无情，唯觉尊前笑不成。\n蜡烛有心还惜别，替人垂泪到天明。",
        "notes": "全诗写离别时深情反而显得冷淡、想笑却笑不出来，以及蜡烛替人流泪的拟人意象。",
        "checks": "“似无情”不能译成真正没有感情；“笑不成”是想笑而不能笑；蜡烛要保留替人垂泪的拟人关系。",
        "focus": "情感反差、无法成笑和蜡烛拟人",
    },
    {
        "id": "05_jingyesi", "title": "静夜思", "author": "李白", "dynasty": "唐",
        "text": "床前明月光，疑是地上霜。\n举头望明月，低头思故乡。",
        "notes": "诗以月光、霜的错觉和抬头低头的动作表达思乡。",
        "checks": "保留月光被误认为霜、抬头看月、低头思乡的动作和因果；不要增加具体故乡地点。",
        "focus": "月光与霜的错觉、动作和思乡",
    },
    {
        "id": "06_chunwang", "title": "春望", "author": "杜甫", "dynasty": "唐",
        "text": "国破山河在，城春草木深。\n感时花溅泪，恨别鸟惊心。\n烽火连三月，家书抵万金。\n白头搔更短，浑欲不胜簪。",
        "notes": "诗写战乱背景下的春日所见、忧时伤别、烽火和家书，以及白发增多。",
        "checks": "保留国家破败与山河仍在、花鸟触发悲情、战火延续、家书珍贵和白发难簪等关系；不要削弱战争背景。",
        "focus": "战争背景、花鸟悲情、家书和白发",
    },
    {
        "id": "07_shanjuqiuming", "title": "山居秋暝", "author": "王维", "dynasty": "唐",
        "text": "空山新雨后，天气晚来秋。\n明月松间照，清泉石上流。\n竹喧归浣女，莲动下渔舟。\n随意春芳歇，王孙自可留。",
        "notes": "诗写秋雨后的山居夜景和人物活动；末两句借典表达愿意留居山中。",
        "checks": "保留雨后秋意、月光穿松、清泉流石、浣女归来、渔舟经过以及末句的留居态度；不要把末句简单改成春天景色。",
        "focus": "秋夜山居意象和末句留居态度",
    },
    {
        "id": "08_jiangxue", "title": "江雪", "author": "柳宗元", "dynasty": "唐",
        "text": "千山鸟飞绝，万径人踪灭。\n孤舟蓑笠翁，独钓寒江雪。",
        "notes": "诗以极端空寂的山、路、江雪和孤独垂钓者构成画面。",
        "checks": "保留鸟飞绝、人踪灭、孤舟、蓑笠翁、独钓和寒江雪的极端孤寂；不要加入原文没有的对话或故事。",
        "focus": "极端空寂与独钓者",
    },
    {
        "id": "09_dingfengbo", "title": "定风波·莫听穿林打叶声", "author": "苏轼", "dynasty": "宋",
        "text": "莫听穿林打叶声，何妨吟啸且徐行。\n竹杖芒鞋轻胜马，谁怕？一蓑烟雨任平生。\n料峭春风吹酒醒，微冷，山头斜照却相迎。\n回首向来萧瑟处，归去，也无风雨也无晴。",
        "notes": "词写风雨途中仍从容前行，结尾由天气经验上升为对人生风雨的态度。",
        "checks": "“莫听”是不要受风雨声干扰；“谁怕”是态度；“任平生”和“无风雨也无晴”应保留从具体风雨到人生态度的含蓄转折。",
        "focus": "风雨场景与旷达人生态度的转折",
    },
    {
        "id": "10_rumengling", "title": "如梦令·常记溪亭日暮", "author": "李清照", "dynasty": "宋",
        "text": "常记溪亭日暮，沉醉不知归路。\n兴尽晚回舟，误入藕花深处。\n争渡，争渡，惊起一滩鸥鹭。",
        "notes": "词写日暮溪亭游赏后的回舟、误入荷花深处和惊起鸥鹭。",
        "checks": "保留日暮、沉醉、不知归路、晚归舟、误入荷花深处、争渡和惊起鸥鹭的叙事顺序；不要把“争渡”解释成抽象竞争。",
        "focus": "日暮、回舟、荷花和鸥鹭的叙事顺序",
    },
]

PROMPTS = {
    "P0_minimal": """请将下面的中国古诗词翻译成英文。保持原诗分行，只输出英文译文，不要输出分析或说明。\n\n原文：\n{poem}""",
    "P1_task_standard": """请将下面的中国古诗词翻译成英文，面向不了解中国古典诗词的英语读者。\n\n翻译优先级：\n1. 保留原文的基本语义；\n2. 保留情感关系、语气和关键意象；\n3. 保持原诗分行；\n4. 在不改变含义的前提下使用自然英语；\n5. 不添加原文没有提供的历史事实、人物经历或情节；\n6. 如直译会造成明显误解，可以自然重组，但不要扩写成解释性散文。\n\n只输出英文译文，不要输出分析或译注。\n\n原文：\n{poem}""",
    "P2_context": """请将下面的中国古诗词翻译成英文，面向不了解中国古典诗词的英语读者。\n\n翻译标准：保留基本语义、情感关系、关键意象和原诗分行；英语表达自然；不添加背景资料中没有的事实。\n\n可使用的背景资料：\n{notes}\n\n只输出英文译文，不要输出分析或译注。\n\n原文：\n{poem}""",
    "P3_boundary": """请将下面的中国古诗词翻译成英文。请重点执行以下边界检查：\n{checks}\n\n翻译优先级是：基本语义、情感和语气、关键意象、英语自然度。保持原诗分行，不要添加原文没有的事实，不要把含蓄的诗意改写成解释性散文。完成后自行检查，但最终只输出英文译文。\n\n原文：\n{poem}""",
}

if {p["id"] for p in POEMS} != DEV_IDS | {p["id"] for p in POEMS if p["id"] not in DEV_IDS}:
    raise RuntimeError("Invalid split")


def call_api(prompt: str) -> dict:
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a careful literary translator. Follow the user's output constraints exactly."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 2000,
        "thinking": {"type": "disabled"},
    }
    request = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + API_KEY},
        method="POST",
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("API request failed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the poetry experiment in two strictly separated stages.")
    parser.add_argument(
        "--stage",
        choices=("development", "test"),
        default="development",
        help="Run development prompts first, or the locked test prompt later.",
    )
    parser.add_argument(
        "--condition",
        choices=tuple(PROMPTS),
        help="Required for --stage test; the prompt selected after development analysis.",
    )
    args = parser.parse_args()
    if args.stage == "test" and not args.condition:
        parser.error("--stage test requires --condition, for example --condition P1_task_standard")
    if args.stage == "development" and args.condition:
        parser.error("--condition is only used with --stage test")
    if not API_KEY:
        print("DEEPSEEK_API_KEY is not set. Configure it locally; do not paste it into chat.", file=sys.stderr)
        return 2
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output = DATA_DIR / ("development_outputs.jsonl" if args.stage == "development" else "test_outputs.jsonl")
    meta_path = DATA_DIR / ("development_meta.json" if args.stage == "development" else "test_meta.json")
    if output.exists():
        output.unlink()
    started = datetime.now(timezone.utc).isoformat()
    poems = [poem for poem in POEMS if (poem["id"] in DEV_IDS) == (args.stage == "development")]
    conditions = list(PROMPTS) if args.stage == "development" else [args.condition]
    total = len(poems) * len(conditions)
    done = 0
    with output.open("w", encoding="utf-8") as output_file:
        for poem in poems:
            split = args.stage
            for condition in conditions:
                template = PROMPTS[condition]
                prompt = template.format(poem=poem["text"], notes=poem["notes"], checks=poem["checks"])
                print(f"[{done + 1}/{total}] {split} / {poem['title']} / {condition}", flush=True)
                try:
                    result = call_api(prompt)
                    message = ((result.get("choices") or [{}])[0].get("message") or {})
                    record = {
                        "split": split, "poem_id": poem["id"], "title": poem["title"],
                        "author": poem["author"], "dynasty": poem["dynasty"],
                        "original": poem["text"], "focus": poem["focus"],
                        "condition": condition, "prompt": prompt,
                        "translation": message.get("content", "").strip(),
                        "model": result.get("model", MODEL), "usage": result.get("usage", {}),
                        "created": result.get("created"), "error": None,
                    }
                except Exception as exc:
                    record = {
                        "split": split, "poem_id": poem["id"], "title": poem["title"],
                        "author": poem["author"], "dynasty": poem["dynasty"],
                        "original": poem["text"], "focus": poem["focus"],
                        "condition": condition, "prompt": prompt, "translation": "",
                        "model": MODEL, "usage": {}, "created": None,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                    print("  ERROR: " + record["error"], file=sys.stderr, flush=True)
                output_file.write(json.dumps(record, ensure_ascii=False) + "\n")
                output_file.flush()
                done += 1
                time.sleep(0.3)
    meta = {
        "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "stage": args.stage, "selected_condition": args.condition,
        "model": MODEL, "base_url": BASE_URL, "temperature": 0.2,
        "max_tokens": 2000, "thinking": "disabled", "development_count": len(DEV_IDS),
        "test_count": len(POEMS) - len(DEV_IDS), "conditions": conditions, "records": total,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {done} records to {output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
