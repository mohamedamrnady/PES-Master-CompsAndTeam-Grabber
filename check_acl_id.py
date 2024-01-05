def checkACLID(teamID: str):
    if int(teamID) > 16384 and int(teamID) <= 65536:  # from ACL eFootball to ACL PES
        return str(int(teamID) + 65536 - 16384)  # + PES 21 ACL OFFSET - eF ACL OFFSET
    elif int(teamID) > 65536:  # from Asian Cup to Real ID (65536 is a coincidence)
        return str(int(teamID) - 65536)
    else:
        return teamID
