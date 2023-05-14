# Music Player Pico

## 介绍

什么，这不是压缩毛巾？这是一个基于树莓派 Pico 和有源蜂鸣器的音乐播放器。

## 前提

1. 准备好树莓派 Pico 和有源蜂鸣器
    - 因为我只有一个有源蜂鸣器，所以没写多声道的播放
2. 将 MicroPython 固件烧录到树莓派 Pico 上
3. 将 `main.py` 文件复制到树莓派 Pico 的根目录下
4. 修改 `main.py` 文件中引脚的定义等，以适配你的硬件
5. 从 [Open Sequencer](https://opensequencer.net) 复制粘贴你想要播放的音乐的代码（部分不可行）

## 其他

- 由于只有一个有源蜂鸣器（每拍只能播放一个音符），而在播放 `mario.txt` 中的内容时，我发现这个音乐有一个主旋律和两个副旋律（每拍最多重叠三个音符）。因此，在将从 Open Sequencer 那儿复制粘贴来的字符串转换为字典时，我只选择了每拍中的最高音符，这样就需要播放一个旋律了

## 参考

- 仓库中的 `mario.txt` 中的内容来自[这个网址](https://onlinesequencer.net/25966)
- 仓库中的 `shunrun.txt` 中的内容来自[这个网址](https://onlinesequencer.net/3405645)。原曲是 John 的 [春岚](https://www.bilibili.com/video/BV1cJ411q7GF/)，这边我差不多简化了高潮旋律并贴在了 Open Sequencer 上