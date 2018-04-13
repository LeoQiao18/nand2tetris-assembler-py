class Parser():
    def __init__(self, fname):
        self.f = open(fname)
        self.current_line = None
        self.next_line = self.f.readline()

        self.command_type = None

        # A_COMMAND or L_COMMAND
        self.symbol = None

        # C_COMMAND
        self.dest = None
        self.comp = None
        self.jump = None

    def has_more_commands(self):
        return bool(self.next_line)

    def advance(self):
        self.current_line = self.next_line
        self.next_line = self._rm_extra(self.f.readline())
        self.command_type = self.test_command_type()
        self.parse_command()

    def test_command_type(self):
        if self.current_line:
            if self.current_line[0] == "@":
                return "A_COMMAND"
            if self.current_line[0] == "(":
                return "L_COMMAND"
            return "C_COMMAND"
        return None

    def parse_command(self):
        if self.command_type == "A_COMMAND":
            self.parse_a_command()
        if self.command_type == "C_COMMAND":
            self.parse_c_command()
        if self.command_type == "L_COMMAND":
            self.parse_l_command()

    def parse_a_command(self):
        self.symbol = self.current_line[1:]

    def parse_c_command(self):
        eq_sign_index, semi_colon_index = None, None

        for i, c in enumerate(self.current_line):
            if c == "=":
                eq_sign_index = i
            if c == ";":
                semi_colon_index = i

        self.dest = self.current_line[:eq_sign_index] if eq_sign_index else None
        self.comp = self.current_line[eq_sign_index +
                                      1:semi_colon_index] if eq_sign_index else self.current_line[:semi_colon_index]
        self.jump = self.current_line[semi_colon_index:] if semi_colon_index else None

    def parse_l_command(self):
        self.symbol = self.current_line[1:-1]

    def end(self):
        self.f.close()

    def _rm_extra(self, line):
        filtered_cmd = ""
        for i, c in enumerate(line):
            # check if is the second slash for comment
            if c == "/" and line[i - 1] == "/":
                filtered_cmd = filtered_cmd[:-1]
                break
            # check if is a space or newline
            if not self._is_space_or_newline(c):
                filtered_cmd += c
        return filtered_cmd

    def _is_space_or_newline(self, c):
        if c == " " or c == "\n" or c == "\r":
            return True
        return False
