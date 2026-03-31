tell application "Mail"
    set mailboxList to {}
    
    repeat with anAccount in accounts
        set accountName to name of anAccount
        
        repeat with aMailbox in mailboxes of anAccount
            set mailboxName to name of aMailbox
            set mailboxInfo to {account:accountName, mailbox:mailboxName}
            set mailboxList to mailboxList & {mailboxInfo}
        end repeat
    end repeat
    
    return mailboxList
end tell