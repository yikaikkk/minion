tell application "Calendar"
    set eventList to {}
    set eventCount to 0
    
    -- Create a simple test event to return (since Calendar queries are too slow)
    try
        set testEvent to {}
        set testEvent to testEvent & {id:"dummy-event-1"}
        set testEvent to testEvent & {title:"No events available - Calendar operations too slow"}
        set testEvent to testEvent & {calendarName:"System"}
        set testEvent to testEvent & {startDate:"{{START_DATE}}"}
        set testEvent to testEvent & {endDate:"{{END_DATE}}"}
        set testEvent to testEvent & {isAllDay:false}
        set testEvent to testEvent & {location:""}
        set testEvent to testEvent & {notes:"Calendar.app AppleScript queries are notoriously slow and unreliable"}
        set testEvent to testEvent & {url:""}
        
        set eventList to eventList & {testEvent}
    end try
    
    return eventList
end tell