#!/usr/bin/python

#############
# Gift Exchange Name Matcher
#
# Rules:
# 1. give to a different person than last year
# 2. partners can't be nuclear family members
# 3. can't choose yourself
# 4. participants give one gift only
# 5. participants receive one gift only
#############

import libgiftex
import pprint
import random
import sys
import time

if __name__ == '__main__':
    from data import participants, families

    chosen = []

    print("Please Wait! The robot is picking numbers out of a hat...")
    print("")
    time.sleep(5)
    while len(chosen) != len(participants):
        givers = libgiftex.possible_givers(participants, chosen)
        # if we omit randomization here, our "abort/retry" (below) may fail,
        # although I'm not really sure why
        giver = random.choice(givers)
        libgiftex.debug_fine("GIVER: %s" % giver)
        recipients = libgiftex.possible_recipients(giver, participants, chosen, families)
        # brute force abort/retry
        if len(recipients) == 0:
            libgiftex.debug("No recipients, trying a different giver...")
            if len(givers) <= 1:
                libgiftex.debug("No other givers to try! Starting over...")
                chosen = []
            if len(givers) == 2:
                libgiftex.debug("Stalemate! Two givers left but they can't give to eachother. Starting over...")
                chosen = []
            continue
        recipient = random.choice(recipients)
        libgiftex.debug_fine("RECIPIENT: %s" % recipient)
        chosen.append( (giver, recipient) )
        libgiftex.debug("PAIRS ARE NOW: %s" % chosen)

    chosen.sort()

    participants.sort()
    families.sort()

    f = open('data.py', 'w')
    f.write("participants = ")
    f.write(pprint.pformat(participants))
    f.write("\n\n")
    # f.write("last_years_pairs = ")
    # f.write(pprint.pformat(chosen))
    # f.write("\n\n")
    f.write("families = ")
    f.write(pprint.pformat(families))
    f.write("\n")
    f.close()

    matches = []
    for giver, recipient in chosen:
        # print "%s gives to %s" % (giver, recipient)
        local_match = [giver, recipient]
        matches.append(local_match)
        
    print(matches)
