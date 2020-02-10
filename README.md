# Wenku8 Collector

## 一个简略的用法说明

```shell script
# 从源码安装Wenku8Collector
git clone https://github.com/lightyears1998/wenku8-collector --depth=1
cd wenku8-collector
pipenv sync # 若安装依赖时出现问题可尝试`pipenv install`

# 为《文学少女》生成PandocMarkdown格式输出
pipenv shell
python . https://www.wenku8.net/novel/0/1/index.htm --scheme=pandoc-markdown

# 使用Pandoc将PandocMarkdown格式转换为EPUB格式
pandoc "文学少女.md" -o output.epub --metadata "language=zh-CN"
# 可使用Calibre等工具进一步编辑output.epub，并转换为MOBI格式以便在Kindle上查看
cp output.epub ..

# 移除Wenku8Collector
pipenv --rm
cd ..
rm -rf wenku8-collector
```

## 声明

本工具**不是**wenku8官方推出的工具，与wenku8无关。请在遵循wenku8使用条款的前提下使用本工具。
