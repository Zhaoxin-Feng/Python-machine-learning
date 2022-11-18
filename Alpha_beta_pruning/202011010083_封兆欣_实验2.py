# 结点的结构
class Node:
    def __init__(self, name='', val=0):
        self.name = name  # 字母
        self.val = val  # 初始状态为0
        self.children = []  # 存放子树

# 树的结构
class Tree:
    def __init__(self):
        self.root = None
    # 使用递归的方法创建博弈树
    def buildTree(self, data_list, root):
        for i in range(1, len(data_list)):
            # 非叶子结点需要递归
            if type(data_list[i]) == list:
                root.children.append(Node(data_list[i][0]))
                # 递归调用
                self.buildTree(data_list[i], root.children[i - 1])
            # 叶子结点的情况下，可以直接加
            else:
                root.children.append(Node(data_list[i][0], data_list[i][1]))
    # 以列表形式打印已经创建好的树
    def printTree(self, node):
        # 如果该结点存在子结点
        if node.children:
            print('[', end="")
            print('\'', node.name, '\'', end="")
            for i in range(0, len(node.children)):
                self.printTree(node.children[i])
            print(']', end="")
        # 若该节点为叶节点
        else:
            print('(', '\'', node.name, '\'', ',', node.val, ')', end="  ")


class AlphaBeta:

    def __init__(self, mytree):
        self.mytree = mytree

    # 返回结点的值
    def get_value(self, node):
        return node.val

    # 判断结点是否为叶子结点，若是，返回True，否则返回False
    def isTerminal(self, node):
        if node.val == 0:
            return False
        else:
            return True

    # 使用AlphaBeta剪枝进行搜索，返回下一步应该决策的结点v
    def minmax_with_alphabeta(self, node):
        v = self.max_value(node, -10000, 10000)
        for child in node.children:
            if child.val == v:
                return child

    # 计算最大值,alpha是剪枝区间下限，beta是剪枝区间上限，v是子节点中的最大值
    def max_value(self, node, alpha, beta):
        # 如果是叶子节点直接返回
        if self.isTerminal(node):
            # 输出搜索过的结点名称
            print(node.name, end=" ")
            return self.get_value(node)
        v = -10000
        # 搜索子节点，如果某个子节点大于beta，则返回，否则一直寻找子结点中的最大值，并且试图更新alpha值
        for child in node.children:
            print(node.name, end=" ")
            v = max(v, self.min_value(child, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        node.val = v
        return v

    # 计算最小值,alpha是剪枝区间下限，beta是剪枝区间上限，v是子节点中的最小值
    def min_value(self, node, alpha, beta):
        if self.isTerminal(node):
            # 输出搜索过的结点名称
            print(node.name, end=" ")
            return self.get_value(node)
        v = 10000
        # 搜索子节点，如果某个子节点小于等于alpha，则返回 ;否则一直寻找子节点中的最小值，并试图更新beta
        for child in node.children:
            print(node.name, end=" ")
            v = min(v, self.max_value(child, alpha, beta))
            if v <= alpha:
                return v
            beta = min(v, beta)
        node.val = v
        return v

root = Node()
tree = Tree()
data = ['A', ['B', ['D', ['H', ('O', 3), ('P', 20)], ['I', ('Q', 2), ('R', 10)]], ['E', ['J', ('S', 13)], ['K', ('T', 22), ('U', 1)]]],
        ['C', ['F', ['L', ('V', 2), ('W', 10)]], ['G', ['M', ('X', 2), ('Y', 5)], ['N', ('Z', 3)]]]]
tree.buildTree(data, root)
ab = AlphaBeta(tree)
result = ab.minmax_with_alphabeta(root)
print()
print("Best choice:{}".format(result.name))
print("Val:{}".format(result.val))
