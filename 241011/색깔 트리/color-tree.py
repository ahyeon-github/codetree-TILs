# 노드 정보 저장
nodes = {}  # {(m_id : (p_id, color, max_depth))}
children = {}  # {p_id : [자식 노드의 리스트]}
max_depths = {}  # {m_id : max_depth}
depths = {}  # m_id : 서브트리의 현재 깊이

def add_node(m_id, p_id, color, max_depth):
    if p_id == -1:
        nodes[m_id] = (p_id, color, max_depth)
        max_depths[m_id] = max_depth
        depths[m_id] = 1
        children[m_id] = []
    else:
        temp_depth = 1
        curr = p_id
        valid = True
        ancestors = []
        while curr != -1:
            ancestors.append(curr)
            temp_depth += 1
            if temp_depth > max_depths[curr]:
                valid = False
                break
            curr = nodes[curr][0]
        if valid:
            nodes[m_id] = (p_id, color, max_depth)
            max_depths[m_id] = max_depth
            depths[m_id] = 1
            children.setdefault(p_id, []).append(m_id)
            children[m_id] = []
            curr_depth = 2
            for ancestor in ancestors:
                if depths[ancestor] < curr_depth:
                    depths[ancestor] = curr_depth
                curr_depth += 1
        else:
            # 노드를 추가하지 않습니다.
            pass

def change_color(m_id, new_color):
    def dfs(node):
        p_id, _, max_depth = nodes[node]
        nodes[node] = (p_id, new_color, max_depth)
        for child in children.get(node, []):
            dfs(child)
    dfs(m_id)

def check_color(m_id):
    _, color, _ = nodes[m_id]
    print(color)

def check_score():
    total_score = 0
    visited = set()

    def dfs(node):
        visited.add(node)
        _, color, _ = nodes[node]
        unique_colors = set([color])
        for child in children.get(node, []):
            if child not in visited:
                child_colors = dfs(child)
                unique_colors.update(child_colors)
        value = len(unique_colors)
        nonlocal total_score
        total_score += value ** 2
        return unique_colors

    for root in [n for n in nodes if nodes[n][0] == -1]:
        dfs(root)

    print(total_score)

Q= int(input())

for _ in range(Q):
    command_list = list(map(int, input().split()))
    if command_list[0] == 100:
        add_node(command_list[1], command_list[2], command_list[3], command_list[4])
    elif command_list[0] == 200:
        change_color(command_list[1], command_list[2])
    elif command_list[0] == 300:
        check_color(command_list[1])
    elif command_list[0] == 400:
        check_score()