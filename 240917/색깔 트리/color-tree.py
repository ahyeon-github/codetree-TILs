# 노드 정보 저장
nodes = {}  # {m_id : (p_id, color, max_depth)}
children = {}  # {p_id : [자식 노드의 리스트]}
max_depths = {}  # {m_id : max_depth}


# 부모 노드의 최대 깊이를 재귀적으로 갱신하는 함수
def update_depth(m_id, depth):
    if max_depths[m_id] < depth:
        max_depths[m_id] = depth
        p_id, _, _ = nodes[m_id]
        if p_id != -1:
            update_depth(p_id, depth + 1)

# 새로운 노드 추가
def add_node(m_id, p_id, color, max_depth):
    if p_id == -1:
        # 루트 노드 추가
        nodes[m_id] = (p_id, color, max_depth)
        max_depths[m_id] = max_depth
        children[m_id] = []
    else:
        # 부모 노드의 max_depth와 비교하여 추가할 수 있는지 확인
        if max_depths[p_id] >= max_depth:
            nodes[m_id] = (p_id, color, max_depth)
            max_depths[m_id] = max_depth
            if p_id in children:
                children[p_id].append(m_id)
            else:
                children[p_id] = [m_id]
            children[m_id] = []
            # 부모 노드의 최대 깊이 갱신
            update_depth(p_id, max_depth + 1)
        # 부모의 깊이를 초과하면 아무 동작도 하지 않음

# 색상 변경
def change_color(m_id, new_color):
    # 해당 노드를 루트로 하는 서브트리 내 모든 노드의 색상을 변경
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
    # 해당 노드의 서브트리 내 고유 색상 수를 계산하는 DFS 함수
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