def checkACLID(teamID: str):
    hexValue = hex(int(teamID))[2:]
    if int(teamID) > 16384 and int(teamID) <= 65536:
        if hexValue.startswith("4") or hexValue.startswith(
            "5"
        ):  # from ACL eFootball to ACL PES
            return str(
                int(teamID) + 65536 - 16384  # + PES 21 ACL OFFSET - eF ACL OFFSET
            )
        else:
            return teamID
    elif int(teamID) > 65536:
        if hexValue.startswith("10") or hexValue.startswith(
            "11"
        ):  # from Asian Cup to Real ID (65536 is a coincidence)
            return str(int(teamID) - 65536)
        else:
            return teamID
    else:
        return teamID
