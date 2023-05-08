; This script will run when pressing CTRL+O
^o::
{
    Send, !d
    Sleep, 100
    Send, pwsh.exe
    Send, {Enter}
}
return