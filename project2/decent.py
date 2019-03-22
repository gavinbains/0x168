import sys
from datetime import datetime

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
        r_synergy = set()
        d_synergy = set()
        for hero in self.radiant:
            sum_radiant += hero.m_i * hero.p
            r_synergy.add(hero.id % 10)
        if len(r_synergy) == 5:
            sum_radiant += 120

        for hero in self.dire:
            sum_dire += hero.m_j * hero.p
            d_synergy.add(hero.id % 10)
        if len(d_synergy) == 5:
            sum_dire += 120

        self.advantage = sum_radiant - sum_dire
        return self.advantage

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.radiant) + repr(self.dire) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'


def minimax(state: Node):
    advantage = max_value(state)
    for elem in state.children:
        if elem.advantage == advantage:
            print(elem.radiant)
            return str(int(elem.radiant[-1].id))


def min_value(state: Node):
    if len(state.dire) == 5 and len(state.radiant) == 5:
        state.calc_advantage()
    else:
        state.advantage = sys.float_info.max
        for hero in state.pool:
            # new_node_list_radiant = copy.deepcopy(state.radiant)
            # new_node_list_dire = copy.deepcopy(state.dire)
            new_node_list_radiant = state.radiant[:]
            new_node_list_dire = state.dire[:]
            new_node_list_dire.append(hero)
            state.pool.remove(hero)
            new_node = Node(new_node_list_radiant, new_node_list_dire, state.pool, state)
            state.add_child(new_node)
            state.advantage = min(state.advantage, max_value(new_node))
            state.pool.append(hero)
            state.pool.sort(key=lambda h: h.id)
    return state.advantage


def max_value(state: Node):
    if len(state.dire) == 5 and len(state.radiant) == 5:
        state.calc_advantage()
    else:
        state.advantage = -sys.float_info.max
        for hero in state.pool:
            new_node_list_radiant = state.radiant[:]
            new_node_list_dire = state.dire[:]
            new_node_list_radiant.append(hero)
            state.pool.remove(hero)
            new_node = Node(new_node_list_radiant, new_node_list_dire, state.pool, state)
            state.add_child(new_node)
            state.advantage = max(state.advantage, min_value(new_node))
            state.pool.append(hero)
            state.pool.sort(key=lambda h: h.id)
    return state.advantage


def alpha_beta(state: Node):
    advantage = ab_max_value(state, -sys.float_info.max, sys.float_info.max)
    for elem in state.children:
        if elem.advantage == advantage:
            print(elem.radiant)
            return str(int(elem.radiant[-1].id))


def ab_max_value(state: Node, alpha, beta):
    if len(state.dire) == 5 and len(state.radiant) == 5:
        state.calc_advantage()
    else:
        state.advantage = -sys.float_info.max
        for hero in state.pool:
            new_node_list_radiant = state.radiant[:]
            new_node_list_dire = state.dire[:]
            new_node_list_radiant.append(hero)
            state.pool.remove(hero)
            new_node = Node(new_node_list_radiant, new_node_list_dire, state.pool, state)
            state.add_child(new_node)
            state.advantage = max(state.advantage, ab_min_value(new_node, alpha, beta))
            state.pool.append(hero)
            state.pool.sort(key=lambda h: h.id)
            if state.advantage >= beta:
                return state.advantage
            alpha = max(alpha, state.advantage)
    return state.advantage


def ab_min_value(state: Node, alpha, beta):
    if len(state.dire) == 5 and len(state.radiant) == 5:
        state.calc_advantage()
    else:
        state.advantage = sys.float_info.max
        for hero in state.pool:
            new_node_list_radiant = state.radiant[:]
            new_node_list_dire = state.dire[:]
            new_node_list_dire.append(hero)
            state.pool.remove(hero)
            new_node = Node(new_node_list_radiant, new_node_list_dire, state.pool, state)
            state.add_child(new_node)
            state.advantage = min(state.advantage, ab_max_value(new_node, alpha, beta))
            state.pool.append(hero)
            state.pool.sort(key=lambda h: h.id)
            if state.advantage <= alpha:
                return state.advantage
            beta = min(beta, state.advantage)
    return state.advantage


def read_input(file):
    startTime = datetime.now()
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

    out = open("output.txt", "w+")
    if ab:
        out.write(alpha_beta(root))
    else:
        out.write(minimax(root))
    print(datetime.now() - startTime)


read_input("test_case/input2.txt")
