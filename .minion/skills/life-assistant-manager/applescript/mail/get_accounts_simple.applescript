tell application "Mail"
    set accountList to {}
    
    repeat with anAccount in accounts
        set accountName to name of anAccount
        set accountEmail to email address of anAccount
        set accountInfo to {name:accountName, email:accountEmail}
        set accountList to accountList & {accountInfo}
    end repeat
    
    return accountList
end tell