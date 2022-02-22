import pygame

class Cell:
    def __init__(self):
        self.value = 0
        self.nextValue = 0
    def __str__(self):
        return self.value

class Lifegame:
    def __init__(self, board_size=10):
        self.init = True
        self.board_size = board_size
        self.board = self.create_board()
        self.running = True
    def create_board(self):
        board = []
        for N in range(self.board_size):
            row = []
            for M in range(self.board_size):
                row.append(Cell())
            board.append(row)
        return board

    def reset(self):
        self.init = True
        for N in range(self.board_size):
            for M in range(self.board_size):
                self.board[N][M].value = EMPTY
                self.board[N][M].nextValue = EMPTY

    def set_cell(self, i, j, opt=0):
        if opt==0:
            self.board[i][j].value = FILLED
        else:
            self.board[i][j].nextValue = FILLED
    def clear_cell(self, i, j, opt=0):
        if opt==0:
            self.board[i][j].value = EMPTY
        else:
            self.board[i][j].nextValue = EMPTY
    def keep_cell(self, i, j):
        self.board[i][j].nextValue = self.board[i][j].value

    def get_neighbor_cells(self, i, j):
        neighbors = []
        start_i = i - 1
        end_i = i + 1
        if start_i < 0:
            start_i = self.board_size - 1
        if end_i == self.board_size:
            end_i = 0
        start_j = j - 1
        end_j = j + 1
        if start_j < 0:
            start_j = self.board_size - 1
        if end_j == self.board_size:
            end_j = 0
        neighbors.append((start_i, start_j))
        neighbors.append((start_i, j))
        neighbors.append((start_i, end_j))
        neighbors.append((i, start_j))
        neighbors.append((i, end_j))
        neighbors.append((end_i, start_j))
        neighbors.append((end_i, j))
        neighbors.append((end_i, end_j))
        return neighbors  
    def is_cell_set(self, i, j):
        if self.board[i][j].value == FILLED:
            return True
        else:
            return False             
    def count_set_neighbors(self, i, j):
        count = 0
        for idx in self.get_neighbor_cells(i,j):
            ii = idx[0]
            jj = idx[1]
            if self.is_cell_set(ii, jj):
                count += 1
        return count
    def cell_next(self, i, j):
        num_set_cells = self.count_set_neighbors( i, j)
        if num_set_cells == 2:
           self.keep_cell(i,j) 
        elif num_set_cells == 3:
            self.set_cell(i,j, opt=1)
        else:
            self.clear_cell(i,j, opt=1)


    def proceed(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.cell_next(i, j)
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j].value =  self.board[i][j].nextValue




TOTAL_CELLS = 50
CELL_PIXELS = 16
PADDING = 10
BOARD_SIZE = CELL_PIXELS * TOTAL_CELLS + PADDING * 2
EMPTY = 0
FILLED = 1
WHITE = (255,255,255)
BLACK = (255,255,255)



def calcPos2_ij(mx, my):
    j = (mx - PADDING) / CELL_PIXELS
    i = (my - PADDING) / CELL_PIXELS
    return int(i), int(j)

life = Lifegame(TOTAL_CELLS)
clock = pygame.time.Clock()
SURFACE = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
fps = 60
mouse_pressed = False
mouse_clicked = False
mouse_pos_x=0
mouse_pos_y =0
initial_cells = []
while life.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            life.running = False
            break
       
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse down")
            mouse_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            print("mouse up")
            mouse_pressed = False


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                life.init = False
            elif event.key == pygame.K_r:
                life.reset()

    if mouse_pressed and life.init:
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        i, j = calcPos2_ij(mouse_pos_x, mouse_pos_y)
        print( mouse_pos_x, mouse_pos_y)
        if life.is_cell_set(i,j) == False:
            life.set_cell(i,j)
 


    # drawing the board
    for i in range(life.board_size):
        for j in range(life.board_size):
            rect = (j * CELL_PIXELS + PADDING, i * CELL_PIXELS  + PADDING, CELL_PIXELS, CELL_PIXELS)
            if life.is_cell_set(i,j):
                pygame.draw.rect(SURFACE, (240, 217,183), rect, 0)
            else:
                pygame.draw.rect(SURFACE, (180, 136, 102), rect, 0)
    
    
    pygame.display.flip()
    if life.init == False:
        life.proceed()
    clock.tick(fps)
pygame.quit()

            
