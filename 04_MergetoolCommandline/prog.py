import cmd
import cowsay
import shlex


class MyCowsay(cmd.Cmd):
    prompt = 'twocows> '

    def do_cowsay(self, arg):
        pass

    def do_cowthink(self, arg):
        pass

    def do_list_cows(self, arg):
        """list_cows [путь] - выводит список доступных коров"""
        args = shlex.split(arg) if arg else []
        try:
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
        pass    

    def complete_cowthink(self, text, line, begidx, endidx):
        pass


if __name__ == '__main__':
    MyCowsay().cmdloop()