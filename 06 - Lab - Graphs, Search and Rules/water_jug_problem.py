''' Water Jug Problem

This code created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

Also known as water pouring puzzles, the water jug problem, measuring puzzles
and other similar titles.

It is a basic class of interger problem.

For a fun refrence which we use here, see the Die Hard 3 version
~ https://www.youtube.com/watch?v=6cAbgAaEOVE (or similar ...)


Problem description:
- Need 4 gallons
- Have 5 gallon and 3 gallon bottles or "jugs".

The actions we can perform are essentially:
- Fill a jug,
- Pour a jug into another jug
- Empty a jug

We represent state as (jug 1, jug 2). So for example,
(0,0) == both jugs empty
(5,3) == both jugs full

Sequence 1 from (0,0) to goal state of (4,x) where x can be anything
(0,0) fill 1
(5,0) poor 1 into 2
(2,3) empty 2
(2,0) transfer from 1 to 2
(0,2) fill jug 1
(5,2) fill jug 2 from 1,
(4,3) # stop here, or (discard jug 2)
(4,0) # alternative end state


Sequence 2 from (0,0) to (4,x)
(0,0) fill jug 2
(0,3) transfer to jug 1
(3,0) fill jug 2
(3,3) fill jug 1 from jug 2
(5,1) empty jug 1
(0,1) transfer from jug 2 to jug 1
(1,0) fill jug 2
(1,3) transfer from jug 2 to jug 1
(4,0)

There are many other possible sequences, especially if cycles are allowed!

'''

JUG_CFG = []  # global - number and size of jugs

def jug_copy(jugs):
    return list(jugs)

def pour(jugs, src, dest):
    '''This method contains the pouring rules.
    Does not modify the jugs - creats a copy.
    If the pour request is not valid, returns None.
    Returns a new state of jugs as a tuple if pour request works.
    '''
    if (src >= 0 and src < len(jugs)) and (dest >= 0 and dest < len(jugs)):
        result = jug_copy(jugs)
        # pour - overfill
        result[dest] += result[src]
        result[src] = 0
        # put excess back in src
        if result[dest] > JUG_CFG[dest]:
            excess = result[dest] - JUG_CFG[dest]
            result[dest] = JUG_CFG[dest]  # limit
            result[src] = excess  # remainder
        # done
        return tuple(result)
    else:
        print("Eik! src (%d) or dest (%d) index not valid." % (src, dest))
        die()


def fill(jugs, dest):
    '''Fill up the indicated jug to the max. Uses the
    global jug capacity values.

    If dest is not a valid jug index, returns None
    Returns an immutable tuple copy of the jugs with fill change.
    (Does not modify jugs parameter.)
    '''
    if dest >= 0 and dest < len(jugs):
        result = jug_copy(jugs)
        result[dest] = JUG_CFG[dest]
        return tuple(result)
    else:
        return None


def empty(jugs, src):
    '''Emtpy the indicated jug.
    Uses the global jug capacity values.

    If src is not a valid jug index, returns None
    Returns an immutable tuple copy of the jugs with empty change.
    (Does not modify jugs parameter.)
    '''
    if src >= 0 and src < len(jugs):
        result = jug_copy(jugs)
        result[src] = 0
        return tuple(result)
    else:
        return None


def setup_jugs():
    '''Uses the JUG_CFG and returns an empty tuple of same length.
    '''
    return tuple([0 for _ in JUG_CFG])


