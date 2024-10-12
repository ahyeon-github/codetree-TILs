# 방향  상 우 하 좌
di  = [-1, 0, 1, 0]
dj = [0, 1, 0 , -1]


N, M , Q = map (int, input().split())

#arr = [[1]+ [0]* N]

# 2라는 벽으로 둘러싸서 범위체크 안하고 , 범위밖으로 밀리지 않게     +  안에는 입력받은 N 만큼 채우기
# 체스 정보를 입력받음
arr = [[2]*(N+2)] + [[2]+list(map(int, input().split()))+ [2] for _ in range (N) ]
units ={}

#init_k = [0] * M
init_k =[0] * (M+1)


# 디버그용 동작확인
v= [[0]*(N+2) for _ in range(N+2)]

# 기사들에 대한 입력을 받음
# for m in range(M):
for m in range(1, M+1):
    si, sj , h, w, k  = map(int, input().split())
    # 1번 기사에 대한 정보를 딕셔너리로 저장
    units[m] = [si, sj, h, w, k]
    # 초기 체력을 저장
    # 마지막 살아남은 기사의 채력과 Init_k 초기 체력의 차이 뺀 다음 누적
    init_k[m] = k

    # 디버깅 용  표시해서 이동 용으로 출력하기 위해
    for i in range( si, si+h):
        v[i][sj:sj+w] = [m]*w


# 밀리는 작업
#BFS  큐에 저장
def push_unit(start, dr): # start를 dr 방향으로 밀고, 연쇄적으로 처리
    q=[]               # push될 후보들을 저장, q에 append, q에서 pop 해서 주변 탐색
    pset = set() # 이동 기사 번호 저장

    # 대미지도 저장
    damage = [0]*(M+1) # 각 유닛별 대미지를 누적

    # 큐에 초기 데이터 append
    q.append(start)
    pset.add(start)


# 큐에서 빠져나와서 큐가 소진될때까지
    while q:
        # 기사 번호 꺼내와서
        cur = q.pop(0) # 큐에서 데이터 하나 꺼냄
        # 유닛에서 현재 기사의 정보를 꺼냄
        ci, cj, h, w, k = units[cur]

        # 명령받은 방향 진행 , 벽이 아니면 ,  겹치는 다른 조각이면  => 큐에 삽입
        # next i 이동
        # 진행방향
        ni, nj = ci + di[dr], cj+dj[dr]
        for i in range(ni, ni+h):
            # for j in range(nj, nj+h):
            # 디버깅 했을 때 벽이 있는데도 밀어버림 w를 안써서 그런거였음
            for j in range(nj, nj + w):
                # 이동할 좌표에 arr가 벽이라면
                if arr[i][j] == 2: # 벽이라면 밀 수 없음  모두 취소
                    return

                # 함정인 경우 대미지
                if arr[i][j] == 1:
                    # 대미지 현재 기사 누적
                    damage[cur] += 1# 대미지 누적

        # 겹치는 다른 유닛있는 경우 큐에 추가 (모든 유닛 체크)
        for idx in units:
            # 모든 유닛 꺼내고 겹치는지(좌표)
            if idx in pset:
                continue # 이미 움직일 대상 pset이라면 체크할 필요 없음

            ti,tj, th, tw, tk = units[idx]
            # 이동하는 칸에 다른 기사가 있다면 겹치는 처리 겹치면 기사도 한칸씩 밀려야 하니깐

#           # 복집한 방법 상우하좌 (닿는 경우..)
#
#             # 움직이는 기사 상단(윗면이 닿고  기사 하단(밑면이 닿고)
#             if ((ni == ti+th-1) or (ni+h-1 == ti)
#             #가로 세로가 일치하는 경우  나의 세로 좌표가  그범위 안에 있는 경우
#                 and ((tj <= nj <tj+tw or tj<=nj+w-1<tj+tw) and(nj<=tj+tw-1<nj+w))or
#                 # 좌우 움직이는 경우 내 왼쪽이 오른쪽과 닿은 경우
#             #
#                 (nj == tj + tw-1 or nj+w-1 == tj)
#
#             # 내 우측이 좌측과 닿은 경우
#                 and (ti<=ni <ti+th or ti<= ni+h-1< ti+th  or  ni<=ti<ni+h or ni<=ti+th-1<ni+h):
#
#             # 겹치면 q애 추가
#                         q.append(idx)
#                         pset.add(idx)

            # 겹치지 않은 경우 (or)
            # if ni  > ti + th-1 or ni+h-1 <ti or nj+w-1 < tj or nj > tj+tw-1 :
            #     pass
            # else :
            #     q.append(idx)
            #     pset.add(idx)


            # 겹치는 경우 (and)
            if ni <= ti+th-1 and ni+h-1 >= ti and tj <= nj+w-1 and tj+tw-1 >= nj :
                q.append(idx)
                pset.add(idx)

# 명령을 받은 기사는 데미지 받지 않음
    damage[start] = 0

    for idx in pset:
        # 데미지를 먼저 처리
        # 인덱스에 꺼냄
        si, sj, h, w, k = units[idx]


        for i in range(si, si + h):
            # for j in range(sj, sj+w): #(디버그용) 기존 위치 기사 삭제
            v[i][sj:sj + w] = [0] * w  # 기존 위치 지우기


    # 나머지는 이동, 데미지가 체력 이상이면 삭제처리
    # 이동하는 것
    for idx in pset:
        # 데미지를 먼저 처리
        # 인덱스에 꺼냄
        si, sj, h, w, k = units[idx]

        # 디버그용   코드 이동할 위치를 정함
        # ni, nj = si + di[dr], sj + dj[dr]
        #
        # for i in range(si, si+h):
        #     # for j in range(sj, sj+w): #(디버그용) 기존 위치 기사 삭제
        #     v[i][sj:sj+w] = [0]*w # 기존 위치 지우기

        if k <= damage[idx] : # 체력보다 더 큰 데이미지를 받으면 삭제 처리
            units.pop(idx)
        else:
            ni, nj = si+di[dr], sj+dj[dr]
            # 데미지 빼기
            units[idx] = [ni,nj, h, w, k-damage[idx]]

            for i in range(ni, ni + h):
                v[i][nj:nj + w] = [idx] * w  #이동 위치에 표시

# 명령 입력받기 (있는 유닛만 처리)
for _ in range(Q):
    idx, dr = map(int, input().split())
    # 인덱스가 존재하는가?  사라질수도 있음 데미지가 0 이하 라면
    if idx in units:
        push_unit(idx, dr) # 명령받은 기사 번호, 방향을 바탕으로 연쇄적으로 밀기 (벽이 없는 경우)

        # 디버깅 벽이 있는데도 밀어버림
        # idx를 가져옴



ans = 0
# 초기 체력 init_k - units 에 있는 체력
# unit idx값을 하나씩 빼내서
for idx in units:
    # ans += init_k[idx] - units[idx][k] -> 체력을 의미하는 4
    # 초기 체력 5 , 현재 unit에 저장된  현재 체력 3,  5-3 = 2(받은 데미지)
    ans += init_k[idx] - units[idx][4]

# 기사들이 총 받은 데미지의 함
print(ans)