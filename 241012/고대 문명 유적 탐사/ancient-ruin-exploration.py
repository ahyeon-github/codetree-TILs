#[3] roate 함수 짜기
# 회전시킨 array start 하는 좌표
def rotate(arr, si, sj): # 90 도 시계방향으로 회전
    # arr 배열의 전체 복사본을 narr로 만듦
    # 회전시킬걸 복사
    narr = [x[:] for x in arr]
    # 3X3 배열로 회전
    # 회전시킬 범위
    for i in range(3):
        for j in range(3):
            # 배열을 90 도 회전시키는 작업
            #회전 후 값을 저장할 위치      arr에서 회전 전의 값을 가져오는 부분
                                # 크기 3에서 뺌
            narr[si+i][sj+j] = arr[si+3-j-1][sj+i]
    return narr



# [5] BFS 함수
def bfs(arr, v, si, sj,clr ):
    # 생성
    q = []
    # set 사용 clear를 위해
    sset = set()
    cnt = 0

    # # set 사용 clear를 위해
    # sset = set()


    # 초기
    # 큐에 초기값 append
    q.append((si, sj))
    # 방문했으면 1
    # v[si][sj] == 1 비교
    v[si][sj] = 1 #대입
    sset.add((si, sj))
    cnt+=1

    while q:
        ci, cj = q.pop(0)
        # 네방향, 범위 내  미방문, 조건 : 같은 값이라면  상하좌우
        for di, dj  in ((-1,0),(1,0),(0,-1),(0,1)):
            # 그다음좌표들
            ni, nj = ci+di , cj+dj
            #    범위 내                             미방문             조건 : 같은값 (array의 현재 위치 c (s아님) 와 arr의 다음 위치)
            if 0<= ni < 5 and  0<= nj < 5 and  v[ni][nj] == 0 and arr[ci][cj] == arr[ni][nj]:
                q.append((ni, nj))
                # v[ni][nj] ==1
                v[ni][nj] = 1
                # set
                sset.add((ni, nj))
                cnt += 1


    # [6] clear
    # 유물이 3개 이상이라면, 리턴도 하고 clear
    if cnt >= 3: # 유물이면 : cnt 리턴 + clr == 1이면 0으로 초기화 clear
        if clr == 1: # 0으로 초기화 하라는 flag
            for i, j in sset:
                arr[i][j] =0
        return cnt
    # 유물이 없다면  3개 미만이면 0을 리턴
    else :
        return 0








# [4] cout clear 함수 회전시킬 arr, clear 할거냐? -> 0 이라면 안함, 1이라면 clear
#clr ==1 인 경우 , 3개 이상 값들을 0으로 clear


def count_clear(arr, clr):
    v= [[0]*5 for _ in range(5)]
    cnt = 0
    for i in range(5):
        for j in range(5): # 미방문인 경우 같은 값이면 1
            # 미방문이라면
            if v[i][j] == 0:
                # 개수를 누적 tmp
                # 방문, i, j 위치, clear 할건인가 말것인가
                # array 에서 미방문이고, 같은 값이면 찾고, 3개 이상이면 clr 을 0으로 만들거나 유지
                # 같은 값이면 bfs 큐에 append 하고 , 3개 이상인 경우 clear하고 리턴
                t= bfs(arr, v, i, j ,clr)
                # 카윤트 누적
                cnt += t
    return cnt



# 반복 횟수, 유물 조각 개수
K,M = map(int, input().split())
# arr 맵에 넣을 숫자들
arr = [list(map(int, input().split())) for _ in range(5)]
# 벽면
lst = list(map(int, input().split()))

# 턴마다 추가해서 누적 합을 출력
ans =[]


# k턴만큼 진행 (K턴을 진행할 때 획득 유물이 없다면 탐사를 종료, )
for _ in range(K):
    #[1] 탐사 진행
    mx_cnt = 0     # 최대를 찾아야함

    # roate
    for rot in range(1, 4): # 우선순위 : 회전 수   -> 열 -> 행 (작은순)
        # for sj in range(0, 3):
        for sj in range(3):
            for si in range(3) :
                # rot 횟수만큼 90 도 시계 방향 회전 -> narr
                # 메이즈러너처럼 회전    복사
                narr = [x[:] for x in arr]  #원본 array를 복사해서 사용
                for _ in range(rot):
                    # new array를 회전시킨다.
                    narr = rotate(narr, si, sj)


                # 유물 개수를 카운트      flag : clear 안할꺼야 0
                t = count_clear(narr, 0 )
                if mx_cnt < t: # 유물의 최대 갯수를 카운트 , 최대 갱신했다면
                    mx_cnt = t
                    marr = narr # 찾은 것 max arry
    # 유물이 없으면 턴 즉시종료
    if mx_cnt == 0:
        break






    #[2] 연쇄획득 :  무한루프 안에서
    # 유물이면 clear

    # 유물 갯수 카운트
    cnt = 0
    arr = marr  # 복사해서 다시 시작
    while True:
        #                    1: clear 해주겠다
        t= count_clear(arr, 1)
        # 연쇄획득을 하는 과정인데 유물이 없다면
        if t == 0:
            break # 연쇄획득 종료 -> 다음 턴으로

        cnt +=t # 발굴한 유물 개수를 누적

        # arr의 0 값인 부분에서 벽면에 적힌 리스트 순서대로 추가
        # 우선순위 :  열 -> 행
        # 열은 작은순으로 채워짐
        for j in range(5):
            # 행은  밑에서 큰 순서대로
            # for i in range(5): (X)
            # 4부터 0까지 하나씩 빼면서
            for i in range(4, -1, -1):
                # arr 비어있는 경우 채워넣어야함
                if arr[i][j] == 0:
                    arr[i][j] = lst.pop(0)


    ans.append(cnt) # 이번턴에서 연쇄 획득한 개수 추가

# 턴별로 공백을 찍어서 출력
#  ans = [3, 4, 5]라고 가정하면, print(ans)는 출력 결과로 리스트 전체를 출력
#  ans 리스트의 각 요소를 개별 인자로 전달합니다. 이것은 마치 print(3, 4, 5)와 같아지며
# 출력 결과는 3 4 5 각 요소가 공백으로 구분되어 출력
print(*ans)