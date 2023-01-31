
# Programming Language
def C_COMMENT(lang):
    return lambda s: f"/* {lang} \n" + s + "\n*/"


def SHELL_COMMENT(lang):
    return lambda s: f"# {lang} " + s.replace("\n", "#")


ProgrammingToComment = {
    "python:": lambda s: '"""\n' + s + '\n"""',
    "java:": lambda s: "/** Java\n" + s + "\n*/",
    "html:": lambda s: "<!--\n" + s + "\n-->",
    "javascript:": C_COMMENT("Javascript"),
    "js:": C_COMMENT("Javascript"),
    "c:": C_COMMENT("C program"),
    "c++:": C_COMMENT("C++"),
    "c#:": C_COMMENT("C#"),
    "css:": C_COMMENT("CSS"),
    "go:": C_COMMENT("golang"),
    "golang:": C_COMMENT("golang"),
    "dockerfile:": SHELL_COMMENT("Dockerfile"),
    "bash:": SHELL_COMMENT("bash"),
    "sh:": SHELL_COMMENT("sh"),
    "shell:": SHELL_COMMENT("sh"),
}
