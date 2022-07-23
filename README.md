# TI4ALL

核酸检测信息自动提取工具（**T**est **I**nformation **For** **ALL**）


<p align="center">
  <a href=".\doc\ti4all.png">
    <img src=".\doc\ti4all.png" width="60%" >
  </a>
</p>
<p align="center">
    <a href=""><img src="https://img.shields.io/badge/release-3.1-green"></a>
    <a href=""><img src="https://img.shields.io/badge/python-3.8+-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/os-win10/11-pink.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/support-NUAA-blue.svg"></a>
</p>
<p align="center">
“九秋风露越窑开，夺得千峰翠色来”，立秋将至，祝我们在金秋九月收获美好！
</p>

## 简介

本项目旨在利用自动化手段提高核酸结果筛查效率，尽可能减轻工作人员负担。初期工作完成于南京航空航天大学计算机科学与技术学院/人工智能学院，已初步推广使用。

本项目仅对大批量苏康码进行了测试，但程序易于移植，欢迎推广使用并贡献代码！

## 目录

- [快速开始](#快速开始)
  - [客户端教程](客户端教程)
  - [源码运行](#源码运行)
- [效果展示](#效果展示)
- [更新日志](#更新日志)
- [项目结构](#项目结构)
- [打包流程](#打包流程)
- [开发心得](#开发心得)
- [优化方向](#优化方向)
- [感谢](#感谢)

## 快速开始

### 客户端教程

百度网盘：[下载链接](https://pan.baidu.com/s/11Xvp-V0L5Cg8-LCNBWan2w?pwd=ccst)    提取码：ccst

<p align="center">
  <img src="doc\run.png" width="50%">
</p>

- 当需求仅为 **获得大量核酸报告识别结果** （大多数场景）

  - ”辅助信息文件“一栏：选择 `data/placeholder.xlsx`
  
  - 运行结束后：点击 “保存检测结果”

- 当需求为 **获得大量核酸报告识别结果** 且 **关联个人辅助信息** 

  - “辅助信息文件” 一栏：填充并选择 `data/template.xlsx`
  
  - 注意：`data/template.xlsx` 必须存在 “姓名” 和 “身份证号” 两列，其余列根据需求自行增加/删除

- “核酸检测图片文件夹” 示例：

<p align="center">
  <img src="doc\example2.png" width="80%">
</p>


- 关于”开启多核“：**一般情况下无需开启**，大量测试数据（超万张）效果可能会有提升

- 初次运行程序：需稍等片刻

### 源码运行

1. `clone`  / [下载压缩包](https://github.com/pengxiao-song/ti4all/archive/refs/heads/main.zip) 后，并进入项目根目录

2. 新建环境

```bash
conda create -n ti4all python=3.8
conda activate ti4all
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 运行主程序

```bash
python main.py
```

## 效果展示

主程序界面：

<p align="center">
  <img src="doc\exe1.jpg" width="70%">
</p>


保存结果：（为确保程序稳健性保留了部分异常数据用于测试）

<p align="center">
  <img src="doc\res1.png" width="70%">
  <img src="doc\res2.png" width="70%">
</p>

## 更新日志

- **2022.07.23 TI4ALL release/v3.1** [@Pengxiao Song](https://github.com/pengxiao-song)

  - 功能优化：增加 “任务中止” 功能
  
  - 优化项目结构，简单的代码重构
  
- 2022.07.02 TI4ALL beta/v3.0  @Shixq

  - 界面优化：优化工作日志区；增加结果显示区
  
- 2022.05.20 TI4ALL beta/v2.1 [@LSTM-Kirigaya](https://github.com/LSTM-Kirigaya)

  - 关键优化：支持多核并行，开启 mlkdnn 加速接口，优化模型载入策略
  
  - 其它优化：增加进度条，优化退出模式
  
- 2022.04.21 TI4ALL release/v2.0 [@Pengxiao Song](https://github.com/pengxiao-song)

  - 客户端程序构建成功
  
  - 关键功能：支持识别结果关联辅助信息
  
- 2022.04.18 TI4ALL release/v1.0 [@Pengxiao Song](https://github.com/pengxiao-song)

  - 脚本程序测试成功
  
  - 核心功能：提取核酸报告中的结构化信息

## 项目结构

```
TI4ALL
├── main.py				// 程序入口
├── config.yaml
├── src					// 源码
│  ├── __init__.py
│  ├── gui
│  │  ├── __init__.py
│  │  ├── *Widget.py
│  │  ├── *Widget.ui
│  ├── utils.py
│  └── app.py
├── data				// 存放示例文件格式
├── log	
├── doc
├── requirements.txt
├── README.md
```

## 打包流程

**前提**：已经参照“源码运行”部分**严格安装依赖**

1. 进入项目根目录

2. 执行命令：

```bash
pyinstaller gui.spec [--noconsole]
```

3. 执行完毕会生成两个文件夹，其中之一是 dist
   - 找到项目环境下的 paddleocr/ppocr 文件夹，复制到 dist/main 目录下
   
   - 找到项目环境下的 paddle/libs 和 paddle/fluid 文件夹，对应复制到 dist/main/paddle 目录下
   
4. 启动 dist/main/ti4all.exe 

## 开发心得

程序的 pipeline 不复杂：OCR配合正则表达式做信息提取； PyQt5 做可视化，Pyinstaller 打包程序。

主要花费的时间在：

- 前期的OCR工具调研，试了多家还是PaddleOCR最好用

- Pyinstaller 打包经历了很多波折，包括各种依赖项版本不匹配、PaddleOCR 库引发的一些错误

最终独自完成了第一版程序的发布，切实解决了实际问题，还是很开心的。于是后面拉了两位同学做进一步优化，合作很愉快！

## 优化方向

- [ ] 优化用户交互逻辑

- [ ] 缩小程序体积（UPX报错QAQ）

- [ ] 完善主界面菜单栏相关功能

## 感谢

为优秀的 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 打call！尝试了多个开源OCR工具，在本场景下PaddleOCR的速度、准确度、稳健性都是最好的。

感谢提供测试数据的同学！感谢一起优化程序的两位队友（贡献者）：Huang-zhelong, Shi-xuanqing

感谢新华日报、扬子晚报等媒体报道。
