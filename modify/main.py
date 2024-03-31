from time import time

from chart import Chart
from solve import solve, CoordConv
from control import DeviceController

if __name__ == '__main__':
    print('请开启游戏，测量并输入下面五个点的屏幕坐标(以"x, y"的格式输入，单位：像素)：')
    bottom_left = tuple(map(int, input('底部轨道最左下角：').split(',')))
    top_left = tuple(map(int, input('天空线的最左端：').split(',')))
    top_right = tuple(map(int, input('天空线的最右端：').split(',')))
    bottom_right = tuple(map(int, input('底部轨道最右下角：').split(',')))
    retry_button = tuple(map(int, input('暂停界面下，重试按钮的坐标(重试按钮区域上的任意一点即可): ').split(',')))
    print()
    chart_path = input('谱面文件路径: ').strip()

    # 询问用户是否启用延迟
    use_delay = input('是否启用延迟？(y/n): ').strip().lower() == 'y'
    delay = 0.0
    if use_delay:
        delay = float(input('请输入延时(从暂停界面重开游戏所需时间(秒))：'))

    chart = Chart.loads(open(chart_path).read())
    conv = CoordConv(bottom_left, top_left, top_right, bottom_right)
    ans = solve(chart, conv)
    ans_iter = iter(sorted(ans.items()))
    ms, evs = next(ans_iter)

    ctl = DeviceController(server_dir='.')
    start = time() + delay if use_delay else time()  # 根据用户是否启用延迟来设置开始时间
    print('[client] INFO: 自动打歌已启动')
    
    if use_delay:
        try:
            ctl.tap(*retry_button)
            while True:
                now = round((time() - start) * 1000)
                if now >= ms:
                    for ev in evs:
                        ctl.touch(*ev.pos, ev.action, pointer_id=ev.pointer)
                    ms, evs = next(ans_iter)
        except StopIteration:
            print('[client] INFO: 自动打歌已终止')
    else:
        # 用户选择不启用延迟，等待用户按下空格键后开始自动播放
        print('[client] INFO: 等待空格')
        keyboard.wait('space')
        try:
            while True:
                for ev in evs:
                    ctl.touch(*ev.pos, ev.action, pointer_id=ev.pointer)
                ms, evs = next(ans_iter)
        except StopIteration:
            print('[client] INFO: 自动打歌已终止')
