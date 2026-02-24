import cowsay, argparse


def parse_args():
    parser = argparse.ArgumentParser(description="two cows say something")
    parser.add_argument('-e', default=cowsay.Option.eyes)
    parser.add_argument('-f', default='default')
    parser.add_argument('-n', action="store_false")
    parser.add_argument('-T', default=cowsay.Option.tongue)
    parser.add_argument('-W', type=int, default=40)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", action="store_const", const="b", help="Borg", dest="Mode")
    group.add_argument("-d", action="store_const", const="d", help="dead", dest="Mode")
    group.add_argument("-g", action="store_const", const="g", help="greedy", dest="Mode")
    group.add_argument("-p", action="store_const", const="p", help="paranoid", dest="Mode")
    group.add_argument("-s", action="store_const", const="s", help="stoned", dest="Mode")
    group.add_argument("-t", action="store_const", const="t", help="tired", dest="Mode")
    group.add_argument("-w", action="store_const", const="w", help="wired", dest="Mode")
    group.add_argument("-y", action="store_const", const="y", help="young", dest="Mode")

    parser.add_argument('-E', default=cowsay.Option.eyes)
    parser.add_argument('-F', default='default')
    parser.add_argument('-N', action="store_false")
    
    parser.add_argument("message1", default="", nargs='?')
    parser.add_argument("message2", default="", nargs='?')

    return parser.parse_args()


def cow_union(cow1, cow2):
    cow1 = cow1.split('\n')
    cow2 = cow2.split('\n')
    if len(cow1) < len(cow2):
        cow1 = [''] * (len(cow2) - len(cow1)) + cow1
    elif len(cow2) < len(cow1):
        cow2 = [''] * (len(cow1) - len(cow2)) + cow2

    max_len = max(len(i) for i in cow1)
    for ind, val in enumerate(cow1):
        cow1[ind] = val + ' ' * (max_len - len(val))
    cow_res = list(i[0] + i[1] for i in zip(cow1, cow2))
    return '\n'.join(cow_res)


def main():
    args = parse_args()
    cow1 = cowsay.cowsay(args.message1, args.f, args.Mode, args.e, args.T, args.W, args.n)
    cow2 = cowsay.cowsay(args.message2, args.F, args.Mode, args.E, args.T, args.W, args.N)
    cow_res = cow_union(cow1, cow2)
    print(cow_res)


if __name__ == "__main__":
    main()
