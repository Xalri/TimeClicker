[Setup]
AppName=Time Clicker
AppVersion=1.0
DefaultDirName={localappdata}\Time Clicker
OutputDir=output
OutputBaseFilename=TimeClickerInstaller

[Files]
; Extract the main PyInstaller .exe to the installation directory (i.e., {app})
Source: "C:\Users\samy9\OneDrive\Documents\TimeClicker\output\Time Clicker\Time Clicker.exe"; DestDir: "{app}"; Flags: ignoreversion

; Extract the _internal folder (which contains dependencies) to AppData as 'dependencies'
Source: "C:\Users\samy9\OneDrive\Documents\TimeClicker\output\Time Clicker\_internal\*"; DestDir: "{localappdata}\Time Clicker\dependencies"; Flags: recursesubdirs createallsubdirs

[Run]
; Run the main executable after installation
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,Time Clicker}"; Flags: postinstall
