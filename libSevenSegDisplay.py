import RPi.GPIO as GPIO

charToCathodes = {
        0: "ABCDEF", 
        1: "BC", 
        2: "ABGED", 
        3: "ABCDG", 
        4: "BCFG", 
        5: "ACDFG", 
        6: "ACDEFG", 
        7: "ABC", 
        8: "ABCDEFG", 
        9: "ABCDFG", 
}

def displayCharacter(character, cathodeToPin):
    cathodes = list(charToCathodes[character])
    for c in cathodes:
        pin = cathodeToPin[c]
        GPIO.output(pin, GPIO.HIGH)


