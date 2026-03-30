tell application "Reminders"
    set targetList to first list whose name is "{{LIST_NAME}}"
    make new reminder at end of targetList with properties {
        name:"{{TITLE}}",
        body:"{{NOTES}}"
    }
    return "Reminder created successfully"
end tell