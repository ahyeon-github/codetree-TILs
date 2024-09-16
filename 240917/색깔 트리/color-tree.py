# 노드 정보 저장
nodes = {}  # {m_id : (p_id, color, max_depth)}
children = {}  # {p_id : [자식 노드의 리스트]}
max_depths = {}  # {m_id : max_depth}

# 새로운 노드 추가
def add_node(m_id, p_id, color, max_depth):
    if p_id == -1:
        # 루트 노드 추가
        nodes[m_id] = (p_id, color, max_depth)
        max_depths[m_id] = max_depth
        children[m_id] = []
    else:
        # 부모 노드의 깊이와 비교하여 추가 가능한지 확인
        if max_depths[p_id] >= max_depth:
            nodes[m_id] = (p_id, color, max_depth)
            max_depths[m_id] = max_depth
            if p_id in children:
                children[p_id].append(m_id)
            else:
                children[p_id] = [m_id]
            children[m_id] = []
        # else:
        #     print(f"Cannot add node {m_id}: exceeds parent {p_id}'s max depth")

# 색상 변경
def change_color(m_id, new_color):
    def dfs(node):
        p_id, _, max_depth = nodes[node]
        nodes[node] = (p_id, new_color, max_depth)
        for child in children.get(node, []):
            dfs(child)
    dfs(m_id)

# 색깔 조회
def check_color(m_id):
    _, color, _ = nodes[m_id]
    print(color)

# 점수 조회
def check_score():
    def dfs(node):
        _, color, _ = nodes[node]
        unique_colors = set([color])
        for child in children.get(node, []):
            unique_colors.update(dfs(child))
        return unique_colors

    total_score = 0
    for node in nodes:
        unique_colors = dfs(node)
        total_score += len(unique_colors) ** 2

    print(total_score)

# 입력 처리
Q = int(input())
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