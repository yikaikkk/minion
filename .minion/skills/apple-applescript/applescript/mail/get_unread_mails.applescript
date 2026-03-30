tell application "Mail"
    set unreadMails to {}
    
    repeat with anAccount in accounts
        repeat with aMailbox in mailboxes of anAccount
            set mailList to messages of aMailbox whose read status is false
            
            repeat with aMessage in mailList
                set msgSubject to subject of aMessage
                set msgSender to sender of aMessage
                set msgDate to date received of aMessage
                set msgId to id of aMessage
                
                set msgInfo to {id:msgId, subject:msgSubject, sender:msgSender, date:msgDate}
                set unreadMails to unreadMails & {msgInfo}
            end repeat
        end repeat
    end repeat
    
    return unreadMails
end tell