from pipenv.patched.notpip._internal.cli.base_command import Command
from pipenv.patched.notpip._internal.cli.status_codes import SUCCESS
from pipenv.patched.notpip._internal.exceptions import CommandError
from pipenv.patched.notpip._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from optparse import Values
    from typing import List


class HelpCommand(Command):
    """Show help for commands"""

    usage = """
      %prog <command>"""
    ignore_require_venv = True

    def run(self, options, args):
        # type: (Values, List[str]) -> int
        from pipenv.patched.notpip._internal.commands import (
            commands_dict,
            create_command,
            get_similar_commands,
        )

        try:
            # 'pip help' with no args is handled by pip.__init__.parseopt()
            cmd_name = args[0]  # the command we need help for
        except IndexError:
            return SUCCESS

        if cmd_name not in commands_dict:
            guess = get_similar_commands(cmd_name)

            msg = [f'unknown command "{cmd_name}"']
            if guess:
                msg.append(f'maybe you meant "{guess}"')

            raise CommandError(' - '.join(msg))

        command = create_command(cmd_name)
        command.parser.print_help()

        return SUCCESS
