import random
import os
import time

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def get_number_color(number):
        colors = {
            '1': Colors.BLUE,
            '2': Colors.GREEN,
            '3': Colors.RED,
            '4': Colors.PURPLE,
            '5': Colors.YELLOW,
            '6': Colors.CYAN,
            '7': Colors.WHITE,
            '8': Colors.GRAY
        }
        return colors.get(number, Colors.WHITE)

class Minesweeper:
    def __init__(self, width=10, height=10, mines_count=15):
        self.width = width
        self.height = height
        self.mines_count = min(mines_count, width * height - 1)
        self.board = []
        self.visible = []
        self.game_over = False
        self.win = False
        self.flags_count = 0
        self.initialize_boards()
        
    def initialize_boards(self):
        self.board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.visible = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        mines_placed = 0
        while mines_placed < self.mines_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            if self.board[y][x] != 'X':
                self.board[y][x] = 'X'
                mines_placed += 1
        
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 'X':
                    count = self.count_adjacent_mines(x, y)
                    if count > 0:
                        self.board[y][x] = str(count)
    
    def count_adjacent_mines(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[ny][nx] == 'X':
                        count += 1
        return count
    
    def show_explosion_animation(self, explosion_x, explosion_y):
        frames = [
            self.create_explosion_frame(1, explosion_x, explosion_y),
            self.create_explosion_frame(2, explosion_x, explosion_y),
            self.create_explosion_frame(3, explosion_x, explosion_y),
            self.create_explosion_frame(2, explosion_x, explosion_y),
            self.create_explosion_frame(1, explosion_x, explosion_y)
        ]
        
        for frame in frames:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(frame)
            time.sleep(0.3)
    
    def create_explosion_frame(self, stage, center_x, center_y):
        result = []
        result.append(f"{Colors.BOLD}{Colors.RED}>>> ВЗРЫВ! <<<{Colors.END}\n")
        

        result.append(f"{Colors.YELLOW}   ")
        for i in range(self.width):
            result.append(f"{i:2}")
        result.append(f"{Colors.END}\n")
      
        result.append(f"{Colors.YELLOW}   +{'-' * (self.width * 2)}+{Colors.END}\n")
        
        for y in range(self.height):
            result.append(f"{Colors.YELLOW}{y:2} |{Colors.END}")
            for x in range(self.width):
                distance = max(abs(x - center_x), abs(y - center_y))
                
                if distance < stage:
                    if distance == 0:
                        result.append(f"{Colors.BOLD}{Colors.RED}*{Colors.END}")
                    else:
                        chars = ['@', '#', '%', '&']
                        result.append(f"{Colors.RED}{chars[stage % len(chars)]}{Colors.END}")
                else:
                    cell = self.visible[y][x]
                    if cell == 'F':
                        result.append(f"{Colors.RED}F{Colors.END}")
                    elif cell == '.':
                        result.append(f"{Colors.GRAY}.{Colors.END}")
                    elif cell == ' ':
                        result.append(" ")
                    elif cell.isdigit():
                        color = Colors.get_number_color(cell)
                        result.append(f"{color}{cell}{Colors.END}")
                    else:
                        result.append(cell)
                result.append(" ")
            result.append(f"{Colors.YELLOW}|{Colors.END}\n")
        
        result.append(f"{Colors.YELLOW}   +{'-' * (self.width * 2)}+{Colors.END}\n")
        
        messages = [
            f"{Colors.RED}MINE WANNA KABOOM!{Colors.END}"
        ]
        result.append(f"{messages[stage % len(messages)]}\n")
        
        return "".join(result)
    
    def print_board(self, show_mines=False):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{Colors.BOLD}{Colors.CYAN} CONSOLE MINESWEEPER{Colors.END}")
        print(f"{Colors.GRAY}Size: {self.width}x{self.height} | Mines: {self.mines_count} | Flags: {self.flags_count}{Colors.END}")
        print()
        
        print(f"{Colors.YELLOW}   ", end="")
        for i in range(self.width):
            print(f"{i:2}", end="")
        print(Colors.END)
        
        print(f"{Colors.YELLOW}   +{'-' * (self.width * 2)}+{Colors.END}")
        
        for y in range(self.height):
            print(f"{Colors.YELLOW}{y:2} |{Colors.END}", end="")
            for x in range(self.width):
                cell = self.visible[y][x]
                if show_mines and self.board[y][x] == 'X':
                    print(f"{Colors.RED}*{Colors.END}", end="")
                elif cell == 'F':
                    print(f"{Colors.RED}F{Colors.END}", end="")
                elif cell == '.':
                    print(f"{Colors.GRAY}.{Colors.END}", end="")
                elif cell == ' ':
                    print(" ", end="")
                elif cell.isdigit():
                    color = Colors.get_number_color(cell)
                    print(f"{color}{cell}{Colors.END}", end="")
                else:
                    print(cell, end="")
                print(" ", end="")
            print(f"{Colors.YELLOW}|{Colors.END}")
        
        print(f"{Colors.YELLOW}   +{'-' * (self.width * 2)}+{Colors.END}")
        print()
        
        if self.game_over:
            if self.win:
                print(f"{Colors.BOLD}{Colors.GREEN}*** YOU WIN! PERFECT! ***{Colors.END}")
            else:
                print(f"{Colors.BOLD}{Colors.RED}*** BOOM! ***{Colors.END}")
        else:
            print(f"{Colors.CYAN}Commands: r x y - open, f x y - flag, q - exit{Colors.END}")
    
    def reveal(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            print(f"{Colors.RED}Unknown cordinates!{Colors.END}")
            return False
        
        if self.visible[y][x] != '.':
            print(f"{Colors.YELLOW}This is place is open!{Colors.END}")
            return False
        
        if self.board[y][x] == 'X':
            self.show_explosion_animation(x, y)
            self.game_over = True
            self.win = False
            return True
          
        stack = [(x, y)]
        
        while stack:
            cx, cy = stack.pop()
            
            if not (0 <= cx < self.width and 0 <= cy < self.height):
                continue
                
            if self.visible[cy][cx] != '.':
                continue
            
            self.visible[cy][cx] = self.board[cy][cx]
            
            if self.board[cy][cx] == ' ':
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = cx + dx, cy + dy
                        if (0 <= nx < self.width and 0 <= ny < self.height and 
                            self.visible[ny][nx] == '.'):
                            stack.append((nx, ny))
        
        return True
    
    def toggle_flag(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            print(f"{Colors.RED}Unknown cordinates!{Colors.END}")
            return
        
        if self.visible[y][x] == '.':
            self.visible[y][x] = 'F'
            self.flags_count += 1
        elif self.visible[y][x] == 'F':
            self.visible[y][x] = '.'
            self.flags_count -= 1
        else:
            print(f"{Colors.YELLOW}Can't place flag on opened place!{Colors.END}")
    
    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 'X' and self.visible[y][x] == '.':
                    return False
        
        correct_flags = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 'X' and self.visible[y][x] == 'F':
                    correct_flags += 1
        
        if correct_flags == self.mines_count:
            self.game_over = True
            self.win = True
            return True
        return False
    
    def play(self):
        print(f"{Colors.BOLD}{Colors.GREEN}Welcome to the Console Minesweeper!{Colors.END}")
        print(f"{Colors.CYAN}Here your help:{Colors.END}")
        print(f"  {Colors.YELLOW}r x y{Colors.END} - open here (x, y)")
        print(f"  {Colors.YELLOW}f x y{Colors.END} - place/remove flag")
        print(f"  {Colors.YELLOW}q{Colors.END} - exit")
        print()
        input(f"{Colors.GRAY}Press Enter to start...{Colors.END}")
        
        while not self.game_over:
            self.print_board()
            
            try:
                command = input(f"{Colors.CYAN}Enter the command: {Colors.END}").strip().split()
                
                if not command:
                    continue
                
                if command[0] == 'q':
                    print(f"{Colors.YELLOW}Exit...{Colors.END}")
                    break
                
                if len(command) != 3:
                    print(f"{Colors.RED}Error! user: r X Y or f X Y{Colors.END}")
                    continue
                
                action, x_str, y_str = command
                
                try:
                    x, y = int(x_str), int(y_str)
                except ValueError:
                    print(f"{Colors.RED}Координаты должны быть числами!{Colors.END}")
                    continue
                
                if action == 'r':
                    success = self.reveal(x, y)
                    if success and not self.game_over:
                        self.check_win()
                    
                elif action == 'f':
                    self.toggle_flag(x, y)
                    self.check_win()
                    
                else:
                    print(f"{Colors.RED}Unknown command! Use 'r' or 'f'{Colors.END}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Exit..{Colors.END}")
                break
        
        if self.game_over:
            self.print_board(show_mines=True)

def main():
    print(f"{Colors.BOLD}{Colors.CYAN} SETTINGS{Colors.END}")
    print()
    
    try:
        width = int(input(f"{Colors.YELLOW}Weight (by default 10): {Colors.END}") or "10")
        height = int(input(f"{Colors.YELLOW}Height (by default 10): {Colors.END}") or "10")
        mines = int(input(f"{Colors.YELLOW}Value of mines (by default 15): {Colors.END}") or "15")
        
        if width <= 0 or height <= 0 or mines <= 0:
            print(f"{Colors.RED}Don't cheat on my game!{Colors.END}")
            return
        
        max_mines = width * height - 1
        if mines > max_mines:
            print(f"{Colors.YELLOW}a lot of mines! Placed {max_mines} mines.{Colors.END}")
            mines = max_mines
        
        game = Minesweeper(width, height, mines)
        game.play()
        
    except ValueError:
        print(f"{Colors.RED}Error! Setup by default.{Colors.END}")
        game = Minesweeper()
        game.play()

if __name__ == "__main__":
    main()
