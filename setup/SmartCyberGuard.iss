[Setup]
AppName=SmartCyberGuard
AppVersion=1.0.0
AppPublisher=Varun Kumar
DefaultDirName={commonpf}\SmartCyberGuard
DefaultGroupName=SmartCyberGuard
OutputBaseFilename=SmartCyberGuard_Setup_v1
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
WizardStyle=modern

[Files]
Source: "D:\AI & ML PROJECTS\smart_laptop_analyzer\dist\SmartCyberGuardAgent.exe"; \
DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "{app}\SmartCyberGuardAgent.exe"; Flags: runhidden postinstall skipifsilent

[Registry]
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
ValueName: "SmartCyberGuard"; ValueType: string; \
ValueData: """{app}\SmartCyberGuardAgent.exe"""

[Code]
procedure KillProcess(const ProcessName: string);
var
  ResultCode: Integer;
begin
  Exec(
    'taskkill',
    '/F /IM ' + ProcessName,
    '',
    SW_HIDE,
    ewWaitUntilTerminated,
    ResultCode
  );
end;

function InitializeSetup(): Boolean;
begin
  KillProcess('SmartCyberGuardAgent.exe');
  Result := True;
end;

procedure InitializeWizard();
begin
  KillProcess('SmartCyberGuardAgent.exe');
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    KillProcess('SmartCyberGuardAgent.exe');
  end;
end;
