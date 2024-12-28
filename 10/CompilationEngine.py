"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

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



    # def var_type(self) -> None:
    #     var_type_List = ["char", "int", "boolean"]
    #     if self._tokenizer._current_token not in var_type_List:
    #         self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #
    #     elif self._tokenizer._current_token in var_type_List:
    #         self._output_stream.write(f"<keyword> {self._tokenizer._current_token} </keyword>\n")
    #     else:
    #         self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #     self._tokenizer.advance()

    def var_type(self) -> None:
        """Writes the type of a variable to the output stream."""
        var_type_map = {
            "char": self._write_keyword,
            "int": self._write_keyword,
            "boolean": self._write_keyword
        }
        for _ in range(self.num_loop):
            self.num_of_cycles += 1
        current_token = self.my_tokenizer.curr_token
        write_function = var_type_map.get(current_token, self._write_identifier)
        write_function(current_token)
        self.my_tokenizer.advance()


    # def compile_class(self) -> None:
    #     """Compiles a complete class."""
    #     # todo this is only for web? -> put this instead
    #     # self._output_stream.write("<tokens>\n")
    #     self._output_stream.write("<class>\n")
    #     self._tokenizer.advance()
    #     self._output_stream.write("<keyword> class </keyword>\n")
    #     self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #     self._tokenizer.advance()
    #
    #     assert self._tokenizer._current_token == "{"
    #     self._output_stream.write("<symbol> { </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     static_or_field = ["static", "field"]
    #     cons_or_func_or_meth = ["constructor", "function", "method"]
    #     while self._tokenizer._current_token != "}":
    #         if self._tokenizer._current_token in cons_or_func_or_meth:
    #             self.compile_subroutine()
    #         if self._tokenizer._current_token in static_or_field:
    #             self.compile_class_var_dec()
    #     self._output_stream.write("<symbol> } </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     # todo this is only for web? -> put this instead
    #     # self._output_stream.write("</tokens>\n")
    #     self._output_stream.write("</class>\n")
    def compile_class(self) -> None:
        self._write_opening_tag("class")
        self.my_tokenizer.advance()
        self._write_keyword("class")
        self._write_identifier(self.my_tokenizer.curr_token)
        self.my_tokenizer.advance()
        assert self.my_tokenizer.curr_token == "{"
        self._write_symbol("{")
        self.my_tokenizer.advance()

        token_to_method = {
            "static": self.compile_class_var_dec,
            "field": self.compile_class_var_dec,
            "constructor": self.compile_subroutine,
            "function": self.compile_subroutine,
            "method": self.compile_subroutine,
        }

        while self.my_tokenizer.curr_token != "}":
            compile_method = token_to_method.get(self.my_tokenizer.curr_token)
            if compile_method:
                compile_method()

        self._write_symbol("}")
        self.my_tokenizer.advance()
        self._write_closing_tag("class")



    # def compile_class_var_dec(self) -> None:
    #     """
    #     Compiles a static declaration or a field declaration.
    #     """
    #     assert self._tokenizer._current_token in ["static", "field"]
    #     self._output_stream.write("<classVarDec>\n")
    #     self._output_stream.write(f"<keyword> {self._tokenizer._current_token} </keyword>\n")
    #     self._tokenizer.advance()
    #     self.var_type()
    #     self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #     self._tokenizer.advance()
    #     while self._tokenizer._current_token != ";":
    #         self._output_stream.write("<symbol> , </symbol>\n")
    #         self._tokenizer.advance()
    #         self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #         self._tokenizer.advance()
    #     self._output_stream.write("<symbol> ; </symbol>\n")
    #     self._tokenizer.advance()
    #     self._output_stream.write("</classVarDec>\n")
    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self._write_opening_tag("classVarDec")

        self._write_keyword(self.my_tokenizer.curr_token)
        self.my_tokenizer.advance()

        self.var_type()

        self._write_identifier(self.my_tokenizer.curr_token)
        self.my_tokenizer.advance()

        while self.my_tokenizer.curr_token == ",":
            self._write_symbol(",")
            self.my_tokenizer.advance()
            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()

        assert self.my_tokenizer.curr_token == ";"
        self._write_symbol(";")
        self.my_tokenizer.advance()

        self._write_closing_tag("classVarDec")



    # def compile_subroutine(self) -> None:
    #     """
    #     Compiles a complete method, function, or constructor.
    #     You can assume that classes with constructors have at least one field,
    #     you will understand why this is necessary in project 11.
    #     """
    #     # Your code goes here!
    #     if self._tokenizer.curr_token == "{":
    #         # subroutineBody
    #         self._output_stream.write("<subroutineBody>\n")
    #         self._output_stream.write("<symbol> { </symbol>\n")
    #         self._tokenizer.advance()
    #         while self._tokenizer.curr_token == "var":
    #             self.compile_var_dec()
    #         self.compile_statements()
    #         self._output_stream.write("<symbol> } </symbol>\n")
    #         self._output_stream.write("</subroutineBody>\n")
    #         self._tokenizer.advance()
    #     elif self._tokenizer.curr_token in ["constructor", "function", "method"]:
    #         # subroutineDec
    #         assert self._tokenizer.curr_token in ["constructor", "function", "method"]
    #         self._output_stream.write("<subroutineDec>\n")
    #         self._output_stream.write(f"<keyword> {self._tokenizer.curr_token} </keyword>\n")
    #         self._tokenizer.advance()
    #         if self._tokenizer.curr_token == "void":
    #             self._output_stream.write(f"<keyword> {self._tokenizer.curr_token} </keyword>\n")
    #             self._tokenizer.advance()
    #         else:
    #             self.var_type()
    #         self._output_stream.write(f"<identifier> {self._tokenizer.curr_token} </identifier>\n")
    #         self._tokenizer.advance()
    #         assert self._tokenizer.curr_token == "("
    #         self._output_stream.write("<symbol> ( </symbol>\n")
    #         self._tokenizer.advance()
    #         self.compile_parameter_list()
    #         assert self._tokenizer.curr_token == ")"
    #         self._output_stream.write("<symbol> ) </symbol>\n")
    #         self._tokenizer.advance()
    #         self.compile_subroutine()
    #         self._output_stream.write("</subroutineDec>\n")
    #     else:
    #         self.compile_term()
    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        if self.my_tokenizer.curr_token == "{":
            # subroutineBody
            self._write_opening_tag("subroutineBody")
            self._write_symbol("{")
            self.my_tokenizer.advance()

            while self.my_tokenizer.curr_token == "var":
                self.compile_var_dec()

            self.compile_statements()

            assert self.my_tokenizer.curr_token == "}"
            self._write_symbol("}")
            self._write_closing_tag("subroutineBody")
            self.my_tokenizer.advance()

        elif self.my_tokenizer.curr_token in ["constructor", "function", "method"]:
            # subroutineDec
            assert self.my_tokenizer.curr_token in ["constructor", "function", "method"]
            self._write_opening_tag("subroutineDec")
            self._write_keyword(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()

            if self.my_tokenizer.curr_token == "void":
                self._write_keyword("void")
                self.my_tokenizer.advance()
            else:
                self.var_type()

            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()

            assert self.my_tokenizer.curr_token == "("
            self._write_symbol("(")
            self.my_tokenizer.advance()

            self.compile_parameter_list()

            assert self.my_tokenizer.curr_token == ")"
            self._write_symbol(")")
            self.my_tokenizer.advance()

            self.compile_subroutine()

            self._write_closing_tag("subroutineDec")
        else:
            self.compile_term()





    # def compile_parameter_list(self) -> None:
    #     """Compiles a (possibly empty) parameter list, not including the
    #     enclosing "()".
    #     """
    #     # Your code goes here!
    #     self._output_stream.write("<parameterList>\n")
    #     while self._tokenizer._current_token != ")":
    #         self.var_type()
    #         self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #         self._tokenizer.advance()
    #
    #         if self._tokenizer._current_token == ",":
    #             self._output_stream.write("<symbol> , </symbol>\n")
    #             self._tokenizer.advance()
    #     self._output_stream.write("</parameterList>\n")
    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self._write_opening_tag("parameterList")

        while self.my_tokenizer.curr_token != ")":
            self.var_type()

            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()

            if self.my_tokenizer.curr_token == ",":
                self._write_symbol(",")
                self.my_tokenizer.advance()

        self._write_closing_tag("parameterList")



    # def compile_var_dec(self) -> None:
    #     """Compiles a var declaration."""
    #     self._output_stream.write("<varDec>\n")
    #     self._output_stream.write(f"<keyword> {self._tokenizer._current_token} </keyword>\n")
    #     self._tokenizer.advance()
    #     # type could be int, char, boolean, or className
    #     self.var_type()
    #     self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #     self._tokenizer.advance()
    #     while self._tokenizer._current_token == ",":
    #         self._output_stream.write("<symbol> , </symbol>\n")
    #         self._tokenizer.advance()
    #         self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #         self._tokenizer.advance()
    #     assert self._tokenizer._current_token == ";"
    #     self._output_stream.write("<symbol> ; </symbol>\n")
    #     self._output_stream.write("</varDec>\n")
    #     self._tokenizer.advance()
    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self._write_opening_tag("varDec")
        if self.my_tokenizer.curr_token == "var":
            self._write_keyword("var")
        else:
            return  #todo - delete this when taking down asserts

        self.my_tokenizer.advance()
        self.var_type()

        if self.my_tokenizer.curr_token:
            self._write_identifier(self.my_tokenizer.curr_token)
            self.my_tokenizer.advance()

        while self.my_tokenizer.curr_token == ",":
            self._write_symbol(",")
            self.my_tokenizer.advance()
            if self.my_tokenizer.curr_token:
                self._write_identifier(self.my_tokenizer.curr_token)
                self.my_tokenizer.advance()

        if self.my_tokenizer.curr_token == ";":
            self._write_symbol(";")
            self.my_tokenizer.advance()

        self._write_closing_tag("varDec")






    # def compile_statements(self) -> None:
    #     """Compiles a sequence of statements, not including the enclosing
    #     "{}".
    #     """
    #     self._output_stream.write("<statements>\n")
    #     while self._tokenizer._current_token in ["let", "if", "while", "do", "return"]:
    #         if self._tokenizer._current_token == "let":
    #             self.compile_let()
    #         elif self._tokenizer._current_token == "if":
    #             self.compile_if()
    #         elif self._tokenizer._current_token == "while":
    #             self.compile_while()
    #         elif self._tokenizer._current_token == "do":
    #             self.compile_do()
    #         elif self._tokenizer._current_token == "return":
    #             self.compile_return()
    #     self._output_stream.write("</statements>\n")
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
            statement_type = self.my_tokenizer.curr_token
            statement_methods[statement_type]()
        self.output_stream.write("</statements>\n")


    #
    # def compile_do(self) -> None:
    #     """Compiles a do statement."""
    #     self._output_stream.write("<doStatement>\n")
    #     self._output_stream.write("<keyword> do </keyword>\n")
    #     self._tokenizer.advance()
    #
    #     self.compile_subroutine()
    #     assert self._tokenizer._current_token == ";"
    #     self._output_stream.write("<symbol> ; </symbol>\n")
    #     self._output_stream.write("</doStatement>\n")
    #     self._tokenizer.advance()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._write_opening_tag("doStatement")
        # todo delete when taing down asserts
        if self.my_tokenizer.curr_token == "do":
            self._write_keyword("do")
        self.my_tokenizer.advance()
        self.compile_subroutine()
        if self.my_tokenizer.curr_token == ";":
            self._write_symbol(";")
            self.my_tokenizer.advance()
        self._write_closing_tag("doStatement")



    # def compile_let(self) -> None:
    #     """Compiles a let statement."""
    #     # Your code goes here!
    #     assert self._tokenizer._current_token == "let"
    #     self._output_stream.write("<letStatement>\n")
    #     self._output_stream.write("<keyword> let </keyword>\n")
    #     self._tokenizer.advance()
    #
    #     self._output_stream.write(f"<identifier> {self._tokenizer._current_token} </identifier>\n")
    #     self._tokenizer.advance()
    #
    #     if self._tokenizer._current_token == "[":
    #         self._output_stream.write("<symbol> [ </symbol>\n")
    #         self._tokenizer.advance()
    #
    #         self.compile_expression()
    #         assert self._tokenizer._current_token == "]"
    #         self._output_stream.write("<symbol> ] </symbol>\n")
    #         self._tokenizer.advance()
    #
    #     assert self._tokenizer._current_token == "="
    #     self._output_stream.write("<symbol> = </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     self.compile_expression()
    #     assert self._tokenizer._current_token == ";"
    #     self._output_stream.write("<symbol> ; </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     self._output_stream.write("</letStatement>\n")
    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._write_opening_tag("letStatement")
        self._write_keyword("let")
        self.my_tokenizer.advance()

        self._write_identifier(self.my_tokenizer.curr_token)
        self.my_tokenizer.advance()

        if self.my_tokenizer.curr_token == "[":
            self._write_symbol("[")
            self.my_tokenizer.advance()

            self.compile_expression()
            assert self.my_tokenizer.curr_token == "]"
            self._write_symbol("]")
            self.my_tokenizer.advance()

        assert self.my_tokenizer.curr_token == "="
        self._write_symbol("=")
        self.my_tokenizer.advance()

        self.compile_expression()
        assert self.my_tokenizer.curr_token == ";"
        self._write_symbol(";")
        self.my_tokenizer.advance()

        self._write_closing_tag("letStatement")





    # def compile_while(self) -> None:
    #     """Compiles a while statement."""
    #     # assume that the current token is "while"
    #     assert self._tokenizer._current_token == "while"
    #     self._output_stream.write("<whileStatement>\n")
    #     self._output_stream.write("<keyword> while </keyword>\n")
    #     self._tokenizer.advance()
    #
    #     assert self._tokenizer._current_token == "("
    #     self._output_stream.write("<symbol> ( </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     self.compile_expression()
    #     assert self._tokenizer._current_token == ")"
    #     self._output_stream.write("<symbol> ) </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     assert self._tokenizer._current_token == "{"
    #     self._output_stream.write("<symbol> { </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     self.compile_statements()
    #     assert self._tokenizer._current_token == "}"
    #     self._output_stream.write("<symbol> } </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     self._output_stream.write("</whileStatement>\n")
    def compile_while(self) -> None:
        """Compiles a while statement."""
        assert self.my_tokenizer.curr_token == "while"
        self._write_opening_tag("whileStatement")
        self._write_keyword("while")
        self.my_tokenizer.advance()

        assert self.my_tokenizer.curr_token == "("
        self._write_symbol("(")
        self.my_tokenizer.advance()

        self.compile_expression()
        assert self.my_tokenizer.curr_token == ")"
        self._write_symbol(")")
        self.my_tokenizer.advance()

        assert self.my_tokenizer.curr_token == "{"
        self._write_symbol("{")
        self.my_tokenizer.advance()

        self.compile_statements()
        assert self.my_tokenizer.curr_token == "}"
        self._write_symbol("}")
        self.my_tokenizer.advance()

        self._write_closing_tag("whileStatement")



    # def compile_return(self) -> None:
    #     """Compiles a return statement."""
    #     self._output_stream.write("<returnStatement>\n")
    #     self._output_stream.write("<keyword> return </keyword>\n")
    #     self._tokenizer.advance()
    #
    #     if self._tokenizer._current_token != ";":
    #         self.compile_expression()
    #     assert self._tokenizer._current_token == ";"
    #     self._output_stream.write("<symbol> ; </symbol>\n")
    #     self._output_stream.write("</returnStatement>\n")
    #     self._tokenizer.advance()
    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._write_opening_tag("returnStatement")
        self._write_keyword("return")
        self.my_tokenizer.advance()

        if self.my_tokenizer.curr_token != ";":
            self.compile_expression()

        assert self.my_tokenizer.curr_token == ";"
        self._write_symbol(";")
        self._write_closing_tag("returnStatement")
        self.my_tokenizer.advance()




    # def compile_if(self) -> None:
    #     """Compiles a if statement, possibly with a trailing else clause."""
    #     # Your code goes here!
    #     assert self._tokenizer._current_token == "if"
    #     self._output_stream.write("<ifStatement>\n")
    #     self._output_stream.write("<keyword> if </keyword>\n")
    #     self._tokenizer.advance()
    #
    #     assert self._tokenizer._current_token == "("
    #     self._output_stream.write("<symbol> ( </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     self.compile_expression()
    #     assert self._tokenizer._current_token == ")"
    #     self._output_stream.write("<symbol> ) </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     assert self._tokenizer._current_token == "{"
    #     self._output_stream.write("<symbol> { </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     self.compile_statements()
    #     assert self._tokenizer._current_token == "}"
    #     self._output_stream.write("<symbol> } </symbol>\n")
    #     self._tokenizer.advance()
    #
    #     if self._tokenizer._current_token == "else":
    #         self._output_stream.write("<keyword> else </keyword>\n")
    #         self._tokenizer.advance()
    #
    #         assert self._tokenizer._current_token == "{"
    #         self._output_stream.write("<symbol> { </symbol>\n")
    #         self._tokenizer.advance()
    #
    #         self.compile_statements()
    #         assert self._tokenizer._current_token == "}"
    #         self._output_stream.write("<symbol> } </symbol>\n")
    #         self._tokenizer.advance()
    #
    #     self._output_stream.write("</ifStatement>\n")
    def compile_if(self) -> None:
        """Compiles an if statement, possibly with a trailing else clause."""
        self._write_opening_tag("ifStatement")

        assert self.my_tokenizer.curr_token == "if"
        self._write_keyword("if")
        self.my_tokenizer.advance()

        assert self.my_tokenizer.curr_token == "("
        self._write_symbol("(")
        self.my_tokenizer.advance()

        self.compile_expression()

        assert self.my_tokenizer.curr_token == ")"
        self._write_symbol(")")
        self.my_tokenizer.advance()

        assert self.my_tokenizer.curr_token == "{"
        self._write_symbol("{")
        self.my_tokenizer.advance()

        self.compile_statements()

        assert self.my_tokenizer.curr_token == "}"
        self._write_symbol("}")
        self.my_tokenizer.advance()

        if self.my_tokenizer.curr_token == "else":
            self._write_keyword("else")
            self.my_tokenizer.advance()

            assert self.my_tokenizer.curr_token == "{"
            self._write_symbol("{")
            self.my_tokenizer.advance()

            self.compile_statements()

            assert self.my_tokenizer.curr_token == "}"
            self._write_symbol("}")
            self.my_tokenizer.advance()

        self._write_closing_tag("ifStatement")



    # def compile_expression(self) -> None:
    #     """Compiles an expression."""
    #     self._output_stream.write("<expression>\n")
    #     self._output_stream.write("<term>\n")
    #     self.compile_term()
    #     while self._tokenizer._current_token in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
    #
    #         if self._tokenizer._current_token == "<":
    #             self._tokenizer._current_token = "&lt;"
    #         elif self._tokenizer._current_token == ">":
    #             self._tokenizer._current_token = "&gt;"
    #         elif self._tokenizer._current_token == "&":
    #             self._tokenizer._current_token = "&amp;"
    #
    #         self._output_stream.write("</term>\n")
    #         self._output_stream.write(f"<symbol> {self._tokenizer._current_token} </symbol>\n")
    #         self._tokenizer.advance()
    #         self._output_stream.write("<term>\n")
    #         self.compile_term()
    #
    #     self._output_stream.write("</term>\n")
    #     self._output_stream.write("</expression>\n")
    def compile_expression(self) -> None:
        """Compiles an expression."""
        self._write_opening_tag("expression")

        self._write_opening_tag("term")
        self.compile_term()
        self._write_closing_tag("term")

        valid_symbols = {"+", "-", "*", "/", "&", "|", "<", ">", "="}

        while self.my_tokenizer.curr_token in valid_symbols:
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

        self._write_closing_tag("expression")



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
        current_token = self.my_tokenizer.curr_token
        next_token_ind = self.my_tokenizer.curr_word_index
        next_token = self.my_tokenizer.curr_line[next_token_ind]
        # if current_token in ["-", "~"]:
        #     self._output_stream.write(f"<symbol> {current_token} </symbol>\n")
        #     self._tokenizer.advance()
        #     self._output_stream.write("<term>\n")
        #     self.compile_term()
        #     self._output_stream.write("</term>\n")
        keyword_constant_set = {"true", "false", "null", "this"}
        unary_symbols = {"-", "~"}
        if current_token in unary_symbols:
            self._write_symbol(current_token)
            self.my_tokenizer.advance()
            self._write_opening_tag("term")
            self.compile_term()
            self._write_closing_tag("term")

        elif current_token == "(":
            self._write_symbol("(")
            self.my_tokenizer.advance()
            self.compile_expression()
            assert self.my_tokenizer.curr_token == ")"
            self._write_symbol(")")
            self.my_tokenizer.advance()

        # elif current_token == "(":
        #     self._output_stream.write("<symbol> ( </symbol>\n")
        #     self._tokenizer.advance()
        #     self.compile_expression()
        #     assert self._tokenizer.curr_token == ")"
        #     self._output_stream.write("<symbol> ) </symbol>\n")
        #     self._tokenizer.advance()

        elif next_token == "(":
            self._write_identifier(current_token)
            self.my_tokenizer.advance()
            self.compile_expression_list()
            assert self.my_tokenizer.curr_token == ")"
            self.my_tokenizer.advance()

        # elif next_token == "(":
        #     self._output_stream.write(f"<identifier> {current_token} </identifier>\n")
        #     self._tokenizer.advance()
        #     self.compile_expression_list()
        #     assert self._tokenizer.curr_token == ")"
        #     self._tokenizer.advance()


        elif next_token == "[":
            self._write_identifier(current_token)
            self.my_tokenizer.advance()
            self._write_symbol("[")
            self.my_tokenizer.advance()
            self.compile_expression()
            assert self.my_tokenizer.curr_token == "]"
            self._write_symbol("]")
            self.my_tokenizer.advance()

        # elif next_token == "[":
        #     self._output_stream.write(f"<identifier> {current_token} </identifier>\n")
        #     self._tokenizer.advance()
        #     self._output_stream.write("<symbol> [ </symbol>\n")
        #     self._tokenizer.advance()
        #     self.compile_expression()
        #     assert self._tokenizer.curr_token == "]"
        #     self._output_stream.write("<symbol> ] </symbol>\n")
        #     self._tokenizer.advance()

        elif next_token == ".":
                self._write_identifier(current_token)
                self.my_tokenizer.advance()
                self._write_symbol(".")
                self.my_tokenizer.advance()
                self._write_identifier(self.my_tokenizer.curr_token)
                self.my_tokenizer.advance()
                self.compile_expression_list()
                self.my_tokenizer.advance()

        elif current_token in self.my_tokenizer.integer_constants:
                self._write_integer_constant(current_token)
                self.my_tokenizer.advance()

        elif current_token.startswith("\""):
                self._write_string_constant(current_token[1:-1])
                self.my_tokenizer.advance()

        elif current_token in keyword_constant_set:
                self._write_keyword(current_token)
                self.my_tokenizer.advance()

        else:
                self._write_identifier(current_token)
                self.my_tokenizer.advance()
        #
        # elif next_token == ".": # subroutine call
        #     self._output_stream.write(f"<identifier> {current_token} </identifier>\n")
        #     self._tokenizer.advance()
        #     self._output_stream.write("<symbol> . </symbol>\n")
        #     self._tokenizer.advance()
        #     self._output_stream.write(f"<identifier> {self._tokenizer.curr_token} </identifier>\n")
        #     self._tokenizer.advance()
        #     self.compile_expression_list()
        #     self._tokenizer.advance()
        #
        #
        #
        # elif current_token == "(":
        #     self._output_stream.write("<symbol> ( </symbol>\n")
        #     self._tokenizer.advance()
        #     self.compile_expression()
        #     assert self._tokenizer.curr_token == ")"
        #     self._output_stream.write("<symbol> ) </symbol>\n")
        #     self._tokenizer.advance()
        #
        # elif current_token in self._tokenizer.integer_constants:
        #     self._output_stream.write(f"<integerConstant> {current_token} </integerConstant>\n")
        #     self._tokenizer.advance()
        #
        # elif current_token.startswith("\""):
        #     self._output_stream.write("<stringConstant> ")
        #     self._tokenizer.advance()
        #     self._output_stream.write(f"{current_token[1:-1]}")
        #     self._output_stream.write("</stringConstant>\n")
        #
        # elif current_token in ["true", "false", "null", "this"]:
        #     self._output_stream.write(f"<keyword> {current_token} </keyword>\n")
        #     self._tokenizer.advance()
        #
        # else:
        #     self._output_stream.write(f"<identifier> {current_token} </identifier>\n")
        #     self._tokenizer.advance()


    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        assert self.my_tokenizer.curr_token == "("
        self.output_stream.write("<symbol> ( </symbol>\n")
        self.output_stream.write("<expressionList>\n")
        self.my_tokenizer.advance()

        while self.my_tokenizer.curr_token != ")":
            self.compile_expression()
            if self.my_tokenizer.curr_token == ",":
                self.output_stream.write("<symbol> , </symbol>\n")
                self.my_tokenizer.advance()

        assert self.my_tokenizer.curr_token == ")"
        self.output_stream.write("</expressionList>\n")
        self.output_stream.write("<symbol> ) </symbol>\n")
    # def compile_expression_list(self) -> None:
    #     """Compiles a (possibly empty) comma-separated list of expressions."""
    #     assert self._tokenizer._current_token == "("
    #     self._write_symbol("(")
    #     self._write_opening_tag("expressionList")
    #     self._tokenizer.advance()
    #
    #     while self._tokenizer._current_token != ")":
    #         self.compile_expression()
    #         if self._tokenizer._current_token == ",":
    #             self._write_symbol(",")
    #             self._tokenizer.advance()
    #
    #     assert self._tokenizer._current_token == ")"
    #     self._write_closing_tag("expressionList")
    #     self._write_symbol(")")



    ######################################
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
        self.output_stream.write(f"<integerConstant> {value} </integerConstant>\n")

    def _write_string_constant(self, value: str) -> None:
        """Writes a string constant to the output stream."""
        self.output_stream.write(f"<stringConstant> {value} </stringConstant>\n")
    def _write_opening_tag(self, tag: str) -> None:
        """Writes an opening tag to the output stream."""
        self.output_stream.write(f"<{tag}>\n")

    def _write_closing_tag(self, tag: str) -> None:
        """Writes a closing tag to the output stream."""
        self.output_stream.write(f"</{tag}>\n")

    def _write_token(self, token_type: str, token_value: str) -> None:
        """Writes a general token to the output stream."""
        self.output_stream.write(f"<{token_type}> {token_value} </{token_type}>\n")
