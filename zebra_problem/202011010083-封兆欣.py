from kanren import run, eq, membero, var, conde  # kanren一个描述性Python逻辑编程系统
from kanren.core import lall  # lall包用于定义规则
import time


class Agent:
    """
    推理智能体.
    """

    def __init__(self):
        """
        智能体初始化.
        """

        self.units = var()  # 单个unit变量指代一座房子的信息(国家，工作，饮料，宠物，颜色)
        self.rules_zebraproblem = None  # 用lall包定义逻辑规则
        self.solutions = None  # 存储结果

    def define_rules(self):
        """
        定义逻辑规则
        """
        # left()表示在左边,next()表示在旁边
        def left(q, p, list):
            return membero((q, p), zip(list, list[1:]))

        def next(q, p, list):
            return conde([left(q, p, list)], [left(p, q, list)])

        # 定义规则
        self.rules_zebraproblem = lall(
            eq((var(), var(), var(), var(), var()), self.units),
            # 英国人住在红房子里
            (membero, ('英国', var(), var(), var(), '红色'), self.units),
            # 西班牙人养狗
            (membero, ('西班牙', var(), var(), '狗', var()), self.units),
            # 日本人是一名油漆工
            (membero, ('日本', '油漆工', var(), var(), var()), self.units),
            # 意大利人喝茶
            (membero, ('意大利', var(), '茶', var(), var()), self.units),
            # 挪威人住在左边的第一个房子里
            eq((('挪威', var(), var(), var(), var()), var(), var(), var(), var()), self.units),
            # 绿房子在白房子的右边
            (left,
             (var(), var(), var(), var(), '绿色'),
             (var(), var(), var(), var(), '白色'),
             self.units),
            # 摄影师养了一只蜗牛
            (membero, (var(), '摄影师', var(), '蜗牛', var()), self.units),
            # 外交官住在黄房子里
            (membero, (var(), '外交官', var(), var(), '黄色'), self.units),
            # 中间那个房子的人喜欢喝牛奶
            eq((var(), var(), (var(), var(), '牛奶', var(), var()), var(), var()), self.units),
            # 喜欢喝咖啡的人住在绿色的房子里
            (membero, (var(), var(), '咖啡', var(), '绿色'), self.units),
            # 挪威人住在蓝房子旁边
            (next, ('挪威', var(), var(), var(), var()),
             (var(), var(), var(), var(), '蓝色'), self.units),
            # 小提琴家喜欢喝橘子汁
            (membero, (var(), '小提琴家', '橘子汁', var(), var()), self.units),
            # 养狐狸的人所住的房子与医生的房子相邻
            (next, (var(), '医生', var(), var(), var()),
             (var(), var(), var(), '狐狸', var()), self.units),
            # 养马的人所住的房子与外交官的房子相邻
            (next, (var(), '外交官', var(), var(), var()),
             (var(), var(), var(), '马', var()), self.units),
            # 将水和斑马加进去
            (membero, (var(), var(), var(), '斑马', var()), self.units),
            (membero, (var(), var(), '水', var(), var()), self.units))

    def solve(self):
        self.define_rules()
        self.solutions = run(0, self.units, self.rules_zebraproblem)
        return self.solutions


agent = Agent()
solutions = agent.solve()

for j in range(0,5):
    print(solutions[0][j])

# 输出养斑马的人
for i in range(0,5):
    list = solutions[0][i]
    if list[3] == '斑马':
        print('养斑马的人住在{}的房子里'.format(list[4]))
# 输出喝水的人
for i in range(0,5):
    list = solutions[0][i]
    if list[2] == '水':
        print('喜欢喝水的人住在{}的房子里'.format(list[4]))