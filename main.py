from random import shuffle
from save import save_data, load_data, load_all_data

# non-windows users hail me for I bless you with this ;D
try:
    import msvcrt
    msvcrt_exists = True
except ImportError:
    msvcrt_exists = False

COWS_INDEX  = 0
BULLS_INDEX = 1
ATTS_INDEX  = 2
WINS_INDEX  = 3

try:
    HELP_PAGE = open("help", "r", encoding="utf-8").read()
except FileNotFoundError:
    HELP_PAGE = "Error: The help file may have been deleted..."
except PermissionError:
    HELP_PAGE = "Error: The help file cannot be accessed..."

def unique_code(code_len) -> str:
    """ Returns code of length CODE_LEN
        that has unique numbers """
    
    code = [str(value) for value in range(10)]

    # Shuffle randomly
    shuffle(code)
    
    return "".join(code[0:code_len])

class CowsAndBulls():
    def __init__(self, code_len: int, usr: str = "") -> None:
        self.code_len = code_len
        self.code = unique_code(code_len)
        self.guess = "N/A"
        self.usr = usr

        # Stats
        self.attempts = 0
        self.cows = 0
        self.bulls = 0
        self.won = 0

    def run(self) -> bool:
        """ Returns true if guess == code and prints how many bulls/cows """

        if self.guess == self.code:
            self.won = 1
            return True

        cows = 0
        bulls = 0
        exclude_cows = ""

        # Scan for bulls first so that no repeat cows get scanned before bulls
        for index, char in enumerate(self.guess):
            if char == self.code[index]:
                bulls += 1
                # Add char to be excluded from adding to cows variable
                exclude_cows += char

        # Scan for cows afterward
        for char in self.guess:
            if char in self.code and char not in exclude_cows:
                cows += 1
                exclude_cows += char
        
        # If cows or bulls != 0
        if cows or bulls:
            print("%d cows" % cows)
            print("%d bulls" % bulls)
        else:
            print("No matches found")

        self.cows += cows
        self.bulls += bulls

        return False

    def print_results(self) -> None:
        print("\nAttempts: %s" % self.attempts)
        print("Total bulls: %s" % self.bulls)
        print("Total cows: %s" % self.cows)
        print("Answer: %s\n" % self.code)

    def save_data(self) -> None:
        save_data(self.cows, self.bulls, self.attempts, self.won, self.usr)

    def load_data(self) -> str:
        cow, bull, att, win = load_data(self.usr)
        return ("\nStats -->\n\n"
                "Attempts: %d\n"
                "Bulls: %d\n"
                "Cows: %d\n"
                "Wins: %d\n"
            ) % (
                self.attempts + att,
                self.bulls + bull,
                self.cows + cow,
                self.won + win,
            )

    def get_input(self) -> bool:
        """ Takes user input and stores it in self.guess for use later. \n
            Returns a bool depending on if the users input is 'exit'. """
        
        guess = input("Guess: ")

        while len(guess) != self.code_len or not guess.isdigit():
            if guess == "exit":
                return True
            elif guess == "stat":
                print(self.load_data())
                guess = input("Guess: ")
                continue
            print("Error: invalid input")
            guess = input("Guess: ")

        self.guess = guess
        self.attempts += 1

        return False

