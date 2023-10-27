def checkACLID(teamID: str):
    hexValue = hex(int(teamID))[2:]
    if len(hexValue) > 3:
        if hexValue.startswith("4"):
            return str(int(f"0x10{hexValue[1:]}", base=16))
        elif hexValue.startswith("5"):
            return str(int(f"0x11{hexValue[1:]}", base=16))
        else:
            return teamID
    else:
        return teamID
