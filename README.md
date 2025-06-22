# GPTKeyChecker

> 一个很垃圾的 GPT Key 检测脚本

## 使用方法

首先安装依赖

```
pip install curl_cffi
```

将要查询的 Key 放入 `key.txt` 中 每行一个

然后按照如下格式启动即可

```
python3 main.py https://api.openai.com/v1/chat/completions 128 http://127.0.0.1:7890 gpt-4.1-mini
```