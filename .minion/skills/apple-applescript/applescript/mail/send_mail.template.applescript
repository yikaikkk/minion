tell application "Mail"
    set msgBody to read file (POSIX file "{{TMP_POSIX_PATH}}") as «class utf8»
    
    set newMessage to make new outgoing message with properties {
        subject:"{{SUBJECT}}",
        content:msgBody
    }
    
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"{{TO}}"}
        
        if "{{CC}}" ≠ "" then
            make new cc recipient at end of cc recipients with properties {address:"{{CC}}"}
        end if
        
        if "{{BCC}}" ≠ "" then
            make new bcc recipient at end of bcc recipients with properties {address:"{{BCC}}"}
        end if
        
        send
    end tell
    
    return "Email sent successfully"
end tell