vbs_script = [
    'Set WScriptShell = WScript.CreateObject("WScript.Shell")',
    'Set Shortcut = WScriptShell.CreateShortcut(%ShortcutPath%)',
    'Shortcut.TargetPath = %TargetPath%',
    'Shortcut.WorkingDirectory = %WorkingDirectoryPath%',
    'Shortcut.IconLocation = %ShortcutIconPath%',
    'Shortcut.Save'
]

with open('CreateShortcut.vbs', 'w') as file:
    for line in vbs_script:
        file.write(line + '\n')