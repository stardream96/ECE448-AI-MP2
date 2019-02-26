# -*- coding: utf-8 -*-
import numpy as np

def get_pent_idx_solve(pent):
    pidx = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx
def count_available(board, pent):
    m = board.shape[0]
    n = board.shape[1]
    pm = pent.shape[0]
    pn = pent.shape[1]
    count = 0
    for i in range(m-pm + 1):
        for j in range(n-pn + 1):
            this_count = 1
            for row in range(pm):
                for col in range(pn):
                    if pent[row][col] != 0:
                        if board[i+row][j+col] != 0: # Overlap
                            row = pm
                            col = pn
                            this_count = 0
                            break
            count+=this_count
    #print("count",count)
    return count
def all_transformation(this_p):
    list_p = []
    for flipnum in range(3):
        p = np.copy(this_p)
        if flipnum > 0:
            p = np.flip(this_p, flipnum-1)
        for rot_num in range(4):
            exist = False
            for trans_p in list_p:
                if np.array_equal(trans_p, p):
                    exist = True
                    break
            if exist == False :
                list_p.append(p)
            p = np.rot90(p)
    return list_p
def canput(board, x, y, pent):
    m = board.shape[0]
    n = board.shape[1]
    pm = pent.shape[0]
    pn = pent.shape[1]
    if x + pm > m or y + pn > n:
        return False
    for row in range(pm):
        for col in range(pn):
            if pent[row][col] != 0:
                if board[x+row][y+col] != 0: # Overlap
                    return False
    return True
def put(board, x, y, pent):
    number = get_pent_idx_solve(pent)
    m = board.shape[0]
    n = board.shape[1]
    pm = pent.shape[0]
    pn = pent.shape[1]
    for row in range(pm):
        for col in range(pn):
            if pent[row][col] != 0:
                board[x+row][y+col] = number
    return
# def neibor(board, x, y):
#     m = board.shape[0]
#     n = board.shape[1]
#     count = 0
#     if (x == 0):
#         count += 1
#     elif (board[x-1][y]):
#         count += 1
#     if (y == 0):
#         count += 1
#     elif (board[x][y-1]):
#         count += 1
#     if (x == m - 1):
#         count += 1
#     elif (board[x+1][y]):
#         count += 1
#     if (y == n - 1):
#         count += 1
#     elif (board[x][y+1]):
#         count += 1
#     return count==4


def check(board):
    seen = set()
    m = board.shape[0]
    n = board.shape[1]
    def area(r,c):
        if not ( 0 <= r < m and 0 <= c < n and (r, c) not in seen and board[r][c] == 0):
            return 0
        seen.add((r,c))
        return (1 + area(r+1, c) + area(r-1, c) +
                    area(r, c-1) + area(r, c+1))

    visited = np.zeros((m,n))
    result  = m*n
    for i in range(m):
        for j in range(n):

            if board[i][j] == 0 and (i,j) not in seen:
                mianji = area(i, j)
                if mianji % 5 != 0:
                    return False
    return True

def can_fill(board, i, j, trans_p):
    pm = trans_p.shape[0]
    pn = trans_p.shape[1]
    m = board.shape[0]
    n = board.shape[1]
    if (i + pm > m or j + pn > n):
        return False
    else:
        #sub_board = board[i:i+pm][j:j+pn]
        for ii in range(pm):
            for jj in range(pn):
                if (board[i+ii][j+jj] == 0 and trans_p[i][j] == 0) or (board[i+ii][j+jj] != 0 and trans_p[i][j] != 0):
                    return False
    return True
def recursive(board, remaining_orig, pents, transform):
    if len(remaining_orig) == 0:
        return ["solution:"]


    # if (check(board) == False):
    #     #print(board)
    #     return []
    # #print("remain", remaining_orig)
    remaining = remaining_orig.copy()

    seen = set()
    m = board.shape[0]
    n = board.shape[1]
    def area(r,c):
        if not ( 0 <= r < m and 0 <= c < n and (r, c) not in seen and board[r][c] == 0):
            return 0
        seen.add((r,c))
        return (1 + area(r+1, c) + area(r-1, c) +
                    area(r, c-1) + area(r, c+1))

    # visited = np.zeros((m,n))
    result  = m*n
    for j in range(n):
        for i in range(m):
        #for j in range(n):
            if board[i][j] == 0 and (i,j) not in seen:
                mianji = area(i, j)
                if mianji % 5 != 0:
                    return []
                #elif mianji == 5:
                    # canFill = False
                    # for index in remaining:
                    #     for trans_p in transform[index]:
                    #         if (canput(board, i, j, trans_p)):
                    #             print(board, "check")
                    #             recur_board = board.copy()
                    #             put(recur_board, i, j, trans_p)
                    #             recur_remain = remaining.copy()
                    #             recur_remain.remove(index)
                    #             recur_result = recursive(recur_board, recur_remain, pents, transform)
                    #             if len(recur_result) != 0:
                    #                 return recur_result
                    # return []

    #print(board)
    var = pents[remaining[0]]
    var_idx = remaining[0]
    tran_len = len(transform[var_idx])
    for index in remaining:
         trans_list = transform[index]
         cur_len = len(trans_list)
         if (cur_len <  tran_len):
             tran_len = cur_len
             var_idx = index
    trans_list = transform[var_idx]

    for i in range(m):
        for j in range(n):
            for var in trans_list:
                if canput(board, i, j, var):
                    recur_board = board.copy()
                    put(recur_board, i, j, var)
                    recur_remain = remaining.copy()
                    recur_remain.remove(var_idx)
                    recur_result = recursive(recur_board, recur_remain, pents, transform)
                    if len(recur_result) != 0:
                        recur_result.append((var, (i,j)))
                        return recur_result

    return []
