# MiniC Compiler Presentation Script

## Introduction (5 minutes)

Hello everyone! Today I'll walk us through the MiniC compiler we've built. There are 4 main parts to our compiler, and we'll go through each one step by step.

## Part 1: Scanner - The Word Recognizer (7 minutes)

**Team Member 1:**

Imagine you're reading a book. Before you understand sentences, you need to recognize individual words. This is what our scanner does:

- The scanner is in the file `src/icg/scanner.l`
- It reads the MiniC code character by character
- It groups these characters into meaningful "tokens" like:
  - Keywords: `if`, `while`, `return`
  - Identifiers: variable names like `x`, `counter`
  - Numbers: `42`, `3.14`
  - Operators: `+`, `-`, `*`, `/`, `==`
- It ignores things we don't need like spaces and comments
- It passes these tokens to the next stage

**Example:** For code like `int x = 5 + y;`, the scanner produces tokens:
`INT` `IDENTIFIER(x)` `ASSIGN` `NUMBER(5)` `PLUS` `IDENTIFIER(y)` `SEMICOLON`

## Part 2: Parser - The Sentence Understander (7 minutes)

**Team Member 2:**

Now that we have words (tokens), we need to understand how they form sentences. The parser does this:

- The parser is in the file `src/icg/minic.y`
- It takes the stream of tokens from the scanner
- It checks if they follow the grammar rules of MiniC
- It builds a tree structure (syntax tree) showing how tokens relate to each other
- It reports errors if the code doesn't follow MiniC grammar

**Example:** For `int x = 5 + y;`, the parser creates a tree showing:

- This is a variable declaration
- The variable is named "x" of type "int"
- Its value is an expression (5 + y)

## Part 3: Semantic Analyzer & Symbol Table - The Meaning Checker (7 minutes)

**Team Member 3:**

Understanding sentence structure isn't enough - we need to check if statements make logical sense. This part:

- Lives in `src/icg/table.c`
- Keeps track of all variables and functions in a "symbol table"
- Checks if variables are declared before use
- Verifies types match (you can't add a string to a number)
- Manages different scopes (variables inside vs. outside functions)
- Reports errors like "undefined variable" or "type mismatch"

**Example:** If you try to do `x = y + 10;` but `y` was never declared, this stage catches that error.

## Part 4: Code Generator & Interpreter - The Translator & Runner (7 minutes)

**Team Member 4:**

Finally, we need to convert our program into something a computer can execute:

- The code generator is in `src/icg/icg.c`
- It walks through the syntax tree from the parser
- It generates U-code (our intermediate code)
- U-code is like assembly language but simpler
- The interpreter in `src/ucode/ucodei.cpp` then:
  - Takes this U-code
  - Executes it instruction by instruction
  - Handles input/output through the `read()` and `write()` functions

**Example:** For `x = 5 + y;`, it generates U-code like:

```
lod y    // Load the value of y
ldc 5    // Load the constant 5
add      // Add them together
str x    // Store the result in x
```

## Putting It All Together & Demo (7 minutes)

**Everyone:**

Let's see how everything works together:

1. A MiniC program is written in our web interface
2. When you click "Compile & Run":
   - The scanner breaks it into tokens
   - The parser organizes these tokens into a syntax tree
   - The semantic analyzer checks for logical errors
   - The code generator creates U-code
   - The interpreter executes this U-code
3. The result appears in the output box

Let's try a few examples:

- A simple calculation
- A factorial program
- A sorting algorithm

## Q&A (10 minutes)

Any questions about how our compiler works?

## Conclusion (2 minutes)

That's our MiniC compiler! We've seen how it:

1. Recognizes words (scanner)
2. Understands sentences (parser)
3. Checks meaning (semantic analyzer)
4. Translates and runs the code (code generator & interpreter)

This is a simplified version of how real compilers like GCC or Clang work too!
