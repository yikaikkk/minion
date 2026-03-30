tell application "Music"
    if player state is playing then
        set currentTrack to current track
        set trackName to name of currentTrack
        set trackArtist to artist of currentTrack
        set trackAlbum to album of currentTrack
        return "Now playing: " & trackName & " by " & trackArtist & " from " & trackAlbum
    else
        return "No music is currently playing"
    end if
end tell