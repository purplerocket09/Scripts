$password = "Password" | ConvertTo-SecureString -asPlainText -Force
$username = "Domain\User" 
$credential = New-Object System.Management.Automation.PSCredential($username,$password)
Add-Computer -DomainName "Domain" -Credential $credential -OUPath 'OU=Computer-Here,DC=Domain,DC=Domain'