import shutil
import random
import time
import datetime
import os
import sys
from animations import printinghangman
from animations import printingskull
from termcolor import colored

global path

path = sys.argv[0].strip("hangman.py")
columns = shutil.get_terminal_size().columns


printinghangman(columns)


def main():
    life_points = 7
    same_letter = False
    total_lst = welcome()
    start_time = time.time()
    answer = total_lst[1]
    country = total_lst[0]
    answer = answer.upper()
    letters = list(answer)
    os.system("clear")
    columns = config()
    # print(answer)
    # print(columns)
    value_list = [False for x in letters]
    letters_not_in_word = []
    while False in value_list:
        columns = config()
        if same_letter:
            ouput = colored(string_secret(value_list, letters), 'red', 'on_cyan', ["bold"])
            same_letter = False
        else:
            ouput = colored(string_secret(value_list, letters), 'red', 'on_grey', ["bold"])
        print("\n\n\n\n\n\n\n")
        print(ouput.center(columns + 18))
        print("\n\n\n")
        print(string_life(life_points).center(columns))
        print("\n\n\n")
        if len(letters_not_in_word) > 0:
            print("\n\n\n")
            print("Type in a letter or whole word.".center(columns))
            print("\n\n")
            print("Letters you have already missed:".center(columns))
            print("\n", end="")
            print(", ".join(letters_not_in_word).center(columns))
            if life_points == 1:
                print("\n")
                print("You have only one life point left so here is a hint! \
You are looking for the capital city of %s...".center(columns) % country)
            user_guess = input()
        else:
            print("\n\n\n")
            print("Type in a letter or whole word.".center(columns))
            user_guess = input()
        user_guess = user_guess.upper()
        if len(user_guess) > 1:
            if user_guess == answer:
                win_game(answer, country, start_time)
            elif user_guess != answer:
                life_points = lose_hp(life_points, 2, answer)
        elif len(user_guess) == 1:
            lost_life = True
            for i in range(len(letters)):
                if letters[i] == user_guess and value_list[i]:
                    print("You have already uncovered that letter!".center(columns))
                    lost_life = False
                    same_letter = True
                if letters[i] == user_guess:
                    value_list[i] = True
                    lost_life = False
            if lost_life:
                letters_not_in_word.append(user_guess)
                life_points = lose_hp(life_points, 1, answer)
        os.system("clear")
    win_game(answer, country, start_time)


def lose_hp(life_points, points, answer):
    columns = config()
    life_points -= points
    if life_points < 1:
        os.system("clear")
        printingskull(columns)
        # printinghangman()
        os.system("clear")
        print("\n\n\n")
        print(f"Game over! The capital was {answer}!".center(columns))
        time.sleep(3)
        # os.system("clear")
        play_again()
    return life_points


def win_game(answer, country, start_time):
    columns = config()
    os.system("clear")
    print("\n")
    print("\n\n\n")
    print("Congratulations! You guessed the whole word!".center(columns))
    print(f"{answer} is the capital of {country}.".center(columns))
    elapsed_time = round((time.time() - start_time), 3)
    print(("Your guessing time was " + str(elapsed_time) + " seconds.").center(columns))
    user_name = input("Type in your name to save your score on the score board: ".center(columns))
    os.system("clear")
    with open(path + "high_scores.txt", "a+") as hs_f:
        date = datetime.datetime.now()
        hs_input = [str(elapsed_time), user_name, str(date.strftime("%x")), answer]
        hs_f.write(" | ".join(hs_input) + "\n")
        hs_f.seek(0)
        r = hs_f.readlines()
        hs_lst = [x.split("|") for x in r]
        # print(hs_lst)
        # for i in range(len(hs_lst)):
        #    print(hs_lst[i][0])
        #    hs_lst[i][0] = float(hs_lst[i][0])
        hs_lst = sorted(hs_lst, key=lambda x: float(x[0]))
        for i in range(len(hs_lst)):
            hs_lst[i][0] = str(hs_lst[i][0]) + " sec"
        print(":::HIGH SCORES:::".center(columns))
        print("\n")
        if len(hs_lst) > 10:
            for i in range(10):
                print(str(i+1) + ".   " + " | ".join(hs_lst[i]).center(columns))
        else:
            for i in range(range(len(hs_lst))):
                print(str(i+1) + ".   " + " | ".join(hs_lst[i]).center(columns))

    play_again()


def play_again():
    columns = config()
    print("\n\n\n")
    play_again = input("Do you want to play again? [Y/N] ".center(columns))
    play_again.lower()
    while play_again == "y":
        main()
        play_again = input("Do you want to play again? [Y/N] ".center(columns))
    exit()


def string_life(life_points):
    life = ""
    for i in range(life_points):
        life += "\u273A "
    return life


def string_secret(value_list, letters):
    word = ""
    for i in range(len(value_list)):
        if not value_list[i]:
            word += "  _  "
        else:
            if letters[i] == " ":
                word += "  \u2588  "
            else:
                word += "  " + letters[i] + "  "
    return word


def config():
    columns = shutil.get_terminal_size().columns
    return columns


def welcome():
    os.system("clear")
    columns = config()
    print("\n\n\n")
    print("Welcome back to hangman!".center(columns))
    print("The program will now randomly select one of world's capitals.".center(columns))
    time.sleep(2.4)
    with open(path + "countries-capitals.txt", "r") as f:
        contents = f.readlines()
    capital_lst = [x for x in contents]
    choice = random.choice(capital_lst)
    total_lst = choice.split("|")
    for i in range(len(total_lst)):
        total_lst[i] = total_lst[i].strip()
    x = ""
    for i in range(len(total_lst[1])):
        os.system("clear")
        x += ". "
        print("\n\n\n\n\n\n\n\n " + x.center(columns))
        time.sleep(0.3)
    time.sleep(0.1)
    os.system("clear")
    print("\n\n\n\n\n\n\n")
    print(("_ " * len(total_lst[1])).center(columns))
    time.sleep(0.1)
    os.system("clear")
    print("\n\n\n\n\n\n\n")
    print((" _ " * len(total_lst[1])).center(columns))
    time.sleep(0.3)
    return total_lst


main()
