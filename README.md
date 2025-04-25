
# 🧠 Mini C Compiler

A lightweight compiler built in Python that parses a subset of C and generates pseudo-assembly code. Great for learning how compilers work! 💻🛠️

---

## ✨ Features

- 🔍 Lexical Analysis (via `lexer.py`)
- 🌲 Parsing to build an AST (via `parser.py`)
- ⚙️ Pseudo-code Generation (via `codegen.py`)
- ✅ Basic `int` declarations, arithmetic, and return statements supported

---

## 📂 Project Structure

```
MiniC-Compiler/
├── lexer.py        # Tokenizer
├── parser.py       # AST builder
├── codegen.py      # Assembly-like output generator
├── main.py         # Driver script
├── test.c          # Sample C file
└── README.md       # This file
```

---

## 🚀 Getting Started

### ✅ Requirements
- Python 3.7+

### ▶️ Run the Compiler
```bash
git clone https://github.com/yourusername/MiniC-Compiler.git
cd MiniC-Compiler
python main.py
```

---

## 🧪 Sample Input (`test.c`)

```c
int main() {
    int a = 5;
    int b = 10;
    int c = a + b;
    return c;
}
```

---

## 🖨️ Sample Output

```
=== Generated Assembly ===
a = 5
b = 10
c = a + b
RETURN c
```

---

## 📌 Roadmap

- [ ] 🌀 Support for control flow (`if`, `while`, etc.)
- [ ] 🧠 Type checking and error handling
- [ ] ⚡ Generate real x86 or WebAssembly output
- [ ] 🌐 Web UI to visualize AST and output

---

## 🤝 Contributing

Pull requests are welcome! Feel free to fork this repo and suggest improvements 🙌

---

## 👨‍💻 Author

Built with ❤️ by [Joydeep Das](https://github.com/JoyTheSloth)

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).
```

---

Let me know if you'd like your name and GitHub link added to the author section or want a version with screenshots, badges, or GitHub Actions CI integration.
