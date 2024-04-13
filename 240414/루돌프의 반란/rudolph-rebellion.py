N,M,P,C,D = map(int, input().split())
# 루돌프 산타 좌표 표시
v= [[0]*N for _ in range(N)]

#루돌프 좌표 1씩 빼서 
# int 안써서 오류
ri, rj = map(lambda x:int(x)-1, input().split())
# 루돌프 -1
v[ri][rj]= -1

#socre, alive, wakeup
score = [0] * (P+1)
# 0이면 다 죽은 것 종료
alive = [1] * (P+1)
# 배열 첫칸은 0
alive[0] = 0
# 1로 세팅 충돌 후 0
wakeup_turn = [1] * (P+1)


# 산타 좌표
santa  = [[N]*2 for _ in range(P+1)]

for _ in range(1, P+1):
    n,i,j = map(int, input().split())
    santa[n] = [i-1,j-1]
    # v에 움직인 산타의  번호도 표시해줌
    v[i-1][j-1] = n


def move_santa(cur, si, sj , di, dj, mul):
    q = [(cur, si, sj, mul )] # cur번쨰 산타를 si, sj 좌표에서 di, dj 방향으로 mul 만큼 이동

    while q:
        cur , ci, cj, mul = q.pop(0)
        # 범위 a내 범위밖 
        # 진행방향 mul 칸 만큼 이동시켜서 범위내 / 범위밖 처리
        # 범위내이고 산타있으면 q 처리
        ni, nj = ci+di*mul, cj+dj*mul
        if 0<=ni<N and 0<=nj<N: # 범위내 => 산타 있냐없냐 겹치냐
            if v[ni][nj] == 0: # 빈칸  => 이동처리
                v[ni][nj] = cur
                santa[cur] = [ni,nj]
                return
            else:
                # 산타가 있는 경우
                # 연쇄이동 
                #v[ni][nj] : 다음 산타 번호가 적혀있음 cur
                q.append((v[ni][nj], ni, nj,1)) # 한칸이동
                v[ni][nj] = cur # 내번호
                santa[cur] = [ni,nj] # 내좌표 갱신
        else :
            # 범위밖 -> 탈락  -  끝
            alive[cur] =0
            return


        

# 턴은 1~ M턴까지 돌아감
for turn in range(1, M+1):
    # 모두 탈락 시 alive[]:0 이면 종료 break
    if alive.count(1)==0:
        break
    # 루돌프 이동 : 가장 가까운 산타 찾기
    # 가장 먼 조건
    mn = 2*N**2
    #1번부터 p번 산타 인덱스를 모두 체크
    for idx in range(1, P+1):
        if alive[idx]==0:
            continue # 탈락한 산타 => skip
        # 산타좌표를 가져옴
        si, sj = santa[idx]
        # 거리
        dist = (ri-si)**2 + (rj-sj)**2 # 현재거리 -> 가까운 거리 min 값을 찾아야함
        if mn>dist:
            #최소값이면 새로 만들고 
            mn=dist 
            mlst=[(si, sj, idx)] # 최소거리 => 새리스트 만들어줌
        
        elif mn == dist: # 같은 최소거리 => 추가
            mlst.append((si,sj,idx))
        
    # 행큰 ->열큰
    # 내림차순
    mlst.sort(reverse = True)
    si, sj, mn_idx = mlst[0] # 가장 가까운 돌격 목표 산타 

    # 대상 산타 방향으로 루돌프가 이동
    rdi = rdj = 0
    # 산타가 더 작은 좌표에 있다면 
    # 행
    if ri > si:
        rdi = -1 # 산타가 좌표 작은 값 -1 방향 이동
    elif ri < si : 
        rdi = 1 
    
    #열
    if rj > sj:
        rdj = -1
    elif rj<sj:
        rdj = 1

    # 루돌프 현재자리 지우기
    v[ri][rj] = 0
    ri, rj = ri+rdi , rj + rdj # 루돌프를 이동
    v[ri][rj] = -1 #이동한 자리에 표시 루돌프 = -1

    # 루돌프와 산타가 충돌한 경우 산타 밀리는 처리 
    if (ri, rj) == (si, sj): # 좌표가 같다면 충돌
        score[mn_idx] += C # 산타는 C점 획득
        wakeup_turn[mn_idx] = turn+2 # 깨어날 턴 번호 저장
        move_santa(mn_idx, si, sj,rdi, rdj, C) # mn_idx 산타가 si,sj 좌표에서 rdi, rdj 방향으로 C칸만큼 밀려난다




    # 순서대로 산타 이동 : 기절하지 않은 산타 (산타의 턴 = <  현재의턴)
    for idx in range(1, P+1):
        if alive[idx] == 0:
            continue
            # 현재 턴보다 깨어날 턴이 더 크다면
        if wakeup_turn[idx] > turn :# 기절한것, 깨어나지 않은 것
            continue
        si, sj = santa[idx]

        # 루돌프에 가까워지는 방향
        mn_dist = (ri-si)**2 + (rj-sj) **2
        tlst = []

        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj=si+di,sj+dj
            dist = (ri-ni)**2 + (rj-nj)**2
            # 범위내, 산타 없고(<=0),더 짧은 거리인 경우
            if 0<=ni<N and 0<=nj<N and v[ni][nj]<=0 and mn_dist>dist:
                mn_dist = dist
                tlst.append((ni,nj,di,dj))
        if len(tlst)==0:    continue    # 이동할 위치 없음
        ni,nj,di,dj = tlst[-1]          # 마지막에 추가된(더 짧은 거리)


        # 상우하좌 순으로 최소거리 찾기
        # for di, dj in ((-1,0),(0,1),(1,0)(0,-1)):
        #     ni, nj = si+di , sj+dj# 이동할 위치 => 더 짧아지는 거리 & 중복 되면 안됨 & 범위도 이내


        #     dist = (ri-ni)**2 + (rj-nj) **2
        #     # 범위내 산타 없고 (<=0), 더 짧은 거리인경우 
        #     if 0 <= ni  < N and 0<=nj < N and v[ni][nj]<=0 and mn_dist > dist:
        #             # 더 짧은 거리인경우 갱신
        #         mn_dist = dist
        #             #방향을 저장해야
        #             #ni, nj :이동할 좌표, di,dj : 방향 
        #         tlst.append(ni,nj, di,dj)
        # if len(tlst)==0: continue # 이동할 위치가 없음
        # ni,nj, di, dj = tlst[-1] # 마지막에 추가된 (더 짧은 거리 )   
        
        
        # 루돌프와 충돌시    
        # 산타가 이동할 위치가 루돌프의 위치라면  
        if (ri, rj) == (ni,nj): # 루돌프와 충돌  반대로 튕겨나감
            score[idx] += D
            wakeup_turn[idx] = turn+2 # 깨어날 턴 번호 저장
            v[si][sj]=0
            #반대 방향 - 붙여서 반대방향으로 튕겨나간걸 표시
            move_santa(idx, ni, nj,-di, -dj, D)
        else : # 충돌안한경우 빈땅 : 좌표 갱신 , 이동처리
            v[si][sj] = 0
            v[ni][nj] = idx
            santa[idx] = [ni,nj]

                 
    # 점수 획득: alive 산타는 +1점 
    for i in range(1, P+1):
        if alive[i] == 1:
            score   [i]+=1

print(*score[1:])