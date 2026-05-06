def maxScore(grid, k):
    m, n = len(grid), len(grid[0])

    # STRATEGY:
    # Track every possible (position, cost_spent) combination.
    # dp[i][j][c] = the best score we can have at cell (i,j)
    #               having spent exactly c total cost so far.
    # We fill the table left-to-right, top-to-bottom, so when
    # we compute a cell we've already solved both cells above and to the left.

    # -1 means "no valid path reaches this state"
    dp = [[[-1] * (k + 1) for _ in range(n)] for _ in range(m)]

    # Base case: start at (0,0). grid[0][0] is always 0, so cost=0, score=0.
    dp[0][0][0] = 0

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue  # already initialized above

            cell_cost  = 0 if grid[i][j] == 0 else 1
            cell_score = grid[i][j]

            for c in range(cell_cost, k + 1):
                # What was the cost before we stepped into this cell?
                prev_c = c - cell_cost

                # We could only arrive from above (i-1,j) or from the left (i,j-1).
                # Pick whichever predecessor had the higher score.
                best_prev = -1
                if i > 0:
                    best_prev = max(best_prev, dp[i-1][j][prev_c])
                if j > 0:
                    best_prev = max(best_prev, dp[i][j-1][prev_c])

                # If any valid path reached a predecessor, extend it to here.
                if best_prev >= 0:
                    dp[i][j][c] = best_prev + cell_score

    # At the destination, try every cost <= k and return the best score.
    # max() over the last row of the cost dimension; still -1 if unreachable.
    return max(dp[m-1][n-1])

