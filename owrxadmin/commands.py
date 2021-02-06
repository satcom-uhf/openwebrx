from abc import ABC, ABCMeta, abstractmethod
from getpass import getpass
from owrx.users import UserList, User, CleartextPassword
import sys
import random
import string


class Command(ABC):
    @abstractmethod
    def run(self, args):
        pass


class UserCommand(Command, metaclass=ABCMeta):
    def getUser(self, args):
        if args.user:
            return args.user
        else:
            if args.noninteractive:
                print("ERROR: User name not specified")
                sys.exit(1)
            else:
                return input("Please enter the user name: ")


class NewUser(UserCommand):
    def run(self, args):
        username = self.getUser(args)

        if args.noninteractive:
            print("Generating password for user {username}...".format(username=username))
            password = self.getRandomPassword()
            print('Password for {username} is "{password}".'.format(username=username, password=password))
            # TODO implement this threat
            print('This password is suitable for initial setup only, you will be asked to reset it on initial use.')
            print('This password cannot be recovered from the system, please note it down now.')
        else:
            password = getpass("Please enter the password for {username}: ".format(username=username))
            confirm = getpass("Please confirm password: ")
            if password != confirm:
                print("ERROR: Password mismatch.")
                sys.exit(1)

        print("Creating user {username}...".format(username=username))
        userList = UserList()
        user = User(name=username, enabled=True, password=CleartextPassword(password))
        userList.addUser(user)

    def getRandomPassword(self, length=10):
        printable = list(string.ascii_letters) + list(string.digits)
        return ''.join(random.choices(printable, k=length))


class DeleteUser(UserCommand):
    def run(self, args):
        username = self.getUser(args)
        print("Deleting user {username}...".format(username=username))
        userList = UserList()
        userList.deleteUser(username)