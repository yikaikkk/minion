on run argv
    if (count of argv) > 0 then
        set volumeLevel to item 1 of argv as number
        tell application "Music"
            set sound volume to volumeLevel
            return "Volume set to " & volumeLevel & "%"
        end tell
    else
        return "Please provide a volume level between 0 and 100"
    end if
end run