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

DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-OneCore-ApplicationModel-Sync-Desktop-FOD-Package~31bf3856ad364e35~amd64~~10.0.18865.10001
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-Hello-Face-Package~31bf3856ad364e35~amd64~~10.0.18865.1000
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-QuickAssist-Package~31bf3856ad364e35~amd64~~10.0.18865.1000
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-TabletPCMath-Package~31bf3856ad364e35~amd64~~10.0.18865.1000
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-MediaPlayer-Package~31bf3856ad364e35~amd64~~10.0.18865.1000
DISM /online /NoRestart /Remove-Package /PackageName:Microsoft-Windows-InternetExplorer-Optional-Package~31bf3856ad364e35~amd64~~11.0.18865.1000
DISM /online /NoRestart /Remove-Package /PackageName:OpenSSH-Client-Package~31bf3856ad364e35~amd64~~10.0.18865.1000

DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.MixedReality.Portal_2000.19010.1151.0_neutral_~_8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.VP9VideoExtensions_1.0.13333.0_x64__8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.HEIFImageExtension_1.0.13472.0_x64__8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.WebMediaExtensions_1.0.13321.0_neutral_~_8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.WebpImageExtension_1.0.12821.0_x64__8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.Xbox.TCUI_1.23.28002.0_neutral_~_8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.XboxApp_48.49.31001.0_neutral_~_8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.XboxGameOverlay_1.32.17005.0_neutral_~_8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.XboxGamingOverlay_2.26.14003.0_neutral_~_8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.XboxIdentityProvider_12.50.6001.0_neutral_~_8wekyb3d8bbwe
DISM /online /Remove-ProvisionedAppxPackage /PackageName:Microsoft.XboxSpeechToTextOverlay_1.17.29001.0_neutral_~_8wekyb3d8bbwe



Dism /online /NoRestart /Disable-Feature /FeatureName:Printing-Foundation-InternetPrinting-Client
Dism /online /NoRestart /Disable-Feature /FeatureName:FaxServicesClientPackage
Dism /online /NoRestart /Disable-Feature /FeatureName:Xps-Foundation-Xps-Viewer
Dism /online /NoRestart /Disable-Feature /FeatureName:Printing-XPSServices-Features
Dism /online /NoRestart /Disable-Feature /FeatureName:WorkFolders-Client
Dism /online /NoRestart /Disable-Feature /FeatureName:SearchEngine-Client-Package
Dism /online /NoRestart /Disable-Feature /FeatureName:MediaPlayback
Dism /online /NoRestart /Disable-Feature /FeatureName:TelnetClient

C:\Temp\install_wim_tweak.exe /o /l
C:\Temp\install_wim_tweak.exe /o /c Microsoft-PPIProjection /r
C:\Temp\install_wim_tweak.exe /o /c Microsoft-Windows-Internet-Browser-Package /r
C:\Temp\install_wim_tweak.exe /o /c Microsoft-Windows-Holographic /r
C:\Temp\install_wim_tweak.exe /h /o /l

##---Services
Set-Service XboxGipSvc -StartupType Disabled
Set-Service XblAuthManager -StartupType Disabled
Set-Service XblGameSave -StartupType Disabled
Set-Service XboxNetApiSvc -StartupType Disabled
Set-Service BcastDVRUserService -StartupType Disabled
Set-Service DiagTrack -StartupType Disabled
Set-Service MapsBroker -StartupType Disabled
Set-Service lfsvc -StartupType Disabled
Set-Service diagnosticshub.standardcollector.service -StartupType Disabled
Set-Service wlidsvc -StartupType Disabled
Set-Service swprv -StartupType Disabled
Set-Service SEMgrSvc -StartupType Disabled
Set-Service PhoneSvc -StartupType Disabled
Set-Service PcaSvc -StartupType Disabled
Set-Service RasMan -StartupType Disabled
Set-Service RetailDemo -StartupType Disabled
Set-Service SDRSVC -StartupType Disabled
Set-Service WbioSrvc -StartupType Disabled
Set-Service FrameServer -StartupType Disabled
Set-Service WerSvc -StartupType Disabled
Set-Service Wecsvc -StartupType Disabled
Set-Service icssvc -StartupType Disabled
Set-Service WSearch-StartupType Disabled


Get-ScheduledTask -TaskPath "\Microsoft\XblGameSave\" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\OneDrive Standalone Update Task-S-1-5-21-4201915487-290832631-729734359-1001" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\Application Experience\" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\CloudExperienceHost\" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\Customer Experience Improvement Program\" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\HelloFace\" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\RemoteAssistance\" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\RetailDemo\" | Disable-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\Windows Error Reporting\" | Disable-ScheduledTask
