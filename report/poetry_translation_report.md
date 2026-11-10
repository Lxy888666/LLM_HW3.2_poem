# 唐诗宋词英译中的提示设计：开发集与测试集对照实验

## 摘要

本文以十首唐诗宋词的英译为对象，考察不同提示设计对译文质量的影响，并进一步检验提示改动能否迁移到未参与提示选择的新作品。实验预先将语料划分为六首开发集和四首测试集。在开发阶段比较最简提示、任务标准、背景资料和边界检查四种版本；根据开发集结果锁定任务标准版本，在测试阶段只使用该版本。评价主要考察基本语义、情感语气、关键意象、英语自然度和任务适配。结果表明，明确目标读者、翻译优先级和禁止无依据增补的任务标准能够较稳定地改善译文的基本关系保持，并在测试集上表现出一定的迁移能力。背景资料和边界检查具有针对性价值，但应根据具体错误按需使用。

**关键词：** 唐诗宋词；英译；提示设计；开发集；测试集；迁移能力

## 一、研究背景与问题

唐诗宋词的英译不仅涉及词语转换，还涉及情感关系、意象组合、语气和文化语境的重新表达。相同的中文诗句可以产生多种英语译法，译文是否优秀不能只依据英语是否流畅判断，还需要检查是否保留了原作中的关键关系。提示设计的作用，正是在翻译任务开始前明确目标读者、翻译重点和不允许出现的改写。

本研究围绕以下问题展开：

1. 明确目标读者、翻译优先级和禁止无依据增补，是否能够改善诗词英译的基本语义与情感保持？
2. 简短的作品背景资料，是否能帮助模型处理地名、文化意象和含蓄语境？
3. 针对否定、反差、动作顺序或拟人关系的边界检查，能否减少特定误译？
4. 在开发集上有效的提示改动，能否迁移到未参与提示选择的测试集？

## 二、语料与实验划分

实验选取八首唐诗和两首宋词，覆盖相思、登高、羁旅、离别、思乡、战争、山居、孤寂、旷达和闺情等主题。划分在实验开始前固定，测试集不参与提示修改、背景资料增补或评价标准调整。目标读者设定为不了解中国古典诗词的英语读者。

| 集合 | 作品 | 作用 |
|---|---|---|
| 开发集（6 首） | 《相思》《枫桥夜泊》《赠别二首·其二》《静夜思》《春望》《定风波·莫听穿林打叶声》 | 比较四种提示并选择最终版本 |
| 测试集（4 首） | 《登鹳雀楼》《山居秋暝》《江雪》《如梦令·常记溪亭日暮》 | 锁定提示后检验迁移效果 |

## 三、实验方法

### 3.1 提示版本

| 版本 | 增加的信息 | 研究作用 |
|---|---|---|
| P0 最简提示 | 仅要求翻译、分行并只输出译文 | 建立基线 |
| P1 任务标准 | 目标读者、翻译优先级和禁止无依据增补 | 检验任务说明的作用 |
| P2 背景资料 | 每首作品的简短背景说明 | 检验上下文资料的作用 |
| P3 边界检查 | 针对该诗关键关系的核查要求 | 检验错误导向提示的作用 |

四种版本均要求保持原诗分行并只输出英文译文。开发阶段每首诗分别使用四种版本；开发阶段完成后锁定 P1，测试阶段只使用 P1。两个阶段采用相同的模型和生成设置。

### 3.2 评价标准

| 评价维度 | 分值 | 核查内容 |
|---|---:|---|
| 基本语义 | 30 | 事件、动作、关系和逻辑是否保留 |
| 情感与语气 | 20 | 情绪、态度、反差和语气是否改变 |
| 关键意象 | 20 | 景物、人物、物象及其关系是否保留 |
| 英语自然度 | 15 | 是否符合英语表达习惯，是否过度直译 |
| 结构与目的适配 | 15 | 是否保持分行并适合目标读者 |
| **合计** | **100** | |

