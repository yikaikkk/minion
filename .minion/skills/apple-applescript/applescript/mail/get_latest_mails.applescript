tell application "Mail"
    set allMails to {}
    
    repeat with anAccount in accounts
        repeat with aMailbox in mailboxes of anAccount
            set mailList to messages of aMailbox
            
            repeat with aMessage in mailList
                set msgSubject to subject of aMessage
                set msgSender to sender of aMessage
                set msgDate to date received of aMessage
                set msgId to id of aMessage
                
                set msgInfo to {id:msgId, subject:msgSubject, sender:msgSender, date:msgDate}
                set allMails to allMails & {msgInfo}
            end repeat
        end repeat
    end repeat
    
    -- Sort by date (newest first)
    set sortedMails to sort allMails by date descending
    
    -- Return first {{LIMIT}} mails
    return items 1 through {{LIMIT}} of sortedMails
end tell

on sort(listToSort, by propertyName, in direction)
    set sortedList to {}
    set tempList to listToSort
    
    repeat while (count of tempList) > 0
        set maxItem to item 1 of tempList
        set maxIndex to 1
        
        repeat with i from 2 to (count of tempList)
            set currentItem to item i of tempList
            if direction is descending then
                if (get propertyName of currentItem) > (get propertyName of maxItem) then
                    set maxItem to currentItem
                    set maxIndex to i
                end if
            else
                if (get propertyName of currentItem) < (get propertyName of maxItem) then
                    set maxItem to currentItem
                    set maxIndex to i
                end if
            end if
        end repeat
        
        set end of sortedList to maxItem
        set tempList to items 1 through (maxIndex - 1) of tempList & items (maxIndex + 1) through end of tempList
    end repeat
    
    return sortedList
end sort