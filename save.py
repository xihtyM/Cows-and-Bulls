""" Module for saving and reading save-files """

save_filename = "save"

def load_data(usr: str) -> list:
    """ Returns a list of saved contents in the save file
        in order [cows, bulls, attempts, wins] """
    try:
        dat = open(save_filename, "r", encoding="utf-8").read()
    except FileNotFoundError:
        # Returns no stats for a new file
        return [0, 0, 0, 0]
    except PermissionError:
        assert False, "Error loading data, permission denied..."
    
    pos = dat.find("(%s) " % usr)

    if pos == -1:
        # Returns no stats for a new user
        return [0, 0, 0, 0]
    
    # Get the index of the end of f"{(usr)} "
    pos += len("(%s) " % usr)
    usr_dat = dat[pos:dat.find("\n", pos)].split(",")

    # ----> cows, bulls, attempts, wins
    return [int(item) for item in usr_dat]

def load_all_data() -> dict[str, list]:
    # Read lines to get names
    dat = open(save_filename, "r", encoding="utf-8").readlines()
    all_dat = {}
    
    for line in dat:        
        name_start = line.find("(") + 1
        name_end = line.find(")")

        # If name cannot be found
        # (Because +1 it is now 0 instead of -1)
        if not (name_start or name_end):
            continue
        
        name = line[name_start:name_end]
        all_dat[name] = load_data(name)

    return all_dat

print(load_all_data())

def save_data(cows: int, bulls: int, attempts: int, wins: int, usr: str) -> None:
    """ Saves data to save file """
    c_cow, c_bull, c_att, c_win = load_data(usr)
    end_stat = "(%s)" % usr

    new_cow = cows + c_cow
    new_bull = bulls + c_bull
    new_att = attempts + c_att
    new_win = wins + c_win

    end_stat += " %d,%d,%d,%d\n" % (
        new_cow, new_bull,
        new_att, new_win,
    )

    # If user is found
    if c_cow or c_bull or c_att or c_win:
        contents = open(save_filename, "r", encoding="utf-8").read()

        # Find index of user
        pos = contents.find("(%s) " % usr)

        # Add every line before to end_stat
        end_stat = contents[:pos] + end_stat

        # Get rid of old stats
        pos += contents.find("\n", pos) - pos + 1
        end_stat += contents[pos:]

        open(
            save_filename, "w",
            encoding="utf-8"
        ).write(end_stat)
    else:
        open(
            save_filename, "a",
            encoding="utf-8"
        ).write(end_stat)