本研究采用逐条核查和定性比较，不把诗歌审美判断简单折算成精确的自动分数。开发集用于选择提示，测试集只用于最终迁移判断。

## 四、开发集结果与提示选择

开发集比较后，选择 P1 任务标准作为测试阶段的唯一提示版本。选择依据有三点：第一，P1 能够明确目标读者和翻译优先级；第二，它能够约束基本语义、情感关系和关键意象；第三，它比加入大量专门规则的版本更统一，便于迁移和维护。P2 与 P3 的局部优势不直接并入测试提示，避免根据开发集中的个别现象过度增加规则。

| 作品 | 开发集观察 |
|---|---|
| 相思 | 最简版本将“相思”处理成“回忆”，任务标准版本则保留了红豆与相思之间的联系。背景资料和边界检查没有带来明显的额外改进。 |
| 枫桥夜泊 | 各版本基本保留了月落、乌啼、霜、枫树、渔火、寒山寺和钟声等意象。背景资料和边界检查对场景关系的交代较稳定，但个别表达仍不够自然。 |
| 赠别二首·其二 | 各版本均保留了“深情反似无情”和蜡烛拟人的关系。背景资料版本的语气较自然，边界检查版本虽然准确，但个别句子略显生硬。 |
| 静夜思 | 各版本均保留月光误作霜、抬头望月和低头思乡的关系。任务标准版本已经能够满足基本要求，额外说明的收益有限。 |
| 春望 | 各版本均保留战争背景、花鸟悲情、家书和白发等关键内容。任务标准版本在语义完整性和表达简洁度之间较为平衡。 |
| 定风波·莫听穿林打叶声 | 各版本均保留“莫听”“谁怕”和“无风雨也无晴”的态度转折。背景资料版本较紧凑，边界检查版本出现了偏字面的表达。 |

锁定的 P1 任务标准如下：

```text
请将下面的中国古诗词翻译成英文，面向不了解中国古典诗词的英语读者。

翻译优先级：保留基本语义、情感关系、语气和关键意象；保持原诗分行；使用自然英语；不添加原文没有的历史事实、人物经历或情节；必要时可以自然重组，但不要扩写成解释性散文。

只输出英文译文，不要输出分析或译注。

原文：
{poem}
```

## 五、测试集结果与迁移分析

提示版本锁定为 P1 后，使用同一版本处理四首测试集作品。测试集没有参与前面的提示选择。

| 作品 | 测试集观察 |
|---|---|
| 登鹳雀楼 | 锁定的任务标准版本保留了夕阳、黄河、千里视野和继续登楼之间的逻辑，没有把末两句改写成脱离原诗语境的泛泛格言。 |
| 山居秋暝 | 译文保留了雨后秋意、松间月、清泉、浣女、渔舟和末句的留居态度，任务标准能够迁移到新的山水诗。 |
| 江雪 | 译文保留了千山、万径、孤舟、蓑笠翁和独钓等关键关系，说明任务标准能够约束空寂意象的基本表达。 |
| 如梦令·常记溪亭日暮 | 译文保留了日暮、醉后回舟、误入荷花和惊起鸥鹭的叙事顺序，“争渡”被处理为划船动作，没有被改写成抽象竞争。 |

四首测试作品均保留了原诗的主要场景、动作关系和关键意象，说明 P1 的任务标准能够迁移到未参与提示选择的新材料。与此同时，测试结果也表明，通用任务标准不能替代具体的文化知识和专业审校；对于典故、地名和含蓄意象，仍应根据作品需要补充可靠资料。

## 六、讨论

### 6.1 任务标准的作用

任务标准提供了模型无法从单句原文中自动确定的工作约定，例如目标读者、语义优先级和禁止无依据增补。它没有替代模型的语言能力，却减少了“忠实翻译”和“自由改写”之间的歧义，因此在开发集和测试集上都具有较稳定的作用。

### 6.2 背景资料与边界检查的适用范围

