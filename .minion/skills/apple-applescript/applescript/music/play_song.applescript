on run argv
    if (count of argv) > 0 then
        set songName to item 1 of argv
        tell application "Music"
            set searchResults to search for songName
            if (count of searchResults) > 0 then
                play (first item of searchResults)
                return "Now playing: " & songName
            else
                return "Song not found: " & songName
            end if
        end tell
    else
        return "Please provide a song name to play"
    end if
end run