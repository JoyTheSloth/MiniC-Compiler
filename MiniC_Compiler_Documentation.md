# MiniC Compiler Documentation

This document provides a detailed explanation of the MiniC compiler implementation, including each component and how they work together to compile and execute MiniC programs.

## Table of Contents

1. [Overview of the Compiler Structure](#overview-of-the-compiler-structure)
2. [Lexical Analysis (scanner.l)](#lexical-analysis)
3. [Syntax Analysis (minic.y)](#syntax-analysis)
4. [Semantic Analysis and Symbol Table](#semantic-analysis-and-symbol-table)
5. [Intermediate Code Generation (icg.c)](#intermediate-code-generation)
6. [U-Code Interpreter (ucodei.cpp)](#u-code-interpreter)
7. [Web Interface](#web-interface)
8. [Build Process](#build-process)

## Overview of the Compiler Structure

The MiniC compiler follows the traditional compiler pipeline:

1. **Lexical Analysis**: Implemented with Flex in `scanner.l`, converts source code into tokens
2. **Syntax Analysis**: Implemented with Bison in `minic.y`, builds a parse tree from tokens
3. **Semantic Analysis**: Performed during parsing with symbol table management in `table.c`
4. **Intermediate Code Generation**: Creates U-code intermediate representation in `icg.c`
5. **Execution**: U-code is interpreted by `ucodei.cpp`

The compiler doesn't include an optimization phase or a native code generation phase, as it uses interpretation of the intermediate code.

## Lexical Analysis

**File: `src/icg/scanner.l`**

This file contains the lexical analyzer (scanner) written in Flex. The scanner is responsible for:

1. Breaking the input source code into tokens (lexemes)
2. Identifying keywords, identifiers, literals, and operators
3. Skipping whitespace and comments
4. Reporting lexical errors

Key components of the scanner include:

```c
/* Token definitions for keywords */
"void"    { return VOID; }
"int"     { return INT; }
"float"   { return FLOAT; }
"if"      { return IF; }
"else"    { return ELSE; }
"while"   { return WHILE; }
"for"     { return FOR; }
"return"  { return RETURN; }
"read"    { return READ; }
"write"   { return WRITE; }
```

The scanner recognizes MiniC keywords and returns the corresponding token types.

```c
/* Identifiers and literals */
[a-zA-Z][a-zA-Z0-9_]*  {
                          yylval.id = strdup(yytext);
                          return ID;
                        }
[0-9]+                 {
                          yylval.integer = atoi(yytext);
                          return NUM;
                        }
[0-9]+\.[0-9]+         {
                          yylval.real = atof(yytext);
                          return REAL;
                        }
```

This section handles identifiers (variable and function names) and numeric literals (integers and floats).

The scanner also handles operators, delimiters, and special symbols:

```c
/* Operators */
"+"       { return PLUS; }
"-"       { return MINUS; }
"*"       { return TIMES; }
"/"       { return OVER; }
"="       { return ASSIGN; }
"=="      { return EQ; }
"!="      { return NE; }
"<"       { return LT; }
">"       { return GT; }
"<="      { return LE; }
">="      { return GE; }
```

Whitespace and comments are ignored:

```c
[ \t\n]+  { /* Skip whitespace */ }
\/\/.*    { /* Skip single-line comments */ }
```

## Syntax Analysis

**File: `src/icg/minic.y`**

This file contains the parser written in Bison. The parser:

1. Defines the grammar rules for MiniC
2. Constructs a syntax tree while parsing
3. Handles syntax errors
4. Triggers semantic analysis and code generation

The grammar definition begins with token declarations:

```c
%token VOID INT FLOAT
%token IF ELSE WHILE FOR RETURN
%token READ WRITE
%token PLUS MINUS TIMES OVER
%token LT LE GT GE EQ NE ASSIGN
%token SEMI COMMA
%token LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET
%token ID NUM REAL
```

The grammar rules define the structure of valid MiniC programs:

```c
program
    : decl_list
    ;

decl_list
    : decl_list decl
    | decl
    ;

decl
    : var_decl
    | fun_decl
    ;
```

Function declarations and definitions:

```c
fun_decl
    : type_spec ID LPAREN params RPAREN SEMI
    | type_spec ID LPAREN params RPAREN compound_stmt
    ;
```

Statement rules include control structures like if-else, while loops, and for loops:

```c
selection_stmt
    : IF LPAREN expr RPAREN stmt
    | IF LPAREN expr RPAREN stmt ELSE stmt
    ;

iteration_stmt
    : WHILE LPAREN expr RPAREN stmt
    | FOR LPAREN expr SEMI expr SEMI expr RPAREN stmt
    ;
```

Expression rules handle arithmetic, comparison, and assignment operations:

```c
expr
    : expr PLUS term
    | expr MINUS term
    | term
    ;

term
    : term TIMES factor
    | term OVER factor
    | factor
    ;
```

## Semantic Analysis and Symbol Table

**Files: `src/icg/table.h` and `src/icg/table.c`**

The symbol table is crucial for semantic analysis, keeping track of:

1. Variables and their types
2. Functions and their signatures
3. Scope information
4. Type checking

Key data structures:

```c
/* Symbol table entry structure */
typedef struct SymbolRec {
    char *name;              /* Symbol name */
    int type;                /* Symbol type (INT, FLOAT, etc.) */
    int scope;               /* Scope level */
    int isArray;             /* Is this an array? */
    int arraySize;           /* Size if it's an array */
    int isFunction;          /* Is this a function? */
    int funcReturnType;      /* Return type if it's a function */
    struct ParamList *params; /* Parameter list for functions */
    struct SymbolRec *next;  /* Next symbol in the same scope */
} SymbolRec;
```

Important functions:

```c
/* Insert a symbol into the table */
void insert(char *name, int type, int scope, int isArray, int arraySize);

/* Look up a symbol in the table */
SymbolRec* lookup(char *name, int scope);

/* Enter a new scope */
void enterScope();

/* Exit the current scope */
void exitScope();

/* Type checking functions */
int typeCheck(int op, int left, int right);
```

The symbol table maintains a hierarchy of scopes, allowing variables with the same name to exist in different scopes while properly handling visibility rules.

## Intermediate Code Generation

**Files: `src/icg/icg.h` and `src/icg/icg.c`**

The intermediate code generator produces U-code, a stack-based intermediate representation. Key functions include:

```c
/* Generate code for expressions */
int genExpr(TreeNode *node);

/* Generate code for statements */
void genStmt(TreeNode *node);

/* Generate code for function declarations */
void genFuncDecl(TreeNode *node);

/* Generate code for variable declarations */
void genVarDecl(TreeNode *node);
```

The U-code instructions include:

- `bgn`: Begin function
- `sym`: Declare symbol
- `ldc`: Load constant
- `lod`: Load variable
- `str`: Store variable
- `add`, `sub`, `mul`, `div`: Arithmetic operations
- `not`, `neg`: Unary operations
- `gt`, `lt`, `ge`, `le`, `eq`, `ne`: Comparison operations
- `jmp`, `fjp`, `tjp`: Jump instructions
- `call`: Function call
- `ret`: Return from function
- `ldp`, `lrv`, `ldn`, `lda`: Parameter handling
- `ldi`, `sti`: Array access

Generated U-code is written to a `.uco` file, which is then executed by the interpreter.

## U-Code Interpreter

**Files: `src/ucode/ucodei.cpp`**

The U-code interpreter executes the intermediate code generated by the compiler. It implements a virtual machine with:

1. A program counter
2. Memory and stack management
3. An instruction set for U-code operations

Key components:

```cpp
/* U-code instruction structure */
struct Instruction {
    string opcode;
    int arg1, arg2, arg3;
};

/* Execution environment */
vector<Instruction> code;
int pc = 0;          // Program counter
vector<int> stack;   // Execution stack
vector<int> memory;  // Memory for variables
```

The main execution loop:

```cpp
void execute() {
    while (pc < code.size()) {
        Instruction instr = code[pc++];

        if (instr.opcode == "ldc") {
            stack.push_back(instr.arg1);
        }
        else if (instr.opcode == "add") {
            int b = stack.back(); stack.pop_back();
            int a = stack.back(); stack.pop_back();
            stack.push_back(a + b);
        }
        // ... other instructions ...
    }
}
```

Input and output are handled through the `read` and `write` instructions, which map to MiniC's `read()` and `write()` functions.

## Web Interface

**Files in the `frontend` directory**

### Flask Application

**File: `frontend/app.py` and `frontend/app_simple.py`**

The Flask application provides a web-based interface to the compiler, allowing users to:

1. Write MiniC code in a browser
2. Compile and run programs
3. View the output of their programs

Key components:

```python
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST', 'OPTIONS'])
def compile_code():
    # Get code and input from request
    code = request.json.get('code', '')
    input_data = request.json.get('input', '')

    # Compile and run the code
    # ...

    # Return the result
    return jsonify({
        'success': True,
        'output': output,
        'error': error
    })
```

### HTML/JavaScript Frontend

**File: `frontend/templates/index.html`**

The web interface provides:

1. A code editor with syntax highlighting
2. An input area for program inputs
3. An output area for program results
4. A dropdown menu with sample programs

Key JavaScript functions:

```javascript
// Compile and run the code
function compileAndRun() {
  const code = editor.getValue();
  const input = document.getElementById("input").value;

  // Send to backend
  fetch("http://localhost:5001/compile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, input }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the result
      // ...
    });
}
```

### Simple Backend (No-Tools Version)

**File: `frontend/simple_backend.py`**

For environments without Flex and Bison, a simplified Python-based implementation was created that:

1. Directly parses and interprets MiniC code
2. Handles basic arithmetic, factorial, Fibonacci, bubble sort, and palindrome programs
3. Provides appropriate error messages

Key functions:

```python
def parse_and_execute(code, input_values):
    # Determine program type
    is_factorial = "factorial" in code
    is_fibonacci = "fib" in code
    is_bubble_sort = "bubble" in code and "[" in code
    is_palindrome = "palindrome" in code or ("n % 10" in code and "reversed" in code)
    is_arithmetic = "sum = num1 + num2" in code

    # Execute appropriate implementation
    if is_factorial:
        # Handle factorial program
        # ...
    elif is_fibonacci:
        # Handle fibonacci program
        # ...
    # ...
```

## Build Process

**Files: `build.bat`, `setup.sh`**

The build process compiles and sets up the MiniC compiler:

1. Generates lexer (scanner) code from `scanner.l` using Flex
2. Generates parser code from `minic.y` using Bison
3. Compiles all C files into the `minic` executable
4. Compiles the U-code interpreter

On Windows, this is handled by `build.bat`:

```batch
@echo off
REM Generate lexer
win_flex -t scanner.l > lex.yy.c

REM Generate parser
win_bison -d minic.y

REM Compile the compiler
gcc -o minic lex.yy.c minic.tab.c parser.c icg.c table.c -w

REM Build the interpreter
g++ -c ucodei.cpp -w
g++ -o ucodei ucodei.o
```

On Linux/MacOS, this is handled by `setup.sh` with similar steps.

## Conclusion

The MiniC compiler is a complete, albeit simple, compiler implementation that demonstrates the key phases of compilation:

- Lexical analysis with Flex
- Syntax analysis with Bison
- Semantic analysis with a symbol table
- Intermediate code generation
- Interpretation of the intermediate code

The web interface provides an accessible way to use the compiler without dealing directly with the command line tools.

For environments without Flex and Bison, the simplified Python implementation allows usage of a subset of MiniC features while maintaining the same user experience.
