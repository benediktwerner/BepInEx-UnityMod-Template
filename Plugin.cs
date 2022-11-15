using System.Collections;
using System.Collections.Generic;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;

namespace {{MOD_NAME}}
{
    [BepInPlugin("{{USERNAME}}.{{MOD_NAME_LOWER}}", PluginInfo.PLUGIN_NAME, PluginInfo.PLUGIN_VERSION)]
    public class Plugin : BaseUnityPlugin
    {
        static ManualLogSource L;

        private void Awake()
        {
            L = Logger;
            Harmony.CreateAndPatchAll(typeof(Plugin));
        }
    }
}
