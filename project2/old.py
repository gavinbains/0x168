import copy

hero_list = []


class Hero:
    def __init__(self, attributes):
        self.id = attributes[0]  # Hero ID
        self.p = attributes[1]  # Hero Power
        self.m_i = attributes[2]  # My Mastery
        self.m_j = attributes[3]  # Opponent Mastery
        self.team = attributes[4]  # 0 = in pool; 1 = my team; 2 = opponent team
        self.attributes = attributes

    def __repr__(self):
        return "ID: " + str(self.id)

    def __str__(self):
        return "ID: " + str(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Node:
    def __init__(self, r, d, pool, parent=None):
        self.radiant = r
        self.dire = d
        self.advantage = 0
        self.parent = parent
        self.pool = pool
        self.children = []

    def calc_advantage(self):
        sum_radiant = 0
        sum_dire = 0
        # s_radiant = False
        # s_dire = False
        for hero in self.radiant:
            sum_radiant += hero.m_i * hero.p
        for hero in self.dire:
            sum_dire += hero.m_j * hero.p
        return sum_radiant - sum_dire

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.radiant) + repr(self.dire) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

# def __repr__(self):
# 	return str(self.radiant) + str(self.dire)
#
# def __str__(self):
# 	return str(self.radiant) + str(self.dire)


class Tree:
    def __init__(self, n):
        self.root = n

    def build(self, parent: Node):
        # Check if terminal node
        if len(parent.radiant) == 5 and len(parent.dire) == 5:
            return

        # Build the tree
        if len(parent.pool) != 0:
            for hero in parent.pool:
                new_node_list_radiant = copy.deepcopy(parent.radiant)
                new_node_list_dire = copy.deepcopy(parent.dire)
                new_node_list_radiant.append(hero)
                new_node_list_dire.append(hero)
                new_node_pool = copy.deepcopy(parent.pool)
                new_node_pool.remove(hero)
                new_node = Node(new_node_list_radiant, new_node_list_dire, new_node_pool, parent)
                parent.add_child(new_node)
                self.build(new_node)

    def __str__(self):
        return str(self.root)


def minimax():
    print("minimax")


def alpha_beta():
    print("ab")


def read_input(file):
    f = open(file, "r")
    ab = False
    radiant_init = []
    dire_init = []
    pool_init = []
    total_heroes = f.readline()

    if f.readline() == "ab":
        ab = True

    for x in f:
        x = x.rstrip()
        x_list = x.split(",")
        attribute_list = [float(i) for i in x_list]
        hero_list.append(Hero(attribute_list))

    hero_list.sort(key=lambda h: h.id)
    for hero in hero_list:
        if hero.team == 1:
            radiant_init.append(hero)
        elif hero.team == 2:
            dire_init.append(hero)
        else:
            pool_init.append(hero)
    root = Node(radiant_init, dire_init, pool_init)
    tree = Tree(root)
    tree.build(tree.root)
    print(tree)
    if ab:
        alpha_beta()
    else:
        minimax()

    out = open("output.txt", "w+")
    out.write("HERO")


read_input("test_case/input8.txt")
