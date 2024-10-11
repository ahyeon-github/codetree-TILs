# 행, 열, 정령
R, C, K = map(int, input().split())
# 골렘 출발 열 ci, 출구방향 di (0, 1, 2, 3  북 동 남 서)
# j 좌표(열) 와 골렘 출구 방향을 입력 받음
unit = [list(map(int, input().split())) for _ in range(K)]
# 앞 뒤로는 1 열만큼 * C    -> 1 0 0 0 0 0 1 이 걸 R + 3만큼
# 1로 둘러쌓여 ,  R 가로 행 + 3 , C 세로 열 +2
arr = [[1]+ [0]*C +[1]  for _ in range(R+3)]    + [[1]*(C+2)]
#[1, 0, 0, 0, 0, 0, 1]
#마지막 줄 [1]*(C+2): 숫자 1을 C + 2번 반복하여 리스트로 만듭니다. ex [[1]*5] [1, 1, 1, 1, 1]
# print(arr)


exit_set = set()

# 시계방향
# 동쪽
# 북동남서
# 상우하좌
# i 행, j 열
# 상, 우 , 하, 좌
di  = [-1, 0, 1, 0]
dj = [0,1,0,-1]


def bfs(si, sj):
    q = []
    # 열 * 2 + 행 4개
    v = [[0]* (C+2) for _ in range(R+4)]
    mx_i = 0 # -2 해서 리턴!!!!!
    q.append((si, sj))

    v[si][sj] = 1

    while q:
        ci, cj = q.pop(0)
        mx_i = max(mx_i, ci)
        # 네방향 미방문 조건 : 같은 값 또는 내가 출구 상대방이 골렘
        for di, dj in ((-1, 0), (1,0), (0,-1), (0,1)):
            ni, nj = ci + di, cj + dj
            if v[ni][nj] == 0 and (arr[ci][cj]== arr[ni][nj] or ((ci, cj) in exit_set and arr[ni][nj] > 1)):
                q.append((ni,nj))
                v[ni][nj]=1

    return mx_i -2




ans = 0
# 골렘 번호 1이 외곽 2번 부터 적음
num = 2
# 골렘 입력 좌표 / 방향에 따라서 남쪽 이동 및 정령 최대좌표  계산/누족
# 가운데 좌표 기준으로
for cj, dr in unit:
    ci = 1
    # 최대한 남쪽으로 이동 (우선순위 : 남쪽 ->  서쪽 -> 동쪽)
    # 우선 순위 1 남쪽


# [1] 남쪽으로 최대한 이동
    # 계속 반복
    while True: # 가능한 남쪽으로 최대한 이동
        #  남쪽 우선순위 아래쪽으로 한칸 이동
        if  arr[ci+1][cj-1]+ arr[ci+2][cj] + arr[ci+1][cj+1] == 0: # 빈칸 내려감
            ci += 1
        # 서쪽 방향
        # + arr[ci+1][cj-2]+ arr[ci+2][cj-1] 이게 왜 추가? -> :  5칸이 비어져있어야함
        elif (arr[ci-1][cj-1] + arr[ci][cj-2] + arr[ci+1][cj-1] + arr[ci+1][cj-2] +arr[ci+2][cj-1]) ==0:
            ci+=1
            cj -=1
            # 반시계 방향으로 회전
            dr= (dr-1) % 4
        # 동쪽 방향
        elif ( arr[ci][cj+2] + arr[ci-1][cj+1] + arr[ci+1][cj+1] + arr[ci+2][cj+1]+arr[ci+1][cj+2] )== 0 :
            ci += 1
            cj += 1
            # 시계 방향으로 회전
            dr = (dr +1) % 4
        else :
            break

    if ci < 4 : # 3부터는 범위밖이니깐 , 새로 탐색 , 범위 밖(새롭게 탐색 시작)  모두 초기화
        arr = [[1] + [0] * C + [1] for _ in range(R + 3)] + [[1] * (C + 2)]
        exit_set = set()
        num =2
    else :
        # [2] 골렘을 표시 + 비상구 위치 추가
        arr[ci+1][cj] = arr[ci-1][cj] = num
        arr[ci][cj-1:cj+2] = [num]*3
        num += 1
# bfs 로 내가 갈 수 있는 가장 큰 행 리턴

# 마지막 회전 디렉션 위치
        exit_set.add((ci+di[dr], cj+dj[dr]))
        ans += bfs(ci, cj)


print(ans)