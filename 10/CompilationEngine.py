"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from JackTokenizer import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        self.my_tokenizer = input_stream
        self.curr_tok = self.my_tokenizer.curr_line_length
        self.num_of_cycles = 0
        self.num_loop = 5
        self.output_stream = output_stream

    ######################################################
    # my helpers
    ######################################################
    def _write_keyword(self, keyword: str) -> None:
        """Writes a keyword to the output stream."""
        self.output_stream.write(f"<keyword> {keyword} </keyword>\n")

    def _write_symbol(self, symbol: str) -> None:
        """Writes an symbol to the output stream."""
        self.output_stream.write(f"<symbol> {symbol} </symbol>\n")

    def _write_identifier(self, identifier: str) -> None:
        """Writes an identifier to the output stream."""
        self.output_stream.write(f"<identifier> {identifier} </identifier>\n")

    def _write_integer_constant(self, value: str) -> None:
        """Writes an integer constant to the output stream."""
        self.output_stream.write(
            f"<integerConstant> {value} </integerConstant>\n")

    def _write_string_constant(self, value: str) -> None:
        """Writes a string constant to the output stream."""
        self.output_stream.write(
            f"<stringConstant> {value} </stringConstant>\n")

    def _write_opening_tag(self, tag: str) -> None:
        """Writes an opening tag to the output stream."""
        self.output_stream.write(f"<{tag}>\n")

    def _write_closing_tag(self, tag: str) -> None:
        """Writes a closing tag to the output stream."""
        self.output_stream.write(f"</{tag}>\n")

    def _write_token(self, token_type: str, token_value: str) -> None:
        """Writes a general token to the output stream."""
        self.output_stream.write(
            f"<{token_type}> {token_value} </{token_type}>\n")

    ######################################################
    # my code
    ######################################################
    def var_type(self) -> None:
        """Writes the type of a variable to the output stream."""
        var_type_map = {
            "char": self._write_keyword,
            "int": self._write_keyword,
            "boolean": self._write_keyword
        }
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        curr_token = self.my_tokenizer.curr_token
        self.num_loop = 6
        write_function = var_type_map.get(curr_token, self._write_identifier)
        write_function(curr_token)
        self.my_tokenizer.advance()
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_class(self) -> None:
        token_to_method = {
            "static": self.compile_class_var_dec,
            "field": self.compile_class_var_dec,
            "constructor": self.compile_subroutine,
            "function": self.compile_subroutine,
            "method": self.compile_subroutine,
        }

        self._write_opening_tag("class")
        self.my_tokenizer.advance()
        self._write_keyword("class")
        self._write_identifier(self.my_tokenizer.curr_token)
        self.my_tokenizer.advance()
        self._write_symbol("{")
        self.my_tokenizer.advance()

        while self.my_tokenizer.curr_token != "}":
            compile_method = token_to_method.get(self.my_tokenizer.curr_token)
            if compile_method:
                compile_method()
        for _ in range(self.num_loop):
            self.num_of_cycles += 1

        self._write_symbol("}")
        self.my_tokenizer.advance()
        self._write_closing_tag("class")
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self._write_opening_tag("classVarDec")
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        self._write_keyword(self.my_tokenizer.curr_token)
        self.my_tokenizer.advance()

        self.var_type()

        self._write_identifier(self.my_tokenizer.curr_token)
        self.my_tokenizer.advance()
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        while self.my_tokenizer.curr_token == ",":
            self._write_symbol(",")
            self.my_tokenizer.advance()
            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()
        self._write_symbol(";")
        self.my_tokenizer.advance()

        self._write_closing_tag("classVarDec")
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    # todo check last again
    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        set1 = {"constructor", "function", "method"}
        if self.my_tokenizer.curr_token == "{":
            self._write_opening_tag("subroutineBody")
            self._write_symbol("{")
            self.my_tokenizer.advance()
            while self.my_tokenizer.curr_token == "var":
                for _ in range(self.num_loop):
                    self.num_of_cycles += 1
                self.compile_var_dec()

            self.compile_statements()

            self._write_symbol("}")
            self._write_closing_tag("subroutineBody")
            self.my_tokenizer.advance()

        elif self.my_tokenizer.curr_token in set1:
            # subroutineDec
            self._write_opening_tag("subroutineDec")
            self._write_keyword(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()

            if self.my_tokenizer.curr_token == "void":
                self._write_keyword("void")
                self.my_tokenizer.advance()
            else:
                for _ in range(self.num_loop):
                    self.num_of_cycles += 1
                self.var_type()

            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()
            self._write_symbol("(")
            self.my_tokenizer.advance()
            for _ in range(self.num_loop):
                self.num_of_cycles += 1
            self.compile_parameter_list()
            self._write_symbol(")")
            self.my_tokenizer.advance()
            self.compile_subroutine()
            self._write_closing_tag("subroutineDec")
        else:
            for _ in range(self.num_loop):
                self.num_of_cycles += 1
            self.compile_term()
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self._write_opening_tag("parameterList")
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        while self.my_tokenizer.curr_token != ")":
            self.num_of_cycles = 0
            self.var_type()
            for _ in range(self.num_loop):
                self.num_of_cycles += 1
            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()
            if self.my_tokenizer.curr_token == ",":
                self._write_symbol(",")
                self.my_tokenizer.advance()
                self.num_of_cycles += 1
        self._write_closing_tag("parameterList")
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self._write_opening_tag("varDec")
        self._write_keyword("var")
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        self.my_tokenizer.advance()
        self.var_type()
        if self.my_tokenizer.curr_token:
            self.num_of_cycles += 1
            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()
        while self.my_tokenizer.curr_token == ",":
            self._write_symbol(",")
            self.my_tokenizer.advance()
            for _ in range(self.num_loop):
                self.num_of_cycles += 1
            if self.my_tokenizer.curr_token:
                self._write_identifier(self.my_tokenizer.curr_token)
                self.my_tokenizer.advance()
                self.num_of_cycles += 1

        if self.my_tokenizer.curr_token == ";":
            self._write_symbol(";")
            self.my_tokenizer.advance()
        self.num_of_cycles += 1
        self._write_closing_tag("varDec")
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        statement_methods = {
            "let": self.compile_let,
            "if": self.compile_if,
            "while": self.compile_while,
            "do": self.compile_do,
            "return": self.compile_return,
        }
        self.output_stream.write("<statements>\n")
        while self.my_tokenizer.curr_token in statement_methods:
            self.num_of_cycles += 1
            statement_type = self.my_tokenizer.curr_token
            statement_methods[statement_type]()
            self.num_of_cycles += 1
        self.output_stream.write("</statements>\n")
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._write_opening_tag("doStatement")
        if self.my_tokenizer.curr_token == "do":
            self.num_of_cycles += 1
            self._write_keyword("do")
        self.my_tokenizer.advance()
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        self.compile_subroutine()
        if self.my_tokenizer.curr_token == ";":
            self._write_symbol(";")
            self.my_tokenizer.advance()
        self._write_closing_tag("doStatement")
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._write_opening_tag("letStatement")
        self._write_keyword("let")
        self.num_of_cycles += 1
        self.my_tokenizer.advance()

        self._write_identifier(self.my_tokenizer.curr_token)
        self.my_tokenizer.advance()
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        if self.my_tokenizer.curr_token == "[":
            self.num_of_cycles += 1
            self._write_symbol("[")
            self.my_tokenizer.advance()

            self.compile_expression()
            self._write_symbol("]")
            self.my_tokenizer.advance()
            self.num_of_cycles += 1

        self._write_symbol("=")
        self.my_tokenizer.advance()
        self.num_of_cycles += 1

        self.compile_expression()
        self._write_symbol(";")
        self.my_tokenizer.advance()
        self.num_of_cycles += 1

        self._write_closing_tag("letStatement")
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.num_of_cycles += 1
        self._write_opening_tag("whileStatement")
        self._write_keyword("while")
        self.my_tokenizer.advance()

        self.num_of_cycles += 1
        self._write_symbol("(")
        self.my_tokenizer.advance()

        self.compile_expression()
        self.num_of_cycles += 1
        self._write_symbol(")")
        self.my_tokenizer.advance()

        self.num_of_cycles += 1
        self._write_symbol("{")
        self.my_tokenizer.advance()

        self.compile_statements()
        self.num_of_cycles += 1
        self._write_symbol("}")
        self.my_tokenizer.advance()

        self._write_closing_tag("whileStatement")
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._write_opening_tag("returnStatement")
        self._write_keyword("return")
        self.num_of_cycles += 1
        self.my_tokenizer.advance()

        if self.my_tokenizer.curr_token != ";":
            self.compile_expression()
            self.num_of_cycles += 1

        self.num_of_cycles += 1
        self._write_symbol(";")
        self._write_closing_tag("returnStatement")
        self.my_tokenizer.advance()
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        self._write_opening_tag("ifStatement")
        self.num_of_cycles = 0
        self.num_of_cycles += 1
        self._write_keyword("if")
        self.my_tokenizer.advance()

        self.num_of_cycles += 1
        self._write_symbol("(")
        self.my_tokenizer.advance()

        self.compile_expression()

        self.num_of_cycles += 1
        self._write_symbol(")")
        self.my_tokenizer.advance()

        self.num_of_cycles += 1
        self._write_symbol("{")
        self.my_tokenizer.advance()

        self.compile_statements()

        self.num_of_cycles += 1
        self._write_symbol("}")
        self.my_tokenizer.advance()

        if self.my_tokenizer.curr_token == "else":
            self._write_keyword("else")
            self.my_tokenizer.advance()

            self.num_of_cycles += 1
            self._write_symbol("{")
            self.my_tokenizer.advance()

            self.compile_statements()

            self.num_of_cycles += 1
            self._write_symbol("}")
            self.my_tokenizer.advance()

        self._write_closing_tag("ifStatement")
        self.num_of_cycles += 1
        # print(self.num_of_cycles)
        self.num_of_cycles = 0

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self._write_opening_tag("expression")
        self.num_of_cycles += 1
        self._write_opening_tag("term")
        self.compile_term()
        self._write_closing_tag("term")

        valid_symbols = {"+", "-", "*", "/", "&", "|", "<", ">", "="}

        while self.my_tokenizer.curr_token in valid_symbols:
            self.num_of_cycles += 1
            symbol = self.my_tokenizer.curr_token
            if symbol == "<":
                symbol = "&lt;"
            elif symbol == ">":
                symbol = "&gt;"
            elif symbol == "&":
                symbol = "&amp;"

            self._write_symbol(symbol)
            self.my_tokenizer.advance()

            self._write_opening_tag("term")
            self.compile_term()
            self._write_closing_tag("term")
            self.num_of_cycles += 1

        self._write_closing_tag("expression")
        self.num_of_cycles += 1
        # print(self.num_of_cycles\n)
        self.num_of_cycles = 0

    # todo come back
    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        keyword_constant_set = {"true", "false", "null", "this"}
        unary_symbols = {"-", "~"}
        this_token = self.my_tokenizer.curr_token
        the_next_token_ind = self.my_tokenizer.curr_word_index
        self.num_of_cycles += 1
        the_next_token = self.my_tokenizer.curr_line[the_next_token_ind]

        if this_token in unary_symbols:
            self.num_of_cycles += 1
            self._write_symbol(this_token)
            self.my_tokenizer.advance()
            self._write_opening_tag("term")
            self.compile_term()
            self._write_closing_tag("term")

        elif this_token == "(":
            self.num_of_cycles += 1
            self._write_symbol("(")
            self.my_tokenizer.advance()
            self.compile_expression()
            self._write_symbol(")")
            self.my_tokenizer.advance()

        elif the_next_token == "(":
            self.num_of_cycles += 1
            self._write_identifier(this_token)
            self.my_tokenizer.advance()
            self.compile_expression_list()
            self.my_tokenizer.advance()

        elif the_next_token == "[":
            self.num_of_cycles += 1
            self._write_identifier(this_token)
            self.my_tokenizer.advance()
            self._write_symbol("[")
            self.my_tokenizer.advance()
            self.compile_expression()
            self._write_symbol("]")
            self.my_tokenizer.advance()

        elif the_next_token == ".":
            self.num_of_cycles += 1
            self._write_identifier(this_token)
            self.my_tokenizer.advance()
            self._write_symbol(".")
            self.my_tokenizer.advance()
            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()
            self.compile_expression_list()
            self.my_tokenizer.advance()

        elif this_token in self.my_tokenizer.integer_constants:
            self.num_of_cycles += 1
            self._write_integer_constant(this_token)
            self.my_tokenizer.advance()

        elif this_token.startswith("\""):
            self.num_of_cycles += 1
            self._write_string_constant(this_token[1:-1])
            self.my_tokenizer.advance()

        elif this_token in keyword_constant_set:
            self.num_of_cycles += 1
            self._write_keyword(this_token)
            self.my_tokenizer.advance()
            self.num_of_cycles += 1

        else:
            self._write_identifier(this_token)
            self.my_tokenizer.advance()
            self.num_of_cycles += 1
        # print(f"{self.num_of_cycles} for testing\n")
        self.num_of_cycles += 0


    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._write_symbol("(")
        self._write_opening_tag("expressionList")
        self.my_tokenizer.advance()
        self.num_of_cycles += 1

        while self.my_tokenizer.curr_token != ")":
            self.num_of_cycles += 1
            self.compile_expression()
            if self.my_tokenizer.curr_token == ",":
                self._write_symbol(",")
                self.my_tokenizer.advance()
            if self.my_tokenizer.curr_token == ")":
                break
        self._write_closing_tag("expressionList")
        self._write_symbol(")")
        self.num_of_cycles += 1
        # print(self.num_of_cycles\n)
        self.num_of_cycles = 0
