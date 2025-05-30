import abc, sys

from ..feed import Command, Group, Implementation, Interface
from ..xml import from_xml, to_xml

def _find_group(feed, arch, commands):
    commands = sorted(commands, key=lambda command: command.name)

    for child in feed.children:
        if not isinstance(child, Group):
            continue

        if child.arch != arch:
            continue

        group_commands = sorted(child.get_commands(), key=lambda command: command.name)

        if group_commands != commands:
            continue

        return child

    return None

class App(abc.ABC):
    def main(self):
        _, command, *args = sys.argv

        match command:
            case 'update':
                self.update(*args)
            case _:
                raise Exception(f'Unknow subcomand: {command}')

    def update(self, file_path):
        try:
            with open(file_path, 'r') as file:
                feed = from_xml(file)
        except FileNotFoundError:
            feed = Interface()

        existing_implementations_id = set([implementation.id for implementation in feed.implementations()])

        for implementation_id, implementation_data in self.implementations():
            if implementation_id in existing_implementations_id:
                continue

            implementation = self.implementation(implementation_data)

            group = _find_group(feed, implementation.arch, implementation.get_commands())

            if group is None:
                group = Group(*implementation.get_commands(), arch=implementation.arch)

                feed.append(group)

            group.append(Implementation(
                *filter(lambda child: not isinstance(child, Command), implementation.children),
                id=implementation.id,
                released=implementation.released,
                version=implementation.version,
            ))

            # Save inside the loop to save progress in case later archive download fail
            with open(file_path, 'w') as file:
                file.write(to_xml(feed, indent='    ').read())

    @abc.abstractmethod
    def implementations(self):
        pass

    @abc.abstractmethod
    def implementation(self, data):
        pass