背景资料适合处理专名、文化意象和作品语境，但资料本身必须有限、可靠，并且不能诱导译文加入原文没有的事实。边界检查适合对应已经观察到的高风险关系，例如情感反差、动作顺序和拟人关系。没有具体错误依据的规则越多，越可能增加表达负担。

### 6.3 质量与复杂度的平衡

P1 不是输入最短的版本，但它以较少的统一规则覆盖了多种作品，因而比针对单首诗不断追加要求更容易维护。提示设计的目标不是让提示尽可能长，而是用必要的信息稳定解决重要错误。

## 七、结论

本研究得到以下结论：

1. 明确目标读者、翻译优先级和禁止无依据增补，是唐诗宋词英译中最值得保留的基础提示改动。
2. 背景资料和边界检查能够解决特定作品的局部困难，但应由实际错误触发，并在新的材料上验证。
3. 开发集与测试集分离后，P1 在四首新作品上仍能保留主要关系，显示出一定的迁移能力。
4. 诗歌翻译不能只以流畅度判断，必须同时检查语义、情感、意象和目标读者适配。

因此，实际翻译流程可以将 P1 作为通用基础提示；遇到明显的典故、专名或高风险语义关系时，再补充简短资料或单条边界检查。任何新增要求都应经过独立材料验证，不能只依据个别译文的表面改善而保留。

## 八、研究局限

1. 语料只有十首作品，不能覆盖古典诗词的全部体裁和语言现象。
2. 每个条件只运行一次，无法充分估计生成波动。
3. 诗歌存在多种合理译法，部分判断仍需要专业读者复核。
4. 测试集规模较小，迁移结论只能视为初步证据。
5. 运行环境会随时间变化，复现实验时应记录完整提示、模型版本和调用日期。

## 附录：实验原始译文

以下译文为实验生成的原始结果，未进行人工润色。开发集保留四种提示版本的全部输出；测试集只保留锁定的 P1 输出。

### 相思——王维（开发集）

**原文：**

```text
红豆生南国，春来发几枝。
愿君多采撷，此物最相思。
```

**P0 最简提示:**

```text
Red berries grow in southern land.
How many load in spring the trees?
Gather them till full is your hand;
They would revive fond memories.
```

**P1 任务标准:**

```text
Red beans grow in the southland;
When spring comes, how many branches will they send forth?
I hope you will gather many of them—
This thing most evokes longing.
```

**P2 背景资料:**

```text
Red beans grow in the south.
How many branches bloom when spring comes?
I hope you will gather more of them—
This thing is most tied to longing.
```

**P3 边界检查:**

```text
Red beans grow in southern lands,
How many branches spring up when spring comes?
I hope you will gather more of them,
For this thing best speaks of longing.
```

### 枫桥夜泊——张继（开发集）

**原文：**

```text
月落乌啼霜满天，江枫渔火对愁眠。
姑苏城外寒山寺，夜半钟声到客船。
```

**P0 最简提示:**

```text
The moon is down, crows caw, frost fills the sky;
River maples, fishing fires, facing troubled sleep I lie.
Outside the city of Gusu stands Cold Mountain Temple;
At midnight, the sound of its bell reaches the traveler's boat.
```

**P1 任务标准:**

```text
The moon sets, crows caw, frost fills the sky;
river maples, fishing fires, face my troubled sleep.
Outside Gusu City, Cold Mountain Temple—
at midnight, the sound of bells reaches the traveler's boat.
```

**P2 背景资料:**

```text
The moon sets, crows cry, and frost fills the sky;
River maples and fishing lights face my troubled sleep.
Outside the walls of Gusu stands Cold Mountain Temple;
At midnight, the sound of its bell reaches the traveler's boat.
```

**P3 边界检查:**

```text
The moon sets, crows cry, and frost fills the sky;
By riverside maples and fishing lights, I lie in sorrowful sleep.
Outside the city of Gusu stands Cold Mountain Temple;
At midnight, the sound of its bell reaches the traveler's boat.
```

