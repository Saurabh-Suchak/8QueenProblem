import heapq

class Node:
    def __init__(self, board, h, g):
        self.board = board
        self.h = h
        self.g = g
        self.f = self.h + self.g
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(tuple(self.board))

 # checks if any pair of queens is attacking   
def is_goal(node):
    for i in range(len(node.board)):
        for j in range(i + 1, len(node.board)):
            if node.board[i] == node.board[j]:
                return False
            if abs(node.board[i] - node.board[j]) == abs(i - j):
                return False
    return True


# generate successors of each state by moving each queen by a row and appneding to the successor list 

def get_successors(node):
    successors = []
    for i in range(len(node.board)):
        for j in range(len(node.board)):
            if j != node.board[i]:
                new_board = list(node.board)
                new_board[i] = j
                successors.append(Node(new_board, calculate_h(new_board), node.g + 1))
    return successors

# calculate the heuristc value (no. of pairs of queens attacking)
def calculate_h(board):
    h = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                h += 1
    return h


# main fun that implements a* - initialise a heap to push all states in it, then it evaluates f and generates succussors , if successors f less then push in open set and pop current
def a_star(start):
    heap = [start]
    closed_set = set()
    step = 0
    while heap:
        step += 1
        print(f"Step {step}:")
        current = heapq.heappop(heap)
        print("Board state:", current.board)
        print("Heuristic value:", current.h)
        if is_goal(current):
            return current.board
        closed_set.add(current)
        for successor in get_successors(current):
            if successor in closed_set:
                continue
            if successor.f < current.f or successor not in heap:
                heapq.heappush(heap, successor)
    return None

def get_board_from_user():
    board = []
    for i in range(8):
        while True:
            try:
                row_index = int(input(f"Enter the column index of the queen for row {i}: "))
                if row_index < 0 or row_index > 7:
                    print("Row index must be between 0 and 7.")
                else:
                    board.append(row_index)
                    break
            except ValueError:
                print("Please enter an integer between 0 and 7.")
    return board

board = get_board_from_user()
solution = a_star(Node(board, calculate_h(board), 0))
if solution:
    print("Solution found:")
    for i in range(len(solution)):
        row = ['.'] * 8
        row[solution[i]] = 'Q'
        print(' '.join(row))
else:
    print("No solution found.")