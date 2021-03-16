import os
import sys
import re
import shutil
import unicodedata


class PlaceHolderInfo:
    def __init__(self):
        self.x: int
        self.y: int
        self.length: int


class Anal:
    def __init__(self, file_name: str):
        # read template
        self.template: str = ''
        with open(file_name, 'r') as f:
            self.template = f.read()

        self.place_holders: list = self.get_place_holders()
        self.init_draw()

    def draw(self, *texts: list) -> None:
        if len(texts) != len(self.place_holders):
            raise Exception(
                'The number of placeholders and arguments do not match.')

        # replace place holder
        for i, place_holder in enumerate(self.place_holders):
            max_size: int = self.get_window_width() \
                - place_holder.x \
                - self.get_text_length(texts[i])
            value: str = texts[i][:max_size] + '\033[0m'
            if place_holder.length == 0:
                value = value.ljust(
                    max_size + self.get_text_length(value), ' ')
            else:
                value = value.ljust(place_holder.length, ' ')

            sys.stdout.write('\033[%dC\033[%dB%s' % (
                place_holder.x,
                place_holder.y,
                value,
            ))
            self.move_init_position()

        sys.stdout.flush()

    def init_draw(self) -> None:
        template: str = self.template
        for place_holder in self.place_holders:
            template = re.sub(
                r'\$[0-9\-]+',
                ' ' * place_holder.length,
                template,
                1,
            )
        os.system('clear')
        sys.stdout.write(template)

    def move_init_position(self) -> None:
        sys.stdout.write('\033[%dA\033[%dD' % (
            len(self.template.split('\n')) + 1,
            self.get_window_width(),
        ))
        return

    def get_place_holders(self) -> list:
        result: list = []

        # get place holder size
        place_holders_size: list = []
        for place_holder_str in re.findall(r'\$[0-9\-]+', self.template):
            detail: re.Match = re.search(r'\d+', place_holder_str)
            if detail is None:
                place_holders_size.append(0)
            else:
                place_holders_size.append(int(detail.group()))

        # get place holder position
        for line_pos, line in enumerate(self.template.split('\n')):
            if '$' not in line:
                continue

            columns: list = line.split('$')[:-1]
            bias: int = 0
            for col in columns:
                place_holder_info: PlaceHolderInfo = PlaceHolderInfo()
                place_holder_info.x = self.get_text_length(col) + bias
                place_holder_info.y = line_pos
                place_holder_info.length = place_holders_size.pop(0)
                result.append(place_holder_info)

                bias = place_holder_info.x + place_holder_info.length - 1

        return result

    def get_window_width(self) -> int:
        return shutil.get_terminal_size().columns

    def get_text_length(self, text: str) -> int:
        result: int = 0
        for ch in self.clear_ansi_escape(text):
            if unicodedata.east_asian_width(ch) in 'FWA':
                result += 2
            else:
                result += 1
        return result

    def clear_ansi_escape(self, text: str) -> str:
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        result: str = ansi_escape.sub('', text)
        return result
