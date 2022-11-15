# {{GAME_NAME}} {{MOD_NAME}} Mod

{{DESCRIPTION}}

## Manual Installation
This mod requires BepInEx to work. BepInEx is a modding framework which allows multiple mods to be loaded.

{%IF THUNDERSTORE 1. Download and install BepInEx from the [Thunderstore](https://{{GAME_NAME}}.thunderstore.io/package/BepInEx/BepInExPack_{{GAME_NAME}}/)%}
{%IF NOT THUNDERSTORE 1. Download and install [BepInEx](https://docs.bepinex.dev/articles/user_guide/installation/index.html)%}
2. Download this mod and extract it into `BepInEx/plugins/`
3. Launch the game

## Development
1. Install BepInEx
{%IF PUBLICIZED 2. This mod uses publicized game DLLs to get private members without reflection
   - Use https://github.com/CabbageCrow/AssemblyPublicizer for example to publicize `Stacklands/Stacklands_Data/Managed/GameScripts.dll` (just drag the DLL onto the publicizer exe)
   - This outputs to `Stacklands_Data\Managed\publicized_assemblies\GameScripts_publicized.dll` (if you use another publicizer, place the result there)%}
3. Compile the project. This copies the resulting DLL into `<GAME_PATH>/BepInEx/plugins/`.
   - Your `GAME_PATH` should automatically be detected. If it isn't, you can manually set it in the `.csproj` file.
   - If you're using VSCode, the `.vscode/tasks.json` file should make it so that you can just do `Run Build`/`Ctrl+Shift+B` to build.

## Links
- Github: https://github.com/{{GITHUB_USERNAME}}/{{GAME_NAME}}-{{MOD_NAME}}-Mod
{%IF THUNDERSTORE - Thunderstore: https://{{GAME_NAME}}.thunderstore.io/package/{{GITHUB_USERNAME}}/{{MOD_NAME}}%}

## Changelog

- v1.0: Initial release
