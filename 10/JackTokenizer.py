"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        input_lines = input_stream.read().splitlines()
        input_lines = self.remove_comments(input_lines)
        self.lines_input = input_lines

        self.curr_line_ind = -1
        self.curr_line_ind = -1
        self.curr_line = []
        self.curr_token = None
        self.curr_token_type = None
        self.curr_line_length = 0
        self.curr_word_index = 0
        self.cycles_for_test = 0
        self.num_cycles_for_test = 0
        self.lines_input = input_lines
        self.num_of_lines = len(input_lines)

        self.advance()

    def has_more_tokens(self) -> bool:
        """Checks if there are more tokens available in the input.

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        if self.curr_word_index < self.curr_line_length - 1:
            return True
        return self.curr_line_ind < len(self.lines_input) - 1


    """
     Removes comments and unnecessary lines from the input.
 
     Args:
         input_lines (List[str]): List of lines from the input stream.
 
     Returns:
         List[str]: List of lines with comments and empty lines removed.
     """
    def remove_comments(self, input_lines: typing.List[str])\
            -> typing.List[str]:
        lines_to_return = []
        in_multiline_comment = False

        for line in input_lines:
            stripped_line = line.strip()
            if in_multiline_comment:
                if "*/" in stripped_line:
                    in_multiline_comment = False
                    stripped_line = stripped_line.split("*/", 1)[1].strip()
                else:
                    continue

            if "/*" in stripped_line:
                if stripped_line.endswith("*/"):
                    stripped_line = stripped_line.split("/*", 1)[1].strip()
                    continue
                in_multiline_comment = True
                stripped_line = stripped_line.split("/*", 1)[0].strip()

            if "//" in stripped_line:
                stripped_line = stripped_line.split("//", 1)[0].strip()

            if stripped_line:
                lines_to_return.append(stripped_line)

        return lines_to_return


    def _split_line_to_tokens(self, line: str) -> typing.List[str]:
        """Splits a line into tokens based on Jack grammar, with advanced splitting."""
        tokens = []
        current_token = ""
        symbols = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-",
                   "*", "/", "&", "|", "<", ">", "=", "~", "^", "#"}
        in_string = False

        for char in line:
            self.cycles_for_test += 1
            if in_string:
                current_token += char
                if char == "\"":
                    self.cycles_for_test = 0
                    in_string = False
                    tokens.append(current_token)
                    current_token = ""
            elif char == "\"":
                if current_token:
                    self.cycles_for_test += 1
                    tokens.append(current_token)
                    current_token = ""
                current_token += char
                in_string = True
                self.cycles_for_test = 0
            elif char in symbols:
                if current_token:
                    tokens.append(current_token)
                    self.cycles_for_test = 0
                    current_token = ""
                tokens.append(char)
            elif char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                self.cycles_for_test += 1
                current_token += char
        # print(self.cycles_for_test)
        self.cycles_for_test = 0
        if current_token:
            tokens.append(current_token)
            self.cycles_for_test += 1
            # print(self.cycles_for_test)
        return tokens

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current
         token."""
        while self.curr_word_index >= self.curr_line_length:
            self.curr_line_ind += 1
            if self.curr_line_ind >= len(self.lines_input):
                self.curr_token = None
                self.curr_token_type = None
                return
            current_line = self.lines_input[self.curr_line_ind]
            self.curr_line = self._split_line_to_tokens(current_line)
            self.curr_line_length = len(self.curr_line)
            self.curr_word_index = 0
        token = self.curr_line[self.curr_word_index]
        self.curr_word_index += 1

        if token.startswith("\""):
            while not token.endswith("\""):
                if self.curr_word_index >= self.curr_line_length:
                    break
                token += " " + self.curr_line[self.curr_word_index]
                self.curr_word_index += 1
        self.curr_token_type = self._determine_token_type(token)
        self.curr_token = token


    def _determine_token_type(self, token: str) -> str:
        """Determines the type of the given token."""
        if token in {"class", "constructor", "function", "method",
                     "field", "static", "var", "int", "char", "boolean",
                     "void", "true", "false", "null", "this", "let", "do",
                     "if", "else", "while", "return"}:
            return "KEYWORD"
        if token in {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-",
                     "*", "/", "&", "|", "<", ">", "=", "~", "^", "#"}:
            return "SYMBOL"
        integer_constants = set()
        for i in range(32768):
            integer_constants.add(str(i))
        if token.isdigit() and token in integer_constants:
            return "INT_CONST"
        if token.startswith('"') and token.endswith('"'):
            return "STRING_CONST"
        return "IDENTIFIER"


    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.curr_token_type is None:
            raise ValueError("No current token available.")
        return self.curr_token_type



    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
        """
        if self.token_type() != "KEYWORD":
            raise ValueError("Current token is not a keyword.")
        return self.curr_token


    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        if self.token_type() != "SYMBOL":
            raise ValueError("Current token is not a symbol.")
        return self.curr_token


    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        if self.token_type() != "IDENTIFIER":
            raise ValueError("Current token is not an identifier.")
        return self.curr_token

    def int_val(self) -> int:
        """
        Returns:
            int: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        if self.token_type() != "INT_CONST":
            raise ValueError("Current token is not an integer constant.")
        return int(self.curr_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value
             of the current token, without the double quotes.
            Should be called only when token_type() is "STRING_CONST".
        """
        if self.token_type() != "STRING_CONST":
            raise ValueError("Current token is not a string constant.")
        return self.curr_token