class MainGame():
    def spawn_new_game(self) -> None:
        # Add newline before starting game
        print()

        # Current instance of cows and bulls game
        game = CowsAndBulls(self.code_len, self.usr)
        
        while not game.get_input():
            if game.run():
                game.print_results()
                break
        
        game.save_data()
        self.loop()

    def print_help(self) -> None:
        print(HELP_PAGE)
        
        if msvcrt_exists:
            print("Press any key to continue . . . ")
            msvcrt.getch()
        else:
            input("Press enter to continue . . . ")

        self.loop()
    
    def invalid_usr(self) -> bool:
        # Returns true if usr has ( or ) in name
        return self.usr.find("(") + self.usr.find(")") != -2

    def login(self) -> None:
        usr = self.usr if self.usr else "default"

        self.usr = input(
            "\nEnter username (Current: %s): " % usr)

        # Prevent username from containing
        # potentially broken characters
        while self.invalid_usr():
            print("Username cannot contain \"(\" or \")\".")
            self.usr = input("\nEnter username: ")
        
        self.loop()

    def edit_settings(self) -> None:
        print("\n       -- Settings --       \n")
        print(self.settings)

        option = ""

        while option not in ("1", "2"):
            # No need for a try block as it
            # only needs to be ran once to
            # see if the terminal is compatible
            if msvcrt_exists:
                option = str(msvcrt.getch(), encoding="utf-8")
            else:
                option = input()
        
        if option == "1":
            # Change self.code_len block
            print("\nChange length of the code (Current: %d):" % self.code_len)
            new_length = input("Change to: ")
            
            while new_length not in tuple(str(value) for value in range(1, 11)):
                print("Number must be between 1 and 10 and a valid integer")
                new_length = input("Change to: ")

            self.code_len = int(new_length)
        
        self.loop()
    
    def get_all_data_sorted(self, all_data: dict[str, list], value: int) -> list[tuple[str, int]]:
        sorted_list = []

        # Get users
        for user in all_data.keys():
            current_wins = all_data[user][value]
            
            # Append so that if there was no data 
            # then something still gets added
            sorted_list.append((user, current_wins))

            # Could use dict(sorted, ...)
            # but school python runs on
            # older version so this
            # is my sorting algorithm
            for index, (_, wins) in enumerate(sorted_list):
                if current_wins <= wins:
                    # Remove appended item
                    sorted_list.pop()

                    # And insert the appended item
                    # into the correct position
                    sorted_list.insert(index, (user, current_wins))
                    break

        # Reverse list because
        # it is back to front
        return sorted_list[::-1]
    
    def print_atts_lb(self, all_data: dict[str, list]) -> None:
        print("\nATTEMPTS LEADERBOARD:\n")

        sorted_list = self.get_all_data_sorted(all_data, ATTS_INDEX)
        
        for index, (user, attempts) in enumerate(sorted_list):
            # if user == ""
            # (default login)
            if not user:
                user = "default"

            print("#%d %s - %d attempts" % (index + 1, user, attempts))

    def print_cows_lb(self, all_data: dict[str, list]) -> None:
        print("\nCOWS LEADERBOARD:\n")

        sorted_list = self.get_all_data_sorted(all_data, COWS_INDEX)
        
        for index, (user, cows) in enumerate(sorted_list):
            # if user == ""
            # (default login)
            if not user:
                user = "default"

            print("#%d %s - %d cows" % (index + 1, user, cows))

    def print_bulls_lb(self, all_data: dict[str, list]) -> None:
        print("\nBULLS LEADERBOARD:\n")

        sorted_list = self.get_all_data_sorted(all_data, BULLS_INDEX)
        
        for index, (user, bulls) in enumerate(sorted_list):
            # if user == ""
            # (default login)
            if not user:
                user = "default"

            print("#%d %s - %d bulls" % (index + 1, user, bulls))

    def print_wins_lb(self, all_data: dict[str, list]) -> None:
        print("\nWINS LEADERBOARD:\n")

        sorted_list = self.get_all_data_sorted(all_data, WINS_INDEX)
        
        for index, (user, wins) in enumerate(sorted_list):
            # if user == ""
            # (default login)
            if not user:
                user = "default"

            print("#%d %s - %d wins" % (index + 1, user, wins))

    def print_lb(self) -> None:
        print("\n     -- Leaderboard --     \n")
        print("Wins Leaderboard (1)")
        print("Bulls Leaderboard (2)")
        print("Cows Leaderboard (3)")
        print("Attempts Leaderboard (4)")

        option = ""

        while option not in ("1", "2", "3", "4"):
            # No need for a try block as it
            # only needs to be ran once to
            # see if the terminal is compatible
            if msvcrt_exists:
                option = str(msvcrt.getch(), encoding="utf-8")
            else:
                option = input()
        
        self.print_lbs[option](load_all_data())

        if msvcrt_exists:
            print("\nPress any key to continue . . . ")
            msvcrt.getch()
        else:
            input("\nPress enter to continue . . . ")
        
        self.loop()

    def print_options(self) -> None:
        print("\n     -- Main Menu! --     \n")
        print("Welcome to cows and bulls!")
        print("\nOptions:\n")
        print("Start new game (1)")
        print("Help menu (2)")
        print("User settings (3)")
        print("Leaderboard (4)")
        print("Login (5)")
        print("Exit (6)")

    def stop(self) -> None:
        # Dummy function to pause execution
        print()

    def run_key(self) -> None:
        # Runs function based off of keypress
        self.functions[self.keypress]()
    
    def loop(self) -> None:
        """ Basically the main menu """
        global msvcrt_exists

        # Print all options and values to the user
        self.print_options()

        while True:
            if msvcrt_exists:
                try:
                    self.keypress = str(msvcrt.getch(), encoding="utf-8")
                except UnicodeError:
                    # If failure converting bytes to str
                    # Usually happens in IDLE
                    msvcrt_exists = False
                    continue
            else:
                self.keypress = input()

            # (1, 2, ...) in tuple incase 12, ... is inputted
            if self.keypress in ("1", "2", "3", "4", "5", "6"):
                self.run_key()
                break
            
    def __init__(self) -> None:
        # Length for codes used in cows and bulls
        # - Default value is 4
        self.code_len = 4

        # Username defaults to false
        self.usr = ""

        # Maps keypress to function
        self.functions = {
            "1": self.spawn_new_game,
            "2": self.print_help,
            "3": self.edit_settings,
            "4": self.print_lb,
            "5": self.login,
            "6": self.stop,
        }

        self.print_lbs = {
            "1": self.print_wins_lb,
            "2": self.print_bulls_lb,
            "3": self.print_cows_lb,
            "4": self.print_atts_lb,
        }

        self.settings = (
            "Code length (1)\n"
            "Exit (2)"
        )
        
        self.loop()

if __name__ == "__main__":
    main_menu = MainGame()
    
    # if on windows
    if msvcrt_exists:
        print("The game has finished, press any key to continue . . . ")
        msvcrt.getch()
    else:
        input("The game has finished, press enter to continue . . . ")
