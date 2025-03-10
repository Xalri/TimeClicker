[Setup]
; Define general setup properties
AppName=Time Clicker
AppVersion=1.0
DefaultDirName={localappdata}\TimeClicker
DefaultGroupName=Time Clicker
OutputDir=C:\Users\samyt\Documents\TimeClicker\Installer\
OutputBaseFilename=TimeClickerInstaller
Compression=lzma
SolidCompression=yes
LicenseFile=C:\Users\samyt\Documents\TimeClicker\LICENCE.md
PrivilegesRequired=lowest
AllowNoIcons=yes

[Files]
; Copy all necessary files to AppData\TimeClicker
Source: "C:\Users\samyt\Documents\TimeClicker\main.dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
Source: "C:\Users\samyt\Documents\TimeClicker\LICENCE.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Create shortcut in Start Menu and Desktop
Name: "{group}\Time Clicker"; Filename: "{app}\Time Clicker.exe"
Name: "{userdesktop}\Time Clicker"; Filename: "{app}\Time Clicker.exe"

[Run]
; Optionally run the executable after installation is complete
Filename: "{app}\Time Clicker.exe"; Flags: nowait postinstall skipifsilent; Description: "Launch Time Clicker";

[Code]
procedure DeleteFilesExceptData(Dir: string);
var
  FindRec: TFindRec;
begin
  if DirExists(Dir) and FindFirst(Dir + '\*', FindRec) then
  begin
    repeat
      if (FindRec.Name <> '.') and (FindRec.Name <> '..') and (FindRec.Name <> 'data') then
      begin
        if (FindRec.Attributes and FILE_ATTRIBUTE_DIRECTORY) <> 0 then
        begin
          DelTree(Dir + '\' + FindRec.Name, True, True, True);
        end
        else
        begin
          DeleteFile(Dir + '\' + FindRec.Name);
        end;
      end;
    until not FindNext(FindRec);
    FindClose(FindRec);
  end;
end;

function InitializeSetup: Boolean;
var
  TargetDir: string;
begin
  TargetDir := ExpandConstant('{localappdata}\TimeClicker');
  if DirExists(TargetDir) then
    DeleteFilesExceptData(TargetDir);
  Result := True;
end;
