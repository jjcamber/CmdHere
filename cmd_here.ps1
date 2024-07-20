# Get the handle of the currently active File Explorer window
Add-Type -AssemblyName Microsoft.VisualBasic
Add-Type -AssemblyName System.Windows.Forms
$shell = New-Object -ComObject Shell.Application

$explorerWindows = $shell.Windows() | Where-Object { $_.FullName -like '*\explorer.exe' }
foreach ($window in $explorerWindows) {
    $directoryPath = $window.Document.Folder.Self.Path
    # Change to the directory of the first found Explorer window
    Set-Location $directoryPath
    Start-Process cmd.exe -ArgumentList "/k cd `"$directoryPath`"" -Verb RunAs
    break
}
