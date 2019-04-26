# What To Backup
$BackupInfoList= 	'U:\folderName',
					'U:\folderName',
					'U:\folderName',
					'U:\folderName',
					'S:\folderName',
					'S:\folderName',
					'S:\folderName',
					'I:\folderName',
					'C:\folderName',
					'C:\folderName',
					'C:\folderName'					

#Append date to 7z File
$Cdate=Get-Date -format dd-MM-yyyy

#Delete Old Backups
$AgeDays='-7'

# Backup Destination Drive USB3 Portable
$BackupDestination='B:\Data-Backups'

#CreateFolder for current Backup
$Cfolder ="$BackupDestination\Backup-$Cdate"
If(!(test-path $Cfolder))
{
     New-Item -ItemType directory -Path $BackupDestination\Backup-$Cdate
}
# Alias for 7-zip #
if (-not (test-path "$env:ProgramFiles\7-Zip\7z.exe")) {throw "$env:ProgramFiles\7-Zip\7z.exe needed"} 
set-alias sz "$env:ProgramFiles\7-Zip\7z.exe" 

#------------------------------------------------#
#----------NO need to edit below this line-------#
#------------------------------------------------#
#Array Loop
Foreach ($Path in $BackupInfoList)
{
	#Get Folder Name
	$folderNamme = Get-ItemPropertyValue -Path $Path  -Name Name
	#Create 7z File Backup
	sz a $BackupDestination\Backup-$Cdate\$folderNamme-Backup-$Cdate.7z $Path\* -mx=4
}
#-------------Delete Old Backups---------------------#

# Delete files older than the $limit.
get-childitem -Path $BackupDestination -Recurse -Force | Where-Object {!$_.psiscontainer -and $_.CreationTime -lt (Get-Date).AddDays($AgeDays)} | remove-item -force
# Delete any empty directories left behind after deleting the old files.
Get-ChildItem -Path $BackupDestination -Recurse -Force | Where-Object { $_.PSIsContainer -and (Get-ChildItem -Path $_.FullName -Recurse -Force | Where-Object { !$_.PSIsContainer }) -eq $null } | Remove-Item -Force -Recurse