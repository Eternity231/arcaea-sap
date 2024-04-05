from typing import Any, Union

from easing import Easing


class ArcTap:
    tick: int

    def __init__(self, tick: int):
        self.tick = tick

    def __str__(self):
        return f'arctap(tick={self.tick})'


class Arc: #虹弧Arc & 天空Note
    start: int
    end: int
    start_x: float
    end_x: float
    easing: Easing
    start_y: float
    end_y: float
    color: int
    trace_arc: bool
    taps: list[ArcTap]

    def __init__(
        self,
        start: int,
        end: int,
        start_x: float,
        end_x: float,
        easing: Easing,
        start_y: float,
        end_y: float,
        color: int,
        _,
        trace_arc: bool,
    ):
        self.start = start
        self.end = end
        self.start_x = start_x
        self.end_x = end_x
        self.easing = easing
        self.start_y = start_y
        self.end_y = end_y
        self.color = color
        self.trace_arc = trace_arc
        self.taps = []

    def __getitem__(self, taps):
        if isinstance(taps, tuple):
            self.taps = list(taps)
        else:
            self.taps = [taps]
        return self

    def __str__(self):
        return f'arc(({self.start_x:.02f}, {self.start_y:.02f})@{self.start} -> ({self.end_x:.02f}, {self.end_y:.02f})@{self.end} using {self.easing}, color={self.color}, trace_arc={self.trace_arc}){self.taps}'


class Tap: #地键Tap
    tick: int
    track: int

    def __init__(self, tick: int, track: int):
        self.tick = tick
        self.track = track

    def __str__(self):
        return f'tap(tick={self.tick}, track={self.track})'


class Hold: #地面Hold
    start: int
    end: int
    track: int

    def __init__(self, start: int, end: int, track: int):
        self.start = start
        self.end = end
        self.track = track

    def __str__(self):
        return f'hold(start={self.start}, end={self.end}, track={self.track})'


class Timing:
    tick: int
    bpm: float
    beats_per_measure: float

    def __init__(self, tick: int, bpm: float, beats_per_measure: float):
        self.tick = tick
        self.bpm = bpm
        self.beats_per_measure = beats_per_measure

    def __str__(self):
        return f'timing(tick={self.tick}, bpm={self.bpm}, beats_per_measure={self.beats_per_measure})'


class TimingGroup:
    notes: list[Union[Arc, Timing, Tap, Hold]]  # 可以根据需要添加其他类型

    def __init__(self, notes: list[Union[Arc, Timing]]):
        self.notes = notes

    def __str__(self):
        return f'timinggroup(notes={self.notes})'


class Chart:
    notes: list[Union[Timing, Tap, Hold, Arc, 'TimingGroup']]
    options: dict[str, Any] | None

    def __init__(self, notes: list[Union[Timing, Tap, Hold, Arc, 'TimingGroup']], options: dict[str, Any] | None = None):
        self.notes = notes
        self.options = options

    @classmethod
    def loads(cls, content: str) -> 'Chart':
        lines = content.splitlines()
        options = {}
        notes = []
        line_iter = iter(lines)
        lcls = {
            'true': True,
            'false': False,
            'none': None,
            'arc': Arc,
            'tap': Tap,
            'arctap': ArcTap,
            'hold': Hold,
            'timing': Timing,
            's': Easing.Linear,
            'b': Easing.CubicBezier,
            'so': Easing.So,
            'si': Easing.Si,
            'soso': Easing.SoSo,
            'sisi': Easing.SiSi,
            'sosi': Easing.SoSi,
            'siso': Easing.SiSo,
            'timinggroup': TimingGroup, 
        }
        for line in line_iter:
            if ':' in line:
                key, value = line.split(':')
                options[key] = value
            elif line.startswith('timinggroup'):
                # 忽略 timinggroup 括号内的内容
                open_brace_count = 0
                timinggroup_line = ''
                for char in line:
                    if char == '(':
                        open_brace_count += 1
                    elif char == ')':
                        open_brace_count -= 1
                    timinggroup_line += char
                    if open_brace_count == 0:
                        break
                # 解析 timinggroup 外的内容
                res = eval(timinggroup_line[:-1], {}, lcls)
                notes.append(TimingGroup(*res))
                # 继续处理 timinggroup 大括号内的内容
                open_brace_count = 1
                while open_brace_count > 0:
                    next_line = next(line_iter)
                    for char in next_line:
                        if char == '{':
                            open_brace_count += 1
                        elif char == '}':
                            open_brace_count -= 1
                    # 解析 timinggroup 大括号内的内容
                    if open_brace_count > 0:
                        res = eval(next_line[:-1], {}, lcls)
                        notes.extend(res)
            else:
                # 解析其他类型
                res = eval(line[:-1], {}, lcls)
                notes.append(Tap(*res) if isinstance(res, tuple) else res)
        return Chart(notes, options)

    def __str__(self):
        return f'chart(notes={self.notes}, options={self.options})'


if __name__ == '__main__':
    chart = Chart.loads(open('./songs/tutorial/1.aff').read())
    print(chart)
