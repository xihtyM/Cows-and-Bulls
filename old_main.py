from random import randint

# non-windows users hail me for I bless you with this ;D
try:
    import msvcrt
    msvcrt_exists = True
except ImportError:
    msvcrt_exists = False

# Length for codes used in cows and bulls
# - Default value is 4
CODE_LEN = 4

def unique_code() -> int:
    """ Returns code of length CODE_LEN
        that has unique numbers """
    
    # Using 1023, 9876 for performance as
    # 1023 is the smallest valid integer
    # and 9876 is the largest valid integer
    code = randint(1023, 9876)

    # If code repeats a number,
    # assign it a new random integer
    # between 1023 and 9876
    while len(set(str(code))) != CODE_LEN:
        code = randint(1023, 9876)
    
    return code

class CowsAndBulls():
    def __init__(self) -> None:
        self.code = str(unique_code())
        self.guess = "N/A"

        # Stats
        self.attempts = 0
        self.cows = 0
        self.bulls = 0

    def run(self) -> bool:
        """ Returns true if guess == code and prints how many bulls/cows """

        if self.guess == self.code:
            return True

        cows = 0
        bulls = 0
        exclude_cows = ""

        for index, char in enumerate(self.guess):
            if char == self.code[index]:
                bulls += 1
                exclude_cows += char
                continue

            if char in self.code and char not in exclude_cows:
                cows += 1
                exclude_cows += char
        
        if cows or bulls:
            print("%d cows" % cows)
            print("%d bulls" % bulls)
        else:
            print("No matches found")

        self.cows += cows
        self.bulls += bulls

        return False

    def print_results(self) -> None:
        print("Attempts: %s" % self.attempts)
        print("Total bulls: %s" % self.bulls)
        print("Total cows: %s" % self.cows)
        print("Answer: %s\n" % self.code)

    def get_input(self) -> bool:
        """ Takes user input and stores it in self.guess for use later. \n
            Returns a bool depending on if the users input is 'exit'. """
        
        guess = input("Guess: ")

        while len(guess) != CODE_LEN or not guess.isdigit():
            if guess == "exit":
                return True
            print("Error: invalid input")
            guess = input("Guess: ")

        self.guess = guess
        self.attempts += 1

        return False


if __name__ == "__main__":
    game = CowsAndBulls()
    
    # quits when "exit" is typed
    while not game.get_input():
        # if input is correct number
        if game.run():
            print("\nWell done, you can find your results below\n")
            game.print_results()
            break
    
    # if on windows
    if msvcrt_exists:
        print("The game has finished, press any key to continue . . . ")
        msvcrt.getch()
    else:
        input("The game has finished, press enter to continue . . . ")
