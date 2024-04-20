import os

from chart import Chart, Arc, Hold, Tap, ArcTap

def modify_chart(chart, value):
    for note in chart.notes:
        if isinstance(note, Arc):
            note.start -= value
            note.end -= value
            for tap in note.taps:
                tap.tick -= value
        elif isinstance(note, Hold):
            note.start -= value
            note.end -= value
        elif isinstance(note, Tap):
            note.tick -= value
        elif isinstance(note, ArcTap):
            note.tick -= value

    return chart

if __name__ == '__main__':
    chart_path = input('谱面文件路径: ').strip()
    value_to_subtract = int(input('要减去的数值: ').strip())

    chart = Chart.loads(open(chart_path).read())
    modified_chart = modify_chart(chart, value_to_subtract)

    # 保存修改后的文件
    with open('modify.aff', 'w') as f:
        f.write(str(modified_chart))

