import time

from machine import PWM, Pin

# 音符&频率Hz对照表
tones = {
    'C0': 16, 'C#0': 17, 'D0': 18, 'D#0': 19, 'E0': 21, 'F0': 22,
    'F#0': 23, 'G0': 24, 'G#0': 26, 'A0': 28, 'A#0': 29, 'B0': 31,
    'C1': 33, 'C#1': 35, 'D1': 37, 'D#1': 39, 'E1': 41, 'F1': 44,
    'F#1': 46, 'G1': 49, 'G#1': 52, 'A1': 55, 'A#1': 58, 'B1': 62,
    'C2': 65, 'C#2': 69, 'D2': 73, 'D#2': 78, 'E2': 82, 'F2': 87,
    'F#2': 92, 'G2': 98, 'G#2': 104, 'A2': 110, 'A#2': 117, 'B2': 123,
    'C3': 131, 'C#3': 139, 'D3': 147, 'D#3': 156, 'E3': 165, 'F3': 175,
    'F#3': 185, 'G3': 196, 'G#3': 208, 'A3': 220, 'A#3': 233, 'B3': 247,
    'C4': 262, 'C#4': 277, 'D4': 294, 'D#4': 311, 'E4': 330, 'F4': 349,
    'F#4': 370, 'G4': 392, 'G#4': 415, 'A4': 440, 'A#4': 466, 'B4': 494,
    'C5': 523, 'C#5': 554, 'D5': 587, 'D#5': 622, 'E5': 659, 'F5': 698,
    'F#5': 740, 'G5': 784, 'G#5': 831, 'A5': 880, 'A#5': 932, 'B5': 988,
    'C6': 1047, 'C#6': 1109, 'D6': 1175, 'D#6': 1245, 'E6': 1319, 'F6': 1397,
    'F#6': 1480, 'G6': 1568, 'G#6': 1661, 'A6': 1760, 'A#6': 1865, 'B6': 1976,
    'C7': 2093, 'C#7': 2217, 'D7': 2349, 'D#7': 2489, 'E7': 2637, 'F7': 2794,
    'F#7': 2960, 'G7': 3136, 'G#7': 3322, 'A7': 3520, 'A#7': 3729, 'B7': 3951,
    'C8': 4186, 'C#8': 4435, 'D8': 4699, 'D#8': 4978, 'E8': 5274, 'F8': 5588,
    'F#8': 5920, 'G8': 6272, 'G#8': 6645, 'A8': 7040, 'A#8': 7459, 'B8': 7902,
    'C9': 8372, 'C#9': 8870, 'D9': 9397, 'D#9': 9956, 'E9': 10548, 'F9': 11175,
    'F#9': 11840, 'G9': 12544, 'G#9': 13290, 'A9': 14080, 'A#9': 14917, 'B9': 15804
}

# 设置蜂鸣器
buzzer = PWM(Pin(15))  # 蜂鸣器引脚
buzzer.freq(50000)  # PWM频率
buzzer.duty_u16(int(65536 * 0.2))  # PWM占空比

# 节拍
bpm = 180  # 每分钟节拍数
time_signature = [4, 4]  # 拍号
beat_duration = (60 / bpm) / time_signature[0]  # 一拍的时间


def slice_notes(notes) -> dict:
    """
    将Online Sequencer复制粘贴来的旋律切割为主旋律和副旋律两个不同的列表。
    :param notes: Online Sequencer复制粘贴来的旋律
    :return: 主旋律的字典
    """
    notes_dict = {}
    for note in notes:
        note_parts = note.split()
        beat = float(note_parts[0])
        # 如果字典内没有该时间位置
        if beat not in notes_dict:
            # 添加该音符到字典中
            notes_dict[beat] = note_parts[1:]
        else:
            # 如果该时间位置重复，且音符频率大于字典中存在的音符
            if tones[note_parts[1]] >= tones[notes_dict[beat][0]]:
                # 覆盖之前的音符
                notes_dict[beat] = note_parts[1:]
    return notes_dict


def play_note(note, duration) -> None:
    """
    播放音符。
    :param note: 音符
    :param duration: 持续时间
    :return: 无
    """
    buzzer.freq(tones[note])
    time.sleep(duration)


def play_melody(melody_dict) -> None:
    # 从第0拍开始播放
    current_beat = float(0)

    # 播放到最后一个音符
    while current_beat <= max(melody_dict.keys()):
        note_duration = float(melody_dict[current_beat][1]) * beat_duration

        if current_beat in melody_dict:
            note_name = melody_dict[current_beat][0]

            # 如果占有音符名称位置的字符串为X，即暂停（通常为暂停半拍）
            if note_name == "X":
                print("第" + str(current_beat) + "拍：X暂停，持续时间为" + str(beat_duration) + " 秒。")
                buzzer.freq(50000)
                time.sleep(beat_duration)
                current_beat += 1

            else:
                print("第" + str(current_beat) + "拍：播放音符 " + note_name + " 中，持续时间为 " + str(
                    note_duration) + " 秒。")
                play_note(note_name, note_duration)
                current_beat += float(melody_dict[current_beat][1])
                buzzer.freq(50000)

        else:
            # 通常为暂停一整拍
            print("第" + str(current_beat) + "拍：暂停，持续时间为" + str(note_duration) + " 秒。")
            buzzer.freq(50000)
            time.sleep(beat_duration)
            current_beat += 1

    print("播放结束。")
    buzzer.freq(50000)


if __name__ == "__main__":
    with open('shunrun.txt', 'r') as f:
        song_file = f.read()

    song = song_file.split(":")[2]  # 去除开头的Online Sequencer签名
    notes_list = song.split(";")[:-1]  # 去除最后的空白元素
    main_melody = slice_notes(notes_list)
    play_melody(main_melody)
