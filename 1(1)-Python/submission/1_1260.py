from __future__ import annotations
import copy
from collections import deque
from collections import defaultdict
from typing import DefaultDict, List


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
    def __init__(self, n: int) -> None:
        """
        그래프 초기화
        n: 정점의 개수 (1번부터 n번까지)
        """
        self.n = n
        self.near: DefaultDict[int, list[int]] = defaultdict(list)

        for i in range(1, n+1):
            self.near[i]
        """
        정점 개수 저장 후 리스트 형태 구현

        Arg:
            near: 인접 정점을 리스트 형태로 표현
        
        """
    

    
    def add_edge(self, u: int, v: int) -> None:
        """
        양방향 간선 추가
        """
        self.near[u].append(v)
        self.near[v].append(u)
        self.near[u].sort()
        self.near[v].sort()
        """
        u번 정점의 인접 리스트에 v를 추가 후 오름차순 정렬
        v번 정점의 인접 리스트에 u를 추가 후 오름차순 정렬
        """

    
    def dfs(self, start: int) -> list[int]:
        """
        깊이 우선 탐색 (DFS)
        
        구현 방법 선택:
        1. 재귀 방식: 함수 내부에서 재귀 함수 정의하여 구현
        2. 스택 방식: 명시적 스택을 사용하여 반복문으로 구현
        """
        visit = set()
        result=[]
        stack =[start]

        while stack:
            node = stack.pop()

            if node in visit:
                continue
            
            visit.add(node)
            result.append(node)

            for adj in reversed(self.near[node]):
                if adj not in visit:
                    stack.append(adj)

        return result
        """
        스택 방식 선택

        Arg:
            visit: 방문한 정점
        
        return: 
            result: 방문한 정점을 방문 순서대로 기록
        """
    
    
    def bfs(self, start: int) -> list[int]:
        """
        너비 우선 탐색 (BFS)
        큐를 사용하여 구현
        """
        visit=set()
        result=[]
        queue=deque([start])
        visit.add(start)

        while queue:
            node = queue.popleft()
            result.append(node)

            for adj in self.near[node]:
                if adj not in visit:
                    visit.add(adj)
                    queue.append(adj)

        return result
        """
        Arg:
            visit: 방문한 정점
        
        return: 
            result: 방문한 정점을 방문 순서대로 기록
        """
        
    
    def search_and_print(self, start: int) -> None:
        """
        DFS와 BFS 결과를 출력
        """
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))



from typing import Callable
import sys


"""
-아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    lines: list[str] = sys.stdin.readlines()

    N, M, V = intify(lines[0])
    
    graph = Graph(N)  # 그래프 생성
    
    for i in range(1, M + 1): # 간선 정보 입력
        u, v = intify(lines[i])
        graph.add_edge(u, v)
    
    graph.search_and_print(V) # DFS와 BFS 수행 및 출력


if __name__ == "__main__":
    main()
