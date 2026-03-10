import cmd
import cowsay
import shlex


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


def parse_params(args):
    cow1_info = {}
    cow2_info = {}

    if 'reply' in args[1:]:
        ind = args.index('reply', 1)
    else:
        ind = len(args)

    params = {}
    cow1_info['msg'] = args[0]
    cow1_info['cow'] = 'default'
    for arg in args[1:ind]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            if key in ('eyes', 'tongue'):
                params[key] = value
        else:
            cow1_info['cow'] = arg
    
    cow1_info['params'] = params

    if ind == len(args) or ind == len(args) - 1:
        return cow1_info, cow2_info
    
    args = args[ind + 1:]
    
    params = {}
    cow2_info['msg'] = args[0]
    cow2_info['cow'] = 'default'
    for arg in args[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            if key in ('eyes', 'tongue'):
                params[key] = value
        else:
            cow2_info['cow'] = arg
    
    cow2_info['params'] = params
    return cow1_info, cow2_info


def cow_func(arg, func):
    try:
        arg = shlex.split(arg)
    except Exception as e:
        raise ValueError(f"Error: {e}")
        
    if not arg:
        raise ValueError("Error. No msg")
            
    cow1_info, cow2_info = parse_params(arg)
    if cow1_info['cow'] not in cowsay.list_cows():
        raise ValueError("Error. Not available cow")
            
    cow1 = func(cow1_info['msg'], cow=cow1_info['cow'], **cow1_info['params'])

    if not cow2_info:
        return cow1
        
    if cow2_info['cow'] not in cowsay.list_cows():
        raise ValueError("Error. Not available cow")
        
    cow2 = func(cow2_info['msg'], cow=cow2_info['cow'], **cow2_info['params'])
    return cow_union(cow1, cow2)


class MyCowsay(cmd.Cmd):
    prompt = 'twocows> '

    def do_cowsay(self, arg):
        """cowsay сообщение [название [параметр=значение …]] reply ответ [название [[параметр=значение …]]. Без reply будет одна корова"""
        try:
            cow = cow_func(arg, cowsay.cowsay)
            print(cow)
        except Exception as e:
            print(e)

    def do_cowthink(self, arg):
        """cowthink сообщение [название [параметр=значение …]] reply ответ [название [[параметр=значение …]]. Без reply будет одна корова"""
        try:
            cow = cow_func(arg, cowsay.cowthink)
            print(cow)
        except Exception as e:
            print(e)
        
    def do_list_cows(self, arg):
        """list_cows [путь] - выводит список доступных коров"""
        try:
            args = shlex.split(arg) if arg else []
            if args:
                cows = cowsay.list_cows(args[0])
            else:
                cows = cowsay.list_cows()
            print(cows)
        except Exception as e:
            print(f"Error: {e}")

    def do_make_bubble(self, arg):
        """make_bubble сообщение [width=число] [wrap_text=bool] — создает текстовый пузырь"""
        try:
            args = shlex.split(arg)
        except Exception as e:
            print(f"Error: {e}")
            return
            
        if not args:
            print("Error. Empty msg")
            return
        
        message = args[0]
        width = 40
        wrap_text = True
        
        for a in args[1:]:
            if '=' in a:
                key, value = a.split('=', 1)
                if key == 'width':
                    try:
                        width = int(value)
                    except ValueError:
                        print("Error. Width not a number")
                        return
                elif key == 'wrap_text':
                    wrap_text = value.lower() not in ('false', '0', 'no')
        
        print(cowsay.make_bubble(message, width=width, wrap_text=wrap_text))

    def complete_cowsay(self, text, line, begidx, endidx):
        try:
            args = shlex.split(line[:begidx])
        except Exception:
            return []
        
        cows = cowsay.list_cows()
        
        if len(args) == 2:
            return [c for c in cows if c.startswith(text)]
        
        if 'reply' in args:
            ind = args.index('reply')
            pos = len(args) - ind
            if pos == 2:
                return [c for c in cows if c.startswith(text)]
        return []

    def complete_cowthink(self, text, line, begidx, endidx):
        return self.complete_cowsay(text, line, begidx, endidx)

    def do_exit(self, arg):
        """Выход"""
        return True

    def do_EOF(self, arg):
        print()
        return True

if __name__ == '__main__':
    MyCowsay().cmdloop()