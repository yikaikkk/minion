tell application "Calendar"
    set startDate to date "{{START_DATE}}"
    set endDate to date "{{END_DATE}}"
    
    -- Find target calendar
    set targetCal to null
    try
        set targetCal to calendar "{{CALENDAR_NAME}}"
    on error
        -- Use first available calendar
        set targetCal to first calendar
    end try
    
    -- Create the event
    tell targetCal
        set newEvent to make new event with properties {summary:"{{TITLE}}", start date:startDate, end date:endDate, allday event:{{IS_ALL_DAY}}}
        
        if "{{LOCATION}}" ≠ "" then
            set location of newEvent to "{{LOCATION}}"
        end if
        
        if "{{NOTES}}" ≠ "" then
            set description of newEvent to "{{NOTES}}"
        end if
        
        return uid of newEvent
    end tell
end tell