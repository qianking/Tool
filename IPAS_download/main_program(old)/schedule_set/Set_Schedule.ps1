Param ($name, $time, $exe_name, $path)
$taskName = $name
$taskPath = "IPLAS下載"
$STSet = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -DontStopOnIdleEnd
$action = New-ScheduledTaskAction -Execute $exe_name -WorkingDirectory $path -Argument '-NoProfile -ExecutionPolicy ByPass -NoInteractive'
$trigger = New-ScheduledTaskTrigger -Daily -At $time
Register-ScheduledTask $taskName -TaskPath $taskPath -Action $action -Trigger $trigger -Settings $Stset
