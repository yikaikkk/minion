tell application "Mail"
    set foundMails to {}
    
    repeat with anAccount in accounts
        repeat with aMailbox in mailboxes of anAccount
            set mailList to messages of aMailbox
            
            repeat with aMessage in mailList
                set msgSubject to subject of aMessage
                set msgContent to content of aMessage
                
                if msgSubject contains "{{SEARCH_TEXT}}" or msgContent contains "{{SEARCH_TEXT}}" then
                    set msgSender to sender of aMessage
                    set msgDate to date received of aMessage
                    set msgId to id of aMessage
                    
                    set msgInfo to {id:msgId, subject:msgSubject, sender:msgSender, date:msgDate}
                    set foundMails to foundMails & {msgInfo}
                end if
            end repeat
        end repeat
    end repeat
    
    return foundMails
end tell