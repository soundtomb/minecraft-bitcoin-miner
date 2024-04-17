pageNumber := 1
text := FileRead("page_sequence.txt")
wordPosition := 1

`:: {
    Global pageNumber
    Global wordPosition
    Loop {
        If (wordPosition > StrLen(text)) {
            Return
        }
        WriteNibble(HexToDec(SubStr(text, wordPosition, 1)), &pageNumber)
        PreciseSleep(50)
        wordPosition := wordPosition + 1
    }
}

; Converts a hex string into the correct integer
HexToDec(hex) {
    dec := 0
    VarSetStrCapacity(&dec, 66)
    , val := DllCall("msvcrt.dll\_wcstoui64", "Str", hex, "UInt", 0, "UInt", 16, "CDECL Int64")
    , DllCall("msvcrt.dll\_i64tow", "Int64", val, "Str", dec, "UInt", 10, "CDECL")
    return dec
}

; A more precise sleep function.
; This is needed to keep mostly in sync with minecraft ticks
PreciseSleep(milliseconds) {
    DllCall("Winmm\timeBeginPeriod", "UInt", 3)
    DllCall("Sleep", "UInt", milliseconds)
    DllCall("Winmm\timeEndPeriod", "UInt", 3)
}

; Writes 4 bits to the input buffer in minecraft using a lectern and a book
; Reading a book in a lectern and pressing tab twice selects the "Take Book" button
; 
WriteNibble(value, &pageNumber) {
    offset := value - pageNumber
    If (offset = 0) {
        ; Already on the right page, so we just need to update the write signal
        ; by flipping the page forward and backward (or backward and forward it it's page 15)
        If (value = 15) {
            Send "{PgUp}"
            Send "{PgDn}"
        } Else {
            Send "{PgDn}"
            Send "{PgUp}"
        }
    } Else If (offset > 0) {
        Loop offset
            Send "{PgDn}"
    } Else {
        ; Offset is negative
        Loop -offset
            Send "{PgUp}"
    }
    pageNumber := value
    PreciseSleep(200)
}