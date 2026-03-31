tell application "Reminders"
    set listList to {}
    
    repeat with aList in lists
        set listName to name of aList
        set listInfo to {name:listName}
        set listList to listList & {listInfo}
    end repeat
    
    return listList
end tell