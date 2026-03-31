tell application "Notes"
    set noteBody to read file (POSIX file "{{TMP_POSIX_PATH}}") as «class utf8»
    make new note with properties {name:"{{TITLE}}", body:noteBody}
    return "Note created successfully"
end tell