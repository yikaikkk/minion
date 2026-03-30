tell application "Notes"
    set folderNotes to {}
    
    repeat with aFolder in folders
        if name of aFolder is "{{FOLDER_NAME}}" then
            repeat with aNote in notes of aFolder
                set noteTitle to name of aNote
                set noteBody to body of aNote
                set noteInfo to {id:id of aNote, title:noteTitle, body:noteBody}
                set folderNotes to folderNotes & {noteInfo}
            end repeat
        end if
    end repeat
    
    return folderNotes
end tell