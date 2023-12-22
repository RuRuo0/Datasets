# Datasets

[![Version](https://img.shields.io/badge/Version-0.0.1-brightgreen)](https://github.com/FormalGeo/Datasets)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Survey](https://img.shields.io/badge/Survey-FormalGeo-blue)](https://github.com/FormalGeo/FormalGeo)

formalgeo7k数据集第2次标注（图像标注，23年12月）。  
访问[FormalGeo主页](https://formalgeo.github.io/)获取更多有关FormalGeo的信息。

## 任务分配

#### Week 1 (231225): form 2023-12-25 to 2024-12-31.

**注意：** 按照PID（Problem Id）标注自己分配的题目。

| Id | Annotator | WorkLoad | PID | Submitted |
|:--:|:---------:|:--------:|:---:|:---------:|
| 1  |    郭彦钧    |    60    | 1-1 |     √     |
| 2  |    贺艺铭    |    60    | 1-1 |     √     |
| 3  |    黄琦珂    |    60    | 1-1 |     √     |
| 4  |    胡正彧    |    60    | 1-1 |     √     |
| 5  |    金啸笑    |    60    | 1-1 |     √     |
| 6  |    李阳     |    60    | 1-1 |     √     |
| 7  |    毛晨扬    |    60    | 1-1 |     √     |
| 8  |    秦城     |    60    | 1-1 |     √     |
| 9  |    岳登峰    |    60    | 1-1 |     √     |
| 10 |    张效凯    |    60    | 1-1 |     √     |
| 11 |    朱方震    |    60    | 1-1 |     √     |
| 12 |    朱娜     |    60    | 1-1 |     √     |
| 13 |    朱哲     |    60    | 1-1 |     √     |
| 14 |    邹佳     |    60    | 1-1 |     ×     |

## 环境配置

下载项目:

    $ git clone --depth 1 https://github.com/RuRuo0/Datasets.git

新建Python环境:

    $ conda create -n formalgeo python=3.10
    $ conda activate formalgeo
    $ pip install formalgeo

新建个人分支并推送到远程仓库：

    $ git checkout -b your_name
    $ git push --set-upstream origin your_name

## 标注协作

几何问题json文件位于：`projects/formalgeo7k/problems`  
几何图像文件位于：`projects/formalgeo7k/diagrams`  
运行解题程序的脚本位于：`projects/formalgeo7k/files/main.py`  
完成每周的标注任务后，提交到远程仓库：

    $ git add projects/formalgeo7k/problems
    $ git add projects/formalgeo7k/diagrams
    $ git commit -m "your_name week_number"
    $ git push

注意：不要add其他文件，否则可能导致分支合并冲突。

## 标注步骤和流程

coming soon ...