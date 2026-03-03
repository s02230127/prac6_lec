import random
import sys
import urllib.request
import cowsay


def bullscows(guess: str, secret: str) -> tuple[int, int]:
    cows = 0
    bulls = 0
    for i, j in zip(secret, guess):
        if i == j:
            bulls += 1
    guess_dict = {}
    secret_dict = {}
    for i in guess:
        guess_dict[i] = 1 + guess_dict.get(i, 0)

    for i in secret:
        secret_dict[i] = 1 + secret_dict.get(i, 0)

    for i in guess_dict:
        cows += min(secret_dict.get(i, 0), guess_dict.get(i))

    cows -= bulls
    return bulls, cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    word = random.choice(words)
    tries = 0
    while True:
        tries += 1
        guess = ask("Введите слово: ", words)
        b, c = bullscows(guess, word)
        inform("Быки: {}, Коровы: {}", b, c)
        if b == len(word):
            return tries
        

def ask(prompt: str, valid: list[str] = None) -> str:
    if not valid:
        print(cowsay.cowsay(prompt))
        return input().strip().lower()
    else:
        while True:
            print(cowsay.cowsay(prompt))
            word = input().strip().lower()
            if word in valid:
                break
            print(cowsay.cowsay("Wrong word. Try again"))

        return word


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay.cowsay(format_string.format(bulls, cows)))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit("Error. Not enough parameters")
    dictionary = sys.argv[1]
    length = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
    if dictionary.startswith("https://") or dictionary.startswith("http://"):
        try:
            with urllib.request.urlopen(dictionary) as request:
                words_all = request.read().decode("utf-8", errors='ignore')
        except Exception:
            sys.exit("Error. Problem with URL")

    else:
        try:
            with open(dictionary) as file:
                words_all = file.read()
        except Exception:
            sys.exit("Error. Problem with txt file")


    words = [i.lower() for i in words_all.split() if len(i) == length]
    if not words:
        sys.exit(f"Error. No words with len {length} in {dictionary}")
    tries = gameplay(ask, inform, words)
    print(f"Number of attempts: {tries}")