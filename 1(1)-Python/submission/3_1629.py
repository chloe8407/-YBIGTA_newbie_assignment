# lib.py의 Matrix 클래스를 참조하지 않음
import sys


"""
TODO:
- fast_power 구현하기 
"""


def fast_power(base: int, exp: int, mod: int) -> int:
    """
    빠른 거듭제곱 알고리즘 구현
    분할 정복을 이용, 시간복잡도 고민!
    """
    if exp == 0:
        return 1 % mod
    
    half = fast_power(base, exp //2, mod)
    half = (half*half) % mod

    if exp % 2 == 0:
        return half
    else:
        return (half * base) % mod
    
    """
    지수가 매우 큰 경우를 대비해서  지수를 절반으로 쪼개는 재귀의 형태

    half: 지수를 절반으로 나눈 후, 그 값을 다시 저장, 그 값을 다시 곱해서 나눈 값 반환

    예시: 2^10 => (2^5)*(2^5)
    """


def main() -> None:
    A: int
    B: int
    C: int
    A, B, C = map(int, input().split()) # 입력 고정
    
    result: int = fast_power(A, B, C) # 출력 형식
    print(result) 

if __name__ == "__main__":
    main()
