tell application "Music"
    if player state is playing then
        pause
        return "Music paused"
    else
        play
        return "Music playing"
    end if
end tell