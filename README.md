# Vanillifer

Vanillifer goal is to make game more vanilla than in its unmodded state.

Vanillifer does not add any new features to game. It only undoes several new features that are not required for game, and might be considered as an eyesore by many players.

Vanillifer is created with update-resilency in mind. It should survive multiple updates without much attention from user.

Vanillifer contains
  - DogSpam - dog tag removal tool - previously released as [DogSpam](https://wgmods.net/5117)
  - NoPaints - eyesore paint removal tool previously released as [Tonned Down Paints](https://wgmods.net/2809), [NoPaints (Polish)](https://wgmods.net/3272), [NoPaints (Sweedish)](https://wgmods.net/4825)
  - NoStyles - eyesore style removal tool, including 3D styles
  - NoCamouflages - eyesore camouflage removal tool
  - Deskinner - tool to change skinned-clone tank to its unskinned version ([Type 59 Gold non gold](https://wgmods.net/4208) or [WZ-111 QL "Kirin" non gold](https://wgmods.net/5470))

# Update-Resilency
Vanillifer is written to survive multiple game updates, and will be further improved in that manner.

Most of the time you'll be able to just copy it to new mod directory after update without waiting for new release.

As a side effect it has **no** user interface, nor any integration with game UI, as those are the things that break after even minor updates.

# Releases
Releases will be published on GitHub in this repository, and on [official WGMods portal](https://wgmods.net) under [PTwr of NA server](https://worldoftanks.com/en/community/accounts/1000608918-PTwr/) [WGMods account](https://wgmods.net/search/?owner=318781).

Checksums will be attached to release notes

Each release will contain source code (.py files). Compiled python scripts (.pyc files) are required, as that's what game loads. Compiled scripts are **NOT** obfuscated and can be freely inspected for malicious code.

If .wotmod package does not contains source code or .pyc files are obfuscated, package was tampered with and should be immediately deleted.
If checksums are invalid, package was tampered with and should be immediately deleted.

For safety reasons you should avoid closed-source and/or obfuscated mods, as scum exists that will try to ship malware in mods.

# Config file

Vanillifer will automatically create config file  [game root]\mods\config\Vanillifer.ini
![image](https://user-images.githubusercontent.com/20748035/117519883-e0bed700-afa5-11eb-8c29-abf90affba21.png)

If config file in mods\config directory is **not** present (eg. first run after installing Vanillifer) but file in mods\[game version] directory is present, Vanillifer will create new config in mods\config based on it.
This allows mod to be shipped with default settings without risk of user losing exising settings.

## Config Sections

### [dogtags]

Settings for dogtag removal tool.

Fields:
  - ```disable```, disables dogtags when set to ```true```

### [modelOverrides]

Settings for visual model replacing tool.
Currently supports replacing only for skin-clones of same nation. Do **not** use for different tanks.

Keys are tank codes, eg. ```CH01_TYPE59_GOLD``` for Type 59 Gold.
Values are tank codes, eg. ```CH01_TYPE59``` for Type 59.

Key and its Value should have same nation/id prefix (eg. ```CH01```) for feature to work correctly.

For list of tank codes with user-friendly names look into [originalModels] section.

### [originalModels]

Key: "tank code", eg. ```R134_Object_252K```
Value: user-friendly name, eg. ```Object 252U Defender``` (might differ depending on game language)

This section is intended as a lookup-table for user, because otherwise user would have to scavenge game files for those values.
Values will be updated every time game is launched, it will always contain up-to-date data.

### [camouflageOverrides]

Settings for camouflage replacing tool.

Keys are camouflage int ID's, or ```default```.
Values are numerical camouflage ID's, or ```allow``` to not apply ```default``` value to specific camouflage and maintain original values

Camouflage-specific overrides have higher priority over ```default``` value.

For list of camouflage ID's with user-friendly names look into [originalCamouflages] section.

### [originalCamouflages]

Key: camouflage ID, eg. ```1```
Value: user-friendly name, eg. ```Transparent secondary``` (might differ depending on game language)

This section is intended as a lookup-table for user, because otherwise user would have to scavenge game files for those values.
Values will be updated every time game is launched, it will always contain up-to-date data.

Hint: camouflage #1, Transparent secondary, has no camouflage. Therefore to overriding camouflage with it will result in "naked" tank.

### [styleOverrides]

Settings for style replacing tool.

Keys are style int ID's, or ```default```.
Values are numerical **camouflage** ID's (not style), or ```allow``` to not apply ```default``` value to specific style and maintain original values

Style with applied override will lose its special "3D skin" and decals/stickers.

Style-specific overrides have higher priority over ```default``` value.

For list of style ID's with user-friendly names look into [originalStyles] section.
For list of camouflage ID's with user-friendly names look into [originalCamouflages] section.

Styles are overriden with camouflage because style = camouflage+decals+3Dskin

### [originalStyles]

Key: style ID, eg. ```327```
Value: user-friendly name, eg. ```Assault Kit``` (might differ depending on game language)

This section is intended as a lookup-table for user, because otherwise user would have to scavenge game files for those values.
Values will be updated every time game is launched, it will always contain up-to-date data.

### [paintOverrides]

Settings for paint color replacing tool.

Keys are paint ID's, or ```default```.
Values space-delimited base10 RGBA strings, eg. ```79 73 52 255```.

Paint-specific overrides have higher priority over ```default``` value.

For list of paint ID's with values and user-friendly names look into [originalPaints] section.

### [originalPaints]

Key: paint ID, eg. ```2```
Value: RGBA a string with user-friendly name in "inline comment", ```43 50 56 255;Damascus Steel``` (might differ depending on game language)

This section is intended as a lookup-table for user, because otherwise user would have to scavenge game files for those values.
Values will be updated every time game is launched, it will always contain up-to-date data.

## Config example

```ini
[dogtags]
disable = true

[modelOverrides]
A117_T26E5_Patriot = A117_T26E5
Ch01_Type59_Gold = Ch01_Type59
Ch41_WZ_111_QL = Ch41_WZ_111_5A
F74_AMX_M4_1949_Liberte = F74_AMX_M4_1949

[paintOverrides]
default = 79 73 52 255; Applied to all paints without specified override
200 = 118 106 20 255; Purple

[camouflageOverrides]
default = 1
4 = allow; Ad Astra

[styleOverrides]
default = 1
327 = allow; T30 Assault Kit

[originalModels]
R04_T-34 = T-34
R02_SU-85 = SU-85
R01_IS = IS
...

[originalCamouflages]
1 = Transparent secondary
2 = Formosian three-tone
3 = Award Uniform
...

[originalStyles]
1 = China
2 = Czechoslovakia
3 = France
...

[originalPaints]
1 = 14 14 17 255;Ad Astra
2 = 43 50 56 255;Damascus Steel
3 = 17 17 20 255;Vanquisher
...
```
