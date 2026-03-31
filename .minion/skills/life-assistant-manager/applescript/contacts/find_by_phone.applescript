tell application "Contacts"
    set resultList to {}
    
    repeat with aPerson in people
        set phoneNumbers to phones of aPerson
        
        repeat with aPhone in phoneNumbers
            set phoneNumber to value of aPhone
            if phoneNumber contains "{{PHONE}}" then
                set personName to name of aPerson
                set phoneLabel to label of aPhone
                set contactInfo to {name:personName, phone:phoneNumber, label:phoneLabel}
                set resultList to resultList & {contactInfo}
            end if
        end repeat
    end repeat
    
    return resultList
end tell