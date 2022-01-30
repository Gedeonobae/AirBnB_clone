#!/usr/bin/python3
import cmd
import sys


class HBNBcommand(cmd.Cmd):
    """Entry point of the command interpreter"""
    intro = None
    prompt = '(hbnb) '
    file = None

    def do_quit(self, arg):
        """ Method to exit the console """
        return True

    def do_EOF(self, arg):
        """ Method to exit when EOF is reached """
        return True

    def emptyline(self):
        """Called ehen an empty line is entered in response tothe prompt.

        If this method is overridden, it repeats the last nn empty

        """
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')


if __name__ == '__main__':
    HBNBcommand().cmdloop()
