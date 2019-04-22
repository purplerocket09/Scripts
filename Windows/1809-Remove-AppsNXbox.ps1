$AppsList = "Microsoft.WindowsFeedbackHub", 			# FeedbackHub
			"Microsoft.WindowsAlarms", 					# Alarm & Clock
			"Microsoft.YourPhone", 						# Your Phone
			"Microsoft.ScreenSketch", 					# Screen Sketch
			#"Microsoft.DesktopAppInstaller", 			# DesktopAppInstaller			
			#"Microsoft.WindowsStore", 					# Store 
			#"Microsoft.Wallet", 						# Wallet
			#"Microsoft.StorePurchaseApp", 				# StorePurchaseApp			
			"Microsoft.BingWeather", 					# Weather
			"Microsoft.GetHelp", 						# GetHelp
			"Microsoft.Getstarted", 					# Getstarted 
			"Microsoft.Microsoft3DViewer", 				# 3DViewer  
			"Microsoft.MicrosoftStickyNotes", 			# StickyNotes
			"Microsoft.MSPaint", 						# MSPaint
			"Microsoft.Office.OneNote",					# OneNote 
			"Microsoft.OneConnect", 					# OneConnect  
			"Microsoft.Print3D",						# Print3D  
			"Microsoft.WindowsMaps", 					# Maps
			"Microsoft.WindowsSoundRecorder", 			# SoundRecorder 
			"Microsoft.ZuneMusic", 						# ZuneMusic 
			"Microsoft.ZuneVideo", 						# ZuneVideo 
			"Microsoft.WindowsCamera", 					# Camera   
			#"Microsoft.Windows.Photos", 				# Photos  
			"Microsoft.Messaging", 						# Messaging
			"Microsoft.MicrosoftOfficeHub", 			# OfficeHub
			"Microsoft.People", 						# People 
			"microsoft.windowscommunicationsapps",		# communicationsapps 
			"Microsoft.SkypeApp", 						# SkypeApp 
			"Microsoft.MicrosoftSolitaireCollection", 	# SolitaireCollection
			"Microsoft.WebMediaExtensions", 			# MediaExtensions 
			"Microsoft.XboxSpeechToTextOverlay", 		# XboxSpeechToTextOverlay   
			"Microsoft.XboxGameOverlay", 				# XboxGameOverlay 
			"Microsoft.XboxGamingOverlay", 				# XboxGamingOverlay  			
			"Microsoft.Xbox.TCUI", 						# Xbox.TCUI 
			"Microsoft.XboxIdentityProvider",			# XboxIdentityProvider  
			"Microsoft.XboxApp"							# XboxApp 			
					
ForEach ($App in $AppsList)
{
	$Packages = Get-AppxPackage | Where-Object {$_.Name -eq $App}
	if ($Packages -ne $null)
	{
		"Removing Appx Package: $App"
		foreach ($Package in $Packages) { Remove-AppxPackage -package $Package.PackageFullName }
	}
	else { "Unable to find package: $App" }

	$ProvisionedPackage = Get-AppxProvisionedPackage -online | Where-Object {$_.displayName -eq $App}
	if ($ProvisionedPackage -ne $null)
	{
		"Removing Appx Provisioned Package: $App"
		remove-AppxProvisionedPackage -online -packagename $ProvisionedPackage.PackageName
	}
	else { "Unable to find provisioned package: $App" }
}

DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-Hello-Face-Migration-Package~31bf3856ad364e35~amd64~~10.0.17763.1
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-Hello-Face-Package~31bf3856ad364e35~amd64~~10.0.17763.1
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-QuickAssist-Package~31bf3856ad364e35~amd64~~10.0.17763.1
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-TabletPCMath-Package~31bf3856ad364e35~amd64~~10.0.17763.1
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-MediaPlayer-Package~31bf3856ad364e35~amd64~~10.0.17763.1
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-InternetExplorer-Optional-Package~31bf3856ad364e35~amd64~~11.0.17763.1
DISM /online /NoRestart /Remove-Package /PackageName:OpenSSH-Client-Package~31bf3856ad364e35~amd64~~10.0.17763.1
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-OneCore-ApplicationModel-Sync-Desktop-FOD-Package~31bf3856ad364e35~amd64~~10.0.17763.1

DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.MixedReality.Portal_2000.18081.1242.0_neutral_~_8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.VP9VideoExtensions_1.0.12342.0_x64__8wekyb3d8bbwe


Dism /online /NoRestart /Disable-Feature /FeatureName:Printing-Foundation-InternetPrinting-Client
Dism /online /NoRestart /Disable-Feature /FeatureName:FaxServicesClientPackage
Dism /online /NoRestart /Disable-Feature /FeatureName:Xps-Foundation-Xps-Viewer
Dism /online /NoRestart /Disable-Feature /FeatureName:Printing-XPSServices-Features
Dism /online /NoRestart /Disable-Feature /FeatureName:WorkFolders-Client
Dism /online /NoRestart /Disable-Feature /FeatureName:SearchEngine-Client-Package
Dism /online /NoRestart /Disable-Feature /FeatureName:MediaPlayback

C:\Temp\Scripts\install_wim_tweak.exe /o /l
C:\Temp\Scripts\install_wim_tweak.exe /o /c Microsoft-PPIProjection /r
C:\Temp\Scripts\install_wim_tweak.exe /o /c Microsoft-Windows-Internet-Browser-Package /r
C:\Temp\Scripts\install_wim_tweak.exe /o /c Microsoft-Windows-Holographic /r
C:\Temp\Scripts\install_wim_tweak.exe /h /o /l

##--- Remove Xbox Services
Set-Service XboxGipSvc -StartupType Disabled
Set-Service XblAuthManager -StartupType Disabled
Set-Service XblGameSave -StartupType Disabled
Set-Service XboxNetApiSvc -StartupType Disabled
Set-Service BcastDVRUserService -StartupType Disabled

##--- Disable 'Xbox Live Game Save' Scheduled Tasks
Get-ScheduledTask -TaskPath "\Microsoft\XblGameSave\" | Disable-ScheduledTask