### 赠别二首·其二——杜牧（开发集）

**原文：**

```text
多情却似总无情，唯觉尊前笑不成。
蜡烛有心还惜别，替人垂泪到天明。
```

**P0 最简提示:**

```text
Deep passion seems always heartless;
Before the cup I can't smile, so sad.
The candle has a heart to say goodbye;
It sheds tears for us till the morning.
```

**P1 任务标准:**

```text
Deep feeling seems like heartlessness;
Before the cup I cannot smile.
The candle has a heart that grieves at parting,
And sheds tears for us till dawn.
```

**P2 背景资料:**

```text
Deep feeling seems like no feeling at all;
Before the wine, I somehow cannot smile.
The candle, if it has a heart, grieves at parting,
And sheds tears in our place until dawn.
```

**P3 边界检查:**

```text
Deep feeling seems ever unfeeling;
Before the cup I cannot smile.
The candle has a heart for parting,
And sheds tears for us all night long.
```

### 静夜思——李白（开发集）

**原文：**

```text
床前明月光，疑是地上霜。
举头望明月，低头思故乡。
```

**P0 最简提示:**

```text
Before my bed the silver moonlight glows;
I take it for white frost upon the ground.
I raise my head to watch the moon and, lo,
I lower it and think of home.
```

**P1 任务标准:**

```text
Before my bed the bright moonlight shines;
I take it for frost on the ground.
I raise my head to watch the bright moon;
I lower my head and think of my hometown.
```

**P2 背景资料:**

```text
Before my bed the bright moonlight shines,
I take it for frost on the ground.
I raise my head to watch the bright moon,
I lower my head and think of my hometown.
```

**P3 边界检查:**

```text
Before my bed, the bright moonlight,
I suspect it is frost on the ground.
I raise my head to gaze at the bright moon,
I lower my head and think of my hometown.
```

### 春望——杜甫（开发集）

**原文：**

```text
国破山河在，城春草木深。
感时花溅泪，恨别鸟惊心。
烽火连三月，家书抵万金。
白头搔更短，浑欲不胜簪。
```

**P0 最简提示:**

```text
The country is broken; hills and rivers remain.
In spring the city grows grass and trees deep.
Moved by the times, flowers draw tears;
Hating separation, birds alarm the heart.
Beacon fires have linked three months;
A letter from home is worth ten thousand gold.
White hairs, scratched, grow sparser still;
They almost will not hold a hairpin.
```

**P1 任务标准:**

```text
The country is broken; hills and rivers remain.
In spring the city grows deep with grass and trees.
Moved by the times, flowers draw tears;
hating separation, birds startle the heart.
Beacon fires have burned for three months running;
a letter from home is worth ten thousand in gold.
White hair, scratched, grows even thinner—
soon too sparse to hold a hairpin.
```

**P2 背景资料:**

```text
The country is broken; hills and rivers remain.
In spring the city grows rank with grass and trees.
Moved by the times, flowers draw tears;
hating separation, birds startle the heart.
Beacon fires have burned for three months running;
a letter from home is worth ten thousand in gold.
White hairs, scratched, grow sparser still—
so few they will hardly hold a pin.
```

**P3 边界检查:**

```text
The country is broken, though hills and rivers remain;
In the city in spring, grass and trees are thick.
Moved by the times, flowers draw tears;
Hating separation, birds alarm the heart.
Beacon fires have lasted three months;
A letter from home is worth ten thousand in gold.
Scratching my white hair, it grows thinner;
It simply cannot bear a hairpin.
```

### 定风波·莫听穿林打叶声——苏轼（开发集）

**原文：**

```text
莫听穿林打叶声，何妨吟啸且徐行。
竹杖芒鞋轻胜马，谁怕？一蓑烟雨任平生。
料峭春风吹酒醒，微冷，山头斜照却相迎。
回首向来萧瑟处，归去，也无风雨也无晴。
```

**P0 最简提示:**

