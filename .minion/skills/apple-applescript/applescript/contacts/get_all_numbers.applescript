tell application "Contacts"
    set resultList to {}
    
    repeat with aPerson in people
        set personName to name of aPerson
        set phoneNumbers to phones of aPerson
        
        repeat with aPhone in phoneNumbers
            set phoneNumber to value of aPhone
            set phoneLabel to label of aPhone
            set contactInfo to {name:personName, phone:phoneNumber, label:phoneLabel}
            set resultList to resultList & {contactInfo}
        end repeat
    end repeat
    
    return resultList
end tell