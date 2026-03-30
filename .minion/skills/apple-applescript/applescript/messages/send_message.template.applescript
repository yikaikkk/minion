tell application "Messages"
    set targetService to 1st service whose service type = iMessage
    set targetBuddy to buddy "{{RECIPIENT}}" of targetService
    send "{{MESSAGE}}" to targetBuddy
    return "Message sent successfully"
end tell