if __name__ == "__main__":
    ### 1 Basic testing of methods and operations
    if False:
        JUG_CFG = [5,3]  # (Die Hard movie version)
        s = setup_jugs()
        print(s)
        # test fillling
        s = fill(s, 0)
        print(s)
        assert s == (5, 0)
        s = fill(s, 1)
        print(s)
        assert s == (5, 0)
        print(s)
        # test emtpy
        s = empty(s, 0)
        print(s)
        assert s == (0, 3)
        s = empty(s, 1)
        print(s)
        assert s == (0, 3)
        # test pour / leftover actions
        s = fill(s, 0)
        assert s == (5, 0)
        s = pour(s, 0, 1)
        print(s)
        assert s == (2, 5)
        s = empty(s, 0)
        print(s)
        assert s == (0, 3)
        s = pour(s, 1, 0)
        print(s)
        assert s == (5, 0)
        s = fill(s, 1)
        print(s)
        assert s == (3, 3)
        s = pour(s, 1, 0)
        print(s)
        assert s == (5, 1)

    ### 2 Solve using a pre-defined sequence of actions
    if False:
        action_calls = {
            'fill': fill,
            'empty': empty,
            'pour': pour
        }

        print('Doing sequence 1 ...')
        ### 3 Sequence 1 of moves
        actions = [
            # tuples, string of method to call then arguments to call
            ('fill',  (0,)),
            ('pour',  (0, 1)),  # (5,0) poor 1 into 2
            ('empty', (1,)),  # (2,3) empty 2
            ('pour',  (0, 1)),  # (2,0) tranfer from 1 to 2
            ('fill',  (0,)),  # (0,2) fill jug 1
            # TODO: missing move - see header for sequence.
            # result should be (4,0)
        ]

        # execute the sequence of actions
        JUG_CFG = [5,3]  # (Die Hard movie version)
        s = setup_jugs()
        for fn, args in actions:
            #print('Calling...', fn, 'with', args, 'on', s)
            s = action_calls[fn](s, *args)
            print(s)
        print('Done')

    ### 4 Solve using sequence 2
    if False:
        action_calls = {
            'fill': fill,
            'empty': empty,
            'pour': pour
        }

        print('Doing sequence 2 ...')
        actions = [
            # tuples, string of method to call then arguments to call
            ('fill',  [1]),     # fill jug 2 => (0,3)
            ('pour',  [1, 0]),  # transfer 2 to jug 1 => (3,0)
            ###TODO: complete the sequence
            # result should be (4,0)
        ]
        # run sequence of actions
        JUG_CFG = [5,3]  # (Die Hard movie version)
        s = setup_jugs()
        for fn, args in actions:
            #print('Calling...', fn, 'with', args, 'on', s)
            s = action_calls[fn](s, *args)
            print(s)
        print('Done')

    # Random choice from all possible actions for a fixed problem
    if False:
        # There is a set of six unique actions to choose from
        actions = [
            # all possible fill's
            (fill, [0]),
            (fill, [1]),
            # all possible pour's
            (pour, [0, 1]),
            (pour, [1, 0]),
            # all possble empty's
            (empty, [0]),
            (empty, [1]),
        ]
        # Notes:
        # - We exclude pour 0->0 and 1->1 as they pointless
        # - Some actions might have no effect (empty if already empty)
        #   but we are not making conditional actions (only naive ones)

        from random import choice, seed
        #seed(1234)

        # For the Die Hard 3 movie two-jug problem ...
        JUG_CFG = [5, 3]
        s = setup_jugs()
        s_end = (4, 0)

        ###TODO: use a list of valid end_states, not just one
        #end_states = [(4,0)]

        status = 'searching'
        count = 0
        limit = 4000
        history = []  # history of moves taken

        # Search loop
        print('Trying a random action search:')
        while status == 'searching':

            # select a random action to try
            fn, args = choice(actions)
            new_s = fn(s, *args)

            # print(str(fn.__name__), args, 'on', s, '=>', new_s)  # details
            # print('.', end='')  # progress dots ...
            print(new_s, end=' ')  # verbose

            # if move outcome state is valid (not None) keep it
            if new_s:
                history.append((fn, args))
                if new_s == s_end:
                    status = 'Success'

            # count and stop test
            count += 1
            if count >= limit:
                status = 'Hit limit'

        print()
        print('Result: %s (limit=%d, count=%d, history=%d)' % (status, limit, count, len(history)))
