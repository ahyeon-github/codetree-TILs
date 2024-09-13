# 노드 정보 저장
# node = {m_id , p_id, color, max_depth}
nodes = {}  # {(m_id : (p_id, color, max_depth))}
children = {}  # {p_id : [자식 노드의 리스트]}
# p_id 부모 노드를 갖는 자식 노드를 "리스트"로  저장
# 색상 정보 저장
# color = {red :1 , orange  :2 , yellow : 3, green :4, blue : 5 }

# 최대 깊이
max_depths = {}  # {m_id : max_depth } max_depths[m_id]


# p_id = 0
# m_id = 0
# color = 0
# max_depth = 0



# 새로운 노드 추가
def add_node(m_id, p_id, color, max_depth):
    # 부모 노드 최대 깊이 확인해서 조건에 맞으면 추가
    # -1 이라면 새로운 노드에 바로 추가
    if p_id == -1:
        # 노드 딕셔너리에 정보를 저장
        # node = {m_id: (p_id, color, max_depth)} ->기존값 사라짐
        nodes[m_id] = (p_id, color, max_depth)
        # 최대 깊이 저장
        max_depths[m_id] = max_depth
        children[m_id] = []
    else:
        # max_depth 딕셔너리에서 m_id 에 해당하는 Max_depath를 가져온다.

        # if max_depths[p_id] >= max_depth:
        if p_id in max_depths and max_depths[p_id] >= max_depth:
            # if max_depth{p_id} >= max_depth{m_id} :
            nodes[m_id] = (p_id, color, max_depth)
            # 자식최대 깊이 저장
            max_depths[m_id] = max_depth

            if p_id in children:
                children[p_id].append(m_id)
            else:
                children[p_id] = [m_id]

            # if p_max_depth >= max_depth:
            # node = {m_id: (p_id, color, max_depth)}
            # 리스트로 저장
            # 부모 노드의 자식리스트에 해당 트리를 추가
            # children.append  # {p_id : [자식 노드의 리스트]}


        # else:
        #     # 만약 부모 노드 깊이를 초과한다면 X
        #     # p_max_depth < max_depths
        #     # print(f"Cannot add node {m_id}: exceeds parent {p_id}'s max depth")


# 색상 변경
def change_color(m_id,  new_color):
    # 해당 하는 노드의 서브트리 모두 노드를 탐색해서 색상을 변경
    # DFS 모든 노드 순회
    def dfs(node):
        # node = {m_id: (p_id, chage_color, max_depth)}
        # nodes[m_id] = (p_id, new_color, max_depth)
        p_id, color , max_depth = nodes[node]
        nodes[node] = (p_id, new_color, max_depth)
        for child in children.get(node, []) :
            dfs(child)
    dfs(m_id)


# 색깔 조회
def check_color(m_id):
    # 컬러만 조회
    # nodes = {}  # {(m_id : (p_id, color, max_depth))}

    _, color, _ = nodes[m_id]
    # color = nodes[m_id[color]]
    print(color)


# 노드 현재 색상 조회
# 딕셔너리에서 조회

# 점수 조회
def check_score():
    def dfs(node):
        _, color, _ = nodes[node]  # 현재 노드의 색상 가져오기
        # 현재 노드의 색상을 집합에 추가 (중복되지 않게)
        unique_colors = set([color])
        
        # 자식 노드들을 재귀적으로 탐색
        for child in children.get(node, []):
            # 자식 노드에서 반환된 색상 집합을 현재 색상 집합에 추가
            unique_colors.update(dfs(child))
        
        return unique_colors

    total_score = 0

    # 루트 노드에서만 DFS를 시작 (p_id가 -1인 노드들)
    for node, (p_id, _, _) in nodes.items():
        if p_id == -1:  # 루트 노드인 경우에만 DFS 시작
            unique_colors = dfs(node)
            total_score += len(unique_colors) ** 2  # 고유 색상의 개수의 제곱을 점수에 추가

    # 최종 점수 출력
    print(total_score)



# 상위 루트노드부터 각 아래 서브트리와 색상이 다른지 확인
# 하위 서브트리와 색상 다른 것 개수 확인후 거듭제곱
# BFS


Q= int(input())

for _ in range(Q):
    command_list = list(map(int, input().split()))
    if command_list[0] == 100:
        add_node(command_list[1],command_list[2],command_list[3],command_list[4])
    elif command_list[0] == 200:
        change_color(command_list[1],command_list[2])
    elif command_list[0] == 300:
        check_color(command_list[1])
    elif command_list[0] == 400:
        check_score()