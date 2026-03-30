tell application "Mail"
    set mailboxList to {}
    
    repeat with anAccount in accounts
        if name of anAccount is "{{ACCOUNT_NAME}}" then
            repeat with aMailbox in mailboxes of anAccount
                set mailboxName to name of aMailbox
                set mailboxInfo to {mailbox:mailboxName}
                set mailboxList to mailboxList & {mailboxInfo}
            end repeat
        end if
    end repeat
    
    return mailboxList
end tell