def recursive_3(board, remaining_orig, pents, transform):
    if len(remaining_orig) == 0:
        return ["solution:"]


    # if (check(board) == False):
    #     #print(board)
    #     return []
    # #print("remain", remaining_orig)
    remaining = remaining_orig.copy()
    #print(board)
    seen = set()
    m = board.shape[0]
    n = board.shape[1]
    def area(r,c):
        if not ( 0 <= r < m and 0 <= c < n and (r, c) not in seen and board[r][c] == 0):
            return 0
        seen.add((r,c))
        return (1 + area(r+1, c) + area(r-1, c) +
                    area(r, c-1) + area(r, c+1))

    # visited = np.zeros((m,n))
    result  = m*n
    for j in range(n):
        for i in range(m):
        #for j in range(n):
            if board[i][j] == 0 and (i,j) not in seen:
                mianji = area(i, j)
                if mianji % 3 != 0:
                    return []
    single = False
    for trii in remaining_orig:
        tri = pents[trii]
        if tri.shape[0] == 1 or tri.shape[1] == 1 :
            single = True
    i = m - 2

    if not single:
        i = 0
        for j in range(n - 1) :
            if board[1][j] != 0 and board[1][j + 1] != 0 and board[0][j] == 0 and board[0][j + 1] == 0 :
                return []
        i = m - 1
        for j in range(n - 1) :
            if board[m - 2][j] != 0 and board[m - 2][j + 1] != 0 and board[i][j] == 0 and board[i][j + 1] == 0 :
                return []
        j = 0
        for i in range(m - 1):
            if board[i][1] != 0 and board[i + 1][1] != 0 and board[i][0] == 0 and board[i + 1][0] == 0 :
                return []
        j = n - 1
        for i in range(m - 1):
            if board[i][n - 2] != 0 and board[i + 1][n - 2] != 0 and board[i][j] == 0 and board[i + 1][j] == 0 :
                return []
        for i in range(m - 2):
            for j in range(n - 2) :
                if board[i + 2][j] != 0 and board[i + 2][j + 1] != 0 and board[i][j] != 0 and board[i][j + 1] != 0 and board[i + 1][j] == 0 and board[i + 1][j + 1] == 0 :
                    return []
                if board[i][j + 2] != 0 and board[i + 1][j + 2] != 0 and board[i][j] != 0 and board[i + 1][j] != 0 and board[i][j + 1] == 0 and board[i + 1][j + 1] == 0 :
                    return []
        #     j = n - 2
        #     if board[i + 2][j] != 0 and board[i + 2][j + 1] != 0 and board[i][j] != 0 and board[i][j + 1] != 0 and board[i + 1][j] == 0 and board[i + 1][j + 1] == 0 :
        #         return []
        #     if board[i][j] != 0 and board[i + 1][j] != 0 and board[i][j + 1] == 0 and board[i + 1][j + 1] == 0 :
        #         return []
        # i = m - 2
        # for j in range(n - 2) :
        #     if  board[i][j] != 0 and board[i][j + 1] != 0 and board[i + 1][j] == 0 and board[i + 1][j + 1] == 0 :
        #         return []
        #     if board[i][j + 2] != 0 and board[i + 1][j + 2] != 0 and board[i][j] != 0 and board[i + 1][j] != 0 and board[i][j + 1] == 0 and board[i + 1][j + 1] == 0 :
        #         return []



    #print(board)
    var = pents[remaining[0]]
    var_idx = remaining[0]

    trans_list = transform[var_idx]
    #print("line 249")
    for j in range(n):
        for i in range(m):


            for var in trans_list:
                #print("line 254", var)
                if canput(board, i, j, var):
                    recur_board = board.copy()
                    put(recur_board, i, j, var)
                    recur_remain = remaining.copy()
                    recur_remain.remove(var_idx)
                    recur_result = recursive_3(recur_board, recur_remain, pents, transform)
                    if len(recur_result) != 0:
                        recur_result.append((var, (i,j)))
                        return recur_result

    return []
