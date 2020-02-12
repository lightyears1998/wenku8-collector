# Wenku8 Collector

可用于将[轻小说文库](https://www.wenku8.net/)上的小说缓存为本地内容的工具。

## 一个简略的用法说明

一个缓存《文学少女》的例子：

```shell script
# 从源码安装Wenku8Collector
git clone https://github.com/lightyears1998/wenku8-collector --depth=1
cd wenku8-collector
pipenv sync # 若安装依赖时出现问题可尝试`pipenv install`

# 将《文学少女》缓存为PandocMarkdown格式并分卷
pipenv shell
python . https://www.wenku8.net/novel/0/1/index.htm --standalone-volume --scheme=pandoc-markdown

# 查看输出结果
ls "./文学少女：*.md"

# 随后可继续用Pandoc将PandocMarkdown格式的分卷转换为EPUB格式
# 可使用Calibre等工具进一步编辑Pandoc转换后的EPUB
# 可使用Calibre转换将EPUB转换为MOBI格式以便在Kindle上查看

# 移除Wenku8Collector
pipenv --rm
cd ..
rm -rf wenku8-collector
```

一个使用Pandoc进行后续处理的例子：

```powershell
# 在Windows上使用Powershell

Get-ChildItem -Filter '文学少女：*.md' -Name | ForEach-Object {
    $name = [System.IO.Path]::GetFileNameWithoutExtension($_)
    pandoc "$name.md" -o "$name.epub" --metadata "language=zh-CN" --css "extra/zh-CN.css"
}
```

## 声明

本工具**不是**wenku8官方推出的工具，与wenku8无关。
请在遵循wenku8使用条款的前提下使用本工具。
