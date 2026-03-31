try
    tell application "Music"
        set appName to name
        return "Access granted to Music"
    end tell
except
    return "Access denied to Music"
end try