def recursive_2(board, remaining_orig, pents, transform):
    if len(remaining_orig) == 0:
        return ["solution:"]


    # if (check(board) == False):
    #     #print(board)
    #     return []
    # #print("remain", remaining_orig)
    remaining = remaining_orig.copy()

    seen = set()
    m = board.shape[0]
    n = board.shape[1]
    def area(r,c):
        if not ( 0 <= r < m and 0 <= c < n and (r, c) not in seen and board[r][c] == 0):
            return 0
        seen.add((r,c))
        return (1 + area(r+1, c) + area(r-1, c) +
                    area(r, c-1) + area(r, c+1))

    # visited = np.zeros((m,n))
    # result  = m*n
    # for j in range(n):
    #     for i in range(m):
    #     #for j in range(n):
    #         if board[i][j] == 0 and (i,j) not in seen:
    #             mianji = area(i, j)
    #             if mianji % 5 != 0:
    #                 return []
    #             #elif mianji == 5:
    #                 # canFill = False
    #                 # for index in remaining:
    #                 #     for trans_p in transform[index]:
    #                 #         if (canput(board, i, j, trans_p)):
    #                 #             print(board, "check")
    #                 #             recur_board = board.copy()
    #                 #             put(recur_board, i, j, trans_p)
    #                 #             recur_remain = remaining.copy()
    #                 #             recur_remain.remove(index)
    #                 #             recur_result = recursive(recur_board, recur_remain, pents, transform)
    #                 #             if len(recur_result) != 0:
    #                 #                 return recur_result
    #                 # return []
    #
    # #print(board)
    var = pents[remaining[0]]
    var_idx = remaining[0]
    # tran_len = len(transform[var_idx])
    # for index in remaining:
    #      trans_list = transform[index]
    #      cur_len = len(trans_list)
    #      if (cur_len <  tran_len):
    #          tran_len = cur_len
    #          var_idx = index
    trans_list = transform[var_idx]
    #print(board)
    for i in range(m):
        for j in range(n):
            for var in trans_list:
                if canput(board, i, j, var):
                    recur_board = board.copy()
                    put(recur_board, i, j, var)
                    recur_remain = remaining.copy()
                    recur_remain.remove(var_idx)
                    recur_result = recursive_2(recur_board, recur_remain, pents, transform)
                    if len(recur_result) != 0:
                        recur_result.append((var, (i,j)))
                        return recur_result

    return []
def solve(board, pents):

    # m = board.shape[0]
    # n = board.shape[1]
    sol_board = 1 - board

    # create a dictonary to store all the transformations of each pentomino
    transform = {}
    for i, pentomino in enumerate(pents):
        transform[i] = all_transformation(pentomino)
    # for k, v in transform.items():
    #     print(k)
    #     print(v)
    num_pents = len(pents)
    tile = pents[0]
    size = 0
    for i in range(tile.shape[0]):
        for j in range(tile.shape[1]):
            if tile[i][j] != 0:
                size += 1
    print(size)
    remaining_orig = list(range(num_pents))
    if size == 5 :
        solution = recursive(sol_board, remaining_orig, pents, transform)
    elif size == 3:
        solution = recursive_3(sol_board, remaining_orig, pents, transform)
    elif size == 2:
        solution = recursive_2(sol_board, remaining_orig, pents, transform)
    solution.pop(0)
    # print ("solution:", solution)
    print ("board size:", board.shape)
    return solution

##########      garbage
    # remaining_orig = list(range(num_pents))
    #
    # remaining = remaining_orig.copy()
    # # find the pent with smallest possible positions
    # var = pents[remaining[0]]
    # var_br = m*n
    #
    # for index in remaining:
    #     #print("index", index)
    #     trans_list = transform[index]
    #     cur_br = 0
    #     for pentomino in trans_list:
    #         cur_br += count_available(sol_board, pentomino)
    #     if cur_br < var_br:
    #         var = pentomino
    #         var_br = cur_br
    #
    # print(var)
    # print(var_br)
    # idx = get_pent_idx_solve(var)
    #
    #
    # remaining.remove(idx)
    # print("remaining 91", remaining)
    #
    # return []

"""
This is the function you will implement. It will take in a numpy array of the board
as well as a list of n tiles in the form of numpy arrays. The solution returned
is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
where pi is a tile (may be rotated or flipped), and (rowi, coli) is
the coordinate of the upper left corner of pi in the board (lowest row and column index
that the tile covers).

-Use np.flip and np.rot90 to manipulate pentominos.

-You can assume there will always be a solution.
"""
