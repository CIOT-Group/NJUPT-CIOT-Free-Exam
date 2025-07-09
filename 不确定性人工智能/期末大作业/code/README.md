<div align="center">

# CSM: Cloud Sentiment Model

基于BERT和云模型的不确定性情感识别模型（南京邮电大学不确定性人工智能大作业）<br>
输入一段文字，模型预测该段文字是积极还是消极情感，并给出不确定度

</div>

## 环境配置

1. 克隆仓库并安装依赖，推荐使用 python3.10

```bash
git clone https://github.com/SUC-DriverOld/Cloud-Sentiment-Model
cd Cloud-Sentiment-Model
conda create -n csm python=3.10 -y
conda activate csm
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
```

2. 从 Huggingface 下载预训练的BERT模型 [chinese-roberta-wwm-ext-large](https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/tree/main)，按照下面的文件夹结构放置到 `pretrain` 文件夹下。只需要下载以下文件即可，其余文件不必下载。如果想要使用其他 bert 预训练模型，可以修改配置文件中的 `bert` 参数。

```bash
# 以chinese-roberta-wwm-ext-large为例，在pretrain文件夹下需要新建文件夹chinese-roberta-wwm-ext-large
pretrain
    └─chinese-roberta-wwm-ext-large
        │-─ added_tokens.json
        │-─ config.json
        │-─ pytorch_model.bin
        │-─ special_tokens_map.json
        │-─ tokenizer.json
        │-─ tokenizer_config.json
        └-─ vocab.txt

# 对应的配置文件
bert:
  download: false           # 是否下载预训练模型，如果手动下载了，可以设置为false
  cache_dir: "pretrain"     # 自动下载的预训练模型存放路径
  model: "pretrain/chinese-roberta-wwm-ext-large" # 手动加载的模型路径，或者自动模型的Huggingface仓库地址
```

## 数据集制作&修改配置文件

1. 数据集可以从 [ChineseNlpCorpus](https://github.com/SophonPlus/ChineseNlpCorpus) 获取。
2. 可以使用多个 `.csv` 或 `.tsv` 文件作为数据集。将他们存放到同一个文件夹下，然后在配置文件 `configs/config.yaml` 中修改 `data.path` 为你的数据集存放路径即可。
3. 数据集必须是以下面的格式（以csv为例），其中 `label` 列表示标注，每个标注对应的情感在配置文件 `model.labels` 中定义，`text` 列的值是训练文本。其余列可有可无，不影响训练。

```bash
# 例如以下csv格式的数据集
label,text
1,帅的呀，就是越来越爱你！[爱你][爱你][爱你]
1,美~~~~~[爱你]
1,梦想有多大，舞台就有多大![鼓掌]
0,写点儿字容易吗？降税降税[怒骂]
0,可惜啊！它们不是我的啊！[泪][泪]800000啊

# 以及配置文件model.labels的值
labels:
  0: "Negative"
  1: "Positive"
```

3. 按需修改配置文件，配置文件位于 `configs/config.yaml`，有关 `models` 的参数说明如下：

```yaml
model:
  cloud_drop_num: 512       # 云模型云滴数量
  cloud_dim: 16             # 模型维度大小
  attention: false          # 是否使用attention
  labels:                   # 情感标签，可扩充，必须和训练数据中的label列对应
    0: "Negative"
    1: "Positive"
  features:                 # 分类器隐藏层维度，可扩充
  - 256                     # 第一个值需要小于cloud_drop_num * cloud_dim
  - 64
  - 16                      # 最后一个值需要大于标签数量
  dropout: 0.2              # 分类器的dropout率
```

## 训练

1. 使用下面的命令开始训练，第一次开始训练时，会进行数据预处理（速度较慢）。之后如果继续训练，会直接加载上一次预处理后的数据。

```bash
python train.py -c path/to/config.yaml
```

2. 如果需要继续训练，可以使用`-m`传入初始模型，例如

```bash
python train.py -c path/to/config.yaml -m path/to/last/model.ckpt
```

## 推理

推理使用 `inference.py`，该脚本有两种模式。一次性推理和对话类的交互推理。

1. 一次性推理，使用下面的命令，其中 `-m` 传入训练好的模型，`-t` 传入需要推理的文本。注意如果文本中带有空格则需要使用引号将文本括起来。

```bash
python inference.py -m path/to/last/model.ckpt -t 你好呀，今天天气真好！

# 输出结果
Loading tokenizer and model...
[Input]: 你好呀，今天天气真好！
[Prediction]: Positive, [Uncertainty]: 0.2147147823125124
```

2. 对话类的交互推理，使用下面的命令，其中 `-m` 传入训练好的模型。不需要输入文本。如果想退出聊天，按下 `Ctrl+C` 即可。

```bash
python inference.py -m path/to/last/model.ckpt

# 输出结果
Loading tokenizer and model...
>>> 你好呀，今天天气真好！
Prediction: Positive, Uncertainty: 0.2147147823125124
>>> 我太难受了！          
Prediction: Negative, Uncertainty: 0.08376982249319553
```

3. 若需要指定最大推理文本长度，可以传入参数 `--max_length`，默认为128。
4. 若想要使用自定义配置文件，而不使用模型内置的配置文件，可以传入参数 `-c` 指定配置文件路径。但需要注意配置文件需要和模型匹配，否则会报错。

## 参考

- 中文 BERT-wwm | [Chinese-BERT-wwm](https://github.com/ymcui/Chinese-BERT-wwm)
- 中文 自然语言处理 语料/数据集 | [ChineseNlpCorpus](https://github.com/SophonPlus/ChineseNlpCorpus)
