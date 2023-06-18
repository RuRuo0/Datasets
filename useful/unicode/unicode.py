syms = [
    u'\u221A',  # √
    u'\u03C0',  # π
    u'\u25b3',  # △
    u'\u2220',  # ∠
]
"""
01 Α α a:lf 阿尔法 角度；系数
02 Β β bet 贝塔 磁通系数；角度；系数
03 Γ γ ga:m 伽马 电导系数（小写）
04 Δ δ delt 德尔塔 变动；密度；屈光度
05 Ε ε ep`silon 伊普西龙 对数之基数
06 Ζ ζ zat 截塔 系数；方位角；阻抗；相对粘度；原子序数
07 Η η eit 艾塔 磁滞系数；效率（小写）
08 Θ θ θit 西塔 温度；相位角
09 Ι ι aiot 约塔 微小，一点儿
10 Κ κ kap 卡帕 介质常数
11 Λ λ lambd 兰布达 波长（小写）；体积
12 Μ μ mju 缪 磁导系数微（千分之一）放大因数（小写）
13 Ν ν nju 纽 磁阻系数
14 Ξ ξ ksi 克西
15 Ο ο omik`ron 奥密克戎
16 Π π pai 派 圆周率
17 Ρ ρ rou 肉 密度/电阻系数（小写）
18 Σ σ sigma 西格马 总和（大写），表面密度；跨导（小写）
19 Τ τ tau 套 时间常数
20 Υ υ jup`silon 宇普西龙 位移
21 Φ φ fai 佛爱 磁通；角
22 Χ χ phai 西
23 Ψ ψ psai 普西 角速；介质电通量（静电力线）；角
24 Ω ω o`miga 欧米伽 欧姆（大写）；角速（小写）；角
"""


def show_unicode(char):
    print(hex(ord(char)))


def show_char():
    for s in syms:
        print(s)


if __name__ == '__main__':
    show_unicode('🤡')
    show_unicode('A')
    # show_char()
