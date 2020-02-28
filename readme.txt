C:\Users\6104655\AppData\Roaming\Sublime Text 3\Packages\SublimeREPL\config\Python\Main.sublime-memu

{
  "command": "repl_open",
  "caption": "Python - RUN current file",
  "id": "repl_python_run",
  "mnemonic": "R",
  "args": {
    "type": "subprocess",
    "encoding": "utf8",
    "cmd": [
      "C:\\Users\\6104655\\AppData\\Local\\conda\\conda\\envs\\SplitTheBill\\python.exe",
      "-i",
      "-u",
      "$file_basename"
    ],
    "cwd": "$file_path",
    "syntax": "Packages/Python/Python.tmLanguage",
    "view_id": "*REPL* [python]",
    "external_id": "python",
    "extend_env": {
      "PYTHONIOENCODING": "utf-8"
    }
  }
}

https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/
pdfminer.six
https://github.com/pdfminer/pdfminer.six