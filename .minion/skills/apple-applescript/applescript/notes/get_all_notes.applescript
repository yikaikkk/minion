tell application "Notes"
    set allNotes to {}
    
    repeat with aNote in notes
        set noteTitle to name of aNote
        set noteBody to body of aNote
        set noteInfo to {id:id of aNote, title:noteTitle, body:noteBody}
        set allNotes to allNotes & {noteInfo}
    end repeat
    
    return allNotes
end tell