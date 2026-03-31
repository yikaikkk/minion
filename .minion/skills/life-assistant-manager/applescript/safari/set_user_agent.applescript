tell application "Safari"
    tell front document
        do JavaScript "navigator.userAgent = '{{USER_AGENT}}';"
    end tell
    return "User agent set to {{USER_AGENT}}"
end tell