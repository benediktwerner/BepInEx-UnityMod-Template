#!/usr/bin/env python3

from __future__ import annotations
import os, ctypes, subprocess, re, sys
from pathlib import Path
from datetime import datetime
from typing import Any, Dict


variables: Dict[str, Any] = {"YEAR": datetime.now().year}
GAMES = {
    "stacklands": {
        "GAME_NAME": "Stacklands",
        "STEAM_ID": 1948280,
        "UNITY_VERSION": "2020.3.6",
        "ASSEMBLY_NAME": "GameScripts",
        "PUBLICIZED": True,
        "THUNDERSTORE": True,
        "THUNDERSTORE_DEPENDENCY": "BepInEx-BepInExPack_Stacklands-5.4.2100",
    }
}


def yes(prompt: str, default: bool = None) -> bool:
    options = "(y/n)" if default is None else "(Y/n)" if default else "(y/N)"
    res = input(prompt + " " + options + " ").strip()
    while True:
        if not res:
            if default is not None:
                return default
        elif res == "y" or res == "yes":
            return True
        elif res == "n" or res == "no":
            return False

        res = input("Chpose either (y)es or (n)o: ")


def valid_identifier(x: str) -> bool:
    return bool(re.fullmatch("^[a-zA-Z0-9_-]+$", x))


def ask(prompt: str, default: str = None, identifier=False) -> str:
    prompt += " "
    if default:
        prompt += f"({default}) "
    result = input(prompt).strip() or default
    while True:
        if not result:
            result = input("Please enter a value: ")
        elif identifier and not valid_identifier(result):
            result = input("The value should not contain spaces or special symbols: ")
        else:
            return result


def get_git_name() -> str | None:
    try:
        res = (
            subprocess.run(["git", "config", "user.name"], stdout=subprocess.PIPE)
            .stdout.strip()
            .decode()
        )
        if res:
            return res
    except:
        pass
    return None


def get_display_name_win32() -> str | None:
    try:
        GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
        NameDisplay = 3

        size = ctypes.pointer(ctypes.c_ulong(0))
        GetUserNameEx(NameDisplay, None, size)

        nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
        GetUserNameEx(NameDisplay, nameBuffer, size)
        return nameBuffer.value
    except:
        return None


TEST = len(sys.argv) > 1

if TEST:
    print("Running in test mode\n")

variables["MOD_NAME"] = ask("Mod name:", identifier=True)
variables["MOD_NAME_LOWER"] = variables["MOD_NAME"].lower()

default_name = get_git_name() or get_display_name_win32()
variables["USERNAME"] = ask(
    "Username (used as plugin id prefix):", default_name.lower().replace(" ", "")
)

variables["GITHUB_USERNAME"] = ask("GitHub username:", variables["USERNAME"])

variables["TARGET_FRAMEWORK"] = (
    "netstandard2.0" if yes("Use .NET Core?", True) else "net4.6.1"
)

variables["DESCRIPTION"] = ask("Mod description:")

maybe_game = Path(__file__).parent.parent.name
variables["GAME_NAME"] = ask(
    "Game name:", maybe_game if maybe_game.lower() != "modding" else None
)

variables.update(GAMES.get(variables["GAME_NAME"].lower(), {}))

if not variables.get("STEAM_ID"):
    variables["STEAM_ID"] = ask("Game Steam ID:")

if not variables.get("UNITY_VERSION"):
    variables["UNITY_VERSION"] = ask("Unity version:")

if not variables.get("ASSEMBLY_NAME"):
    variables["ASSEMBLY_NAME"] = ask("Game main assembly:", "Assembly-CSharp.dll")

if not variables.get("PUBLICIZED"):
    variables["PUBLICIZED"] = yes("Use publicized DLLs?", True)

if yes("Add MIT license?", True):
    variables["NAME"] = ask("Name for license:", default_name)
else:
    os.remove("LICENSE")

if variables.get("THUNDERSTORE", False) or yes("Add Thunderstore files?", True):
    variables["THUNDERSTORE"] = True
    if not yes("Add icon.xcf?", True):
        os.remove("icon.xcf")
else:
    os.remove("icon.xcf")
    os.remove("manifest.json")

if yes("Package for Nexusmods?", True):
    variables["NEXUS"] = True

variables["PACKAGE"] = variables.get("THUNDERSTORE", False) or variables.get(
    "NEXUS", False
)

missing = set()
errors = []
print()

if not TEST:
    os.remove("Readme.md")
    os.remove("test-input.txt")

for path, _, files in os.walk(os.path.dirname(__file__)):
    if any(f"/{f}" in path + "/" for f in (".mypy_cache", "bin", "obj", ".git")):
        continue

    for file in files:
        if file.endswith("init.py"):
            continue

        new_file = file = os.path.join(path, file)
        vs = re.findall("{{(\w+)}}", file)
        for v in vs:
            if v in variables:
                new_file = new_file.replace("{{" + v + "}}", variables[v])
            else:
                missing.add(v)
        new_file = new_file.replace("_Readme.md", "Readme.md")
        if file != new_file and not TEST:
            os.rename(file, new_file)
            file = new_file

        print(file)
        if file.endswith("icon.xcf"):
            continue

        with open(file) as f:
            content = f.read()

        vs = set(re.findall("{%(.+?)%}", content, re.DOTALL))
        for v in vs:
            if v.startswith("IF "):
                repl = "{%DANGER_REMOVE_LINE%}"
                vv = v.split()[1]
                if vv == "NOT":
                    vv = v.split()[2]
                    if not variables.get(vv, False):
                        repl = v[len(vv) + 8 :]
                elif variables.get(vv, False):
                    repl = v[len(vv) + 4 :]
                content = content.replace("{%" + v + "%}", repl)
            else:
                errors.append(f"Invalid conditional: {v}")

        vs = set(re.findall("{{([^{}]+)}}", content))
        for v in vs:
            if v in variables:
                content = content.replace("{{" + v + "}}", str(variables[v]))
            else:
                missing.add(v)
                continue

        content = re.sub(r"\n[ \t]*({%DANGER_REMOVE_LINE%}[ \t]*)+\n", "\n", content)
        content = content.replace("{%DANGER_REMOVE_LINE%}", "")

        if not TEST:
            with open(file, "w") as f:
                f.write(content)

if not TEST:
    print("\nCreating solution")
    os.system(f"cmd.exe /c dotnet new sln --name {variables['MOD_NAME']}")
    print("\nAdding project to solution")
    os.system(f"cmd.exe /c dotnet sln add {variables['MOD_NAME']}.csproj")

if TEST:
    print("\nTest complete")
    if not missing and not errors:
        print("No missing variables and no errors")
else:
    os.remove(__file__)
    print("\nDone")

if missing:
    print()
    print(len(missing), "missing variables:\n")
    for m in missing:
        print(m)

if errors:
    print()
    print(len(errors), "errors:\n")
    for e in errors:
        print(e)
