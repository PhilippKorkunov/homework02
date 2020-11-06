from typing import Tuple, List, Set, Optional

def read_sudoku(filename: str) -> List[List[str]]:
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()

def group(values: List[str], n: int) -> List[List[str]]:
    l=[]
    k=0
    for i in range(n):
        l.append([])
        for j in range(n):
            l[i].append(values[k])
            k+=1
    return l

def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    return grid[pos[0]] 


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    s=[]
    for i in range(len(grid[0])):
        s.append(grid[i][pos[1]])
    return s


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    a1=pos[0]//3
    a1*=3
    a2=pos[1]//3
    a2*=3
    b=[]
    for i in range(a1,a1+3):
        for j in range(a2,a2+3):
            b.append(grid[i][j])
    return b

def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if i==8 and j==8 and grid[i][j]!=".":
                return 0
            elif grid[i][j]==".":
                return (i, j)


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    Set={'1','2','3','4','5','6','7','8','9'}
    Net=set()
    stroka=get_row(grid, pos)
    stolb=get_col(grid, pos)
    kvadrat=get_block(grid, pos)
    Net.update(stroka)
    Net.update(stolb)
    Net.update(kvadrat)
    Set=Set-Net
    Net.clear()
    return Set


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    def f(grid: List[List[str]]):
        Setik=set()
        l=[]
        t=find_empty_positions(grid)
        if t==0:
            return bool(1)
        else:
            Setik=find_possible_values(grid,(t[0],t[1]))
            l=list(Setik)
            for i in range (len(l)):
                grid[t[0]][t[1]]=l[i]
                if f(grid)==bool(1):
                    return bool(1)
                grid[t[0]][t[1]]="."
            return bool(0)
    f(grid)
    return grid
            
                                   
        
            


def check_solution(solution: List[List[str]]) -> bool:
    a=1
    for i in range(9):
        s=[0]*10
        for j in range(9):
            if solution[i][j]!=".":
                s[int(solution[i][j])]+=1
        for k in range(1,10):
            a*=s[k]
        s=[0]*10
    if a ==1:
        for i in range (9):
            for j in range(9):
                if solution[j][i]!=".":
                    s[int(solution[j][i])]+=1
            for k in range(1,10):
                a*=s[k] 
            s=[0]*10
    if a==1:
        t=0
        p=0        
        for i in range (9):
            r=get_block(solution,(t,p))
            for j in range(9):
                s[int(r[j])]+=1
            for k in range (1,10):
                a*=s[k]
            if p==6:
                t+=3
                p=0
            else:
                p=+3
            s=[0]*10
            
    if a==1:
        return bool(1)
    else:
        return bool(0)


def generate_sudoku(N: int) -> List[List[str]]:
    import random
    grid=[]
    for i in range(9):
        grid.append([])
        for j in range(9):
            grid[i].append(".")
    grid=solve(grid)
    N=81-N
    if N<0:
        N=0
    a=0
    i=0
    j=0
    while a<N:
        if random.choice([0,1,2,3])==1:
            if grid[i][j]!=".":
                grid[i][j]="."
                a+=1
        if i==8 and j==8:
            i=0
            j=0
        elif j==8:
            i+=1
            j=0
        else:
            j+=1
    return grid
if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)