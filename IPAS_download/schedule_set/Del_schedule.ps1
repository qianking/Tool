Param ($name)
$taskName = $name
$taskPath = "IPLAS下載"
$ErrorActionPreference = "STOP"
$chkExist = Get-ScheduledTask | Where-Object { $_.TaskName -eq $taskName -and $_.TaskPath -eq "\$taskPath\" }
if ($chkExist) {
   Unregister-ScheduledTask $taskName -Confirm:$false
   Write-Host "sucess delete"   
}
else{
   Write-Host "no such schedular setup" 
}