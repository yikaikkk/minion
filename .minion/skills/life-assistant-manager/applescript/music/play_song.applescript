on run argv
    if (count of argv) = 0 then
        return "Please provide a song name to play"
    end if

    set songName to item 1 of argv

    tell application "Music"
        try
            -- ✅ 1. 模糊匹配歌曲（核心修复）
            set trackList to (every track whose name contains songName)

            if (count of trackList) > 0 then
                set targetTrack to item 1 of trackList
                play targetTrack
                return "Now playing: " & name of targetTrack
            else
                -- ❗ 没找到歌
                return "NOT_FOUND"
            end if

        on error errMsg
            return "ERROR: " & errMsg
        end try
    end tell
end run