```text
Don't heed the sound of rain beating through the forest leaves;
Why not chant and whistle, and stroll along at ease?
A bamboo staff and straw sandals are lighter than a horse—
Who's afraid? In a straw cloak, through mist and rain, I'll live my life as it please.
The biting spring wind sobers me from wine,
A slight chill—yet the slanting sun greets me from the hilltop.
Looking back at the dreary place I came from,
As I return, there is neither wind nor rain, nor shine.
```

**P1 任务标准:**

```text
Don't heed the sound of rain beating through the forest leaves;
Why not chant and whistle, and stroll along at ease?
A bamboo staff and straw sandals are lighter than a horse—
Who's afraid? In a straw cloak, through mist and rain, I'll live my life as it comes.
The biting spring wind sobers me from wine,
A slight chill—yet the slanting sun on the hilltop comes to meet me.
Looking back at the dreary place I came from,
As I return, there is neither wind nor rain, nor shine.
```

**P2 背景资料:**

```text
Don't heed the sound of rain beating through the forest leaves;
Why not chant and whistle, and stroll on at ease?
With a bamboo staff and straw sandals, lighter than a horse—
Who's afraid? In a straw cloak, through mist and rain, I'll live my life as I please.
The biting spring wind sobers me from wine,
A slight chill—
Yet the slanting sun beyond the hill comes out to greet me.
Looking back at the dreary place I came from,
As I return,
There is neither wind nor rain, nor shine.
```

**P3 边界检查:**

```text
Don't heed the sound of rain beating through the forest and striking the leaves;
Why not chant and whistle, and walk on slowly?
With a bamboo staff and straw sandals, lighter than a horse—who's afraid?
In a straw cloak, through misty rain, I'll live my life as I please.

The biting spring wind sobers me from wine;
A slight chill—
Then the slanting sunlight on the hilltop comes to meet me.
Looking back at the dreary place I came from,
As I return,
There is neither wind nor rain, nor any clearing sky.
```

### 登鹳雀楼——王之涣（测试集）

**原文：**

```text
白日依山尽，黄河入海流。
欲穷千里目，更上一层楼。
```

**P1 任务标准:**

```text
The white sun sets behind mountains,
The Yellow River flows into the sea.
To see a thousand miles farther,
Climb one more floor up.
```

### 山居秋暝——王维（测试集）

**原文：**

```text
空山新雨后，天气晚来秋。
明月松间照，清泉石上流。
竹喧归浣女，莲动下渔舟。
随意春芳歇，王孙自可留。
```

**P1 任务标准:**

```text
Empty hills, fresh after rain,
Evening brings the breath of autumn.
Bright moonlight falls through the pines,
Clear springs flow over the stones.
Bamboo rustles as washing girls return,
Lotuses stir as fishing boats drift down.
Let the spring fragrance fade as it will,
The noble wanderer may stay here still.
```

### 江雪——柳宗元（测试集）

**原文：**

```text
千山鸟飞绝，万径人踪灭。
孤舟蓑笠翁，独钓寒江雪。
```

**P1 任务标准:**

```text
A thousand mountains—no bird in flight,
Ten thousand paths—no trace of man.
A lone boat, an old man in straw cloak and hat,
Fishing alone in the cold river snow.
```

### 如梦令·常记溪亭日暮——李清照（测试集）

**原文：**

```text
常记溪亭日暮，沉醉不知归路。
兴尽晚回舟，误入藕花深处。
争渡，争渡，惊起一滩鸥鹭。
```

**P1 任务标准:**

```text
I often remember the pavilion by the stream at dusk,
So intoxicated that I lost my way home.
When my joy was spent, I turned the boat back late,
And mistakenly entered deep among the lotus flowers.
Rowing hard, rowing hard,
I startled a whole sandbank of gulls and herons into flight.
```

## 实验资料说明

实验使用固定的诗词语料、提示模板、模型版本和生成设置。开发阶段保存 24 条译文，测试阶段保存 4 条译文；附录列出全部结果，便于核对研究结论。
