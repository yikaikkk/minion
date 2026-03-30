tell application "Notes"
    set foundNotes to {}
    
    repeat with aNote in notes
        set noteTitle to name of aNote
        set noteBody to body of aNote
        
        if noteTitle contains "{{SEARCH_TEXT}}" or noteBody contains "{{SEARCH_TEXT}}" then
            set noteInfo to {id:id of aNote, title:noteTitle, body:noteBody}
            set foundNotes to foundNotes & {noteInfo}
        end if
    end repeat
    
    return foundNotes
end tell