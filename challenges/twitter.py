from typing import List, Dict

# Globals / storage
G_timestamp = 0
tweets: List["Tweet"] = []
followers: Dict[int, set[int]] = {}
user_tweets: Dict[int, List[int]] = {}

class Tweet:
    def __init__(self, userid: int, content: str, timestamp: int):
        self.userid = userid
        self.content = content
        self.timestamp = timestamp
    def __repr__(self) -> str:
        return f"Tweet(u={self.userid}, t={self.timestamp}, c={self.content!r})"

def _next_ts() -> int:
    global G_timestamp
    G_timestamp += 1
    return G_timestamp

def follow(myid: int, to_follow_id: int) -> None:
    followers.setdefault(myid, set()).add(to_follow_id)

def unfollow(myid: int, to_unfollow_id: int) -> None:
    if myid in followers:
        followers[myid].discard(to_unfollow_id)

def follow_list(myid: int) -> List[int]:
    return list(followers.get(myid, set()))

def tweet(myid: int, content: str) -> int:
    ts = _next_ts()
    tw = Tweet(myid, content, ts)
    tweets.append(tw)
    user_tweets.setdefault(myid, []).append(len(tweets) - 1)
    return len(tweets) - 1

def users_tweets(userid: int) -> List[Tweet]:
    idxs = user_tweets.get(userid, [])
    return [tweets[i] for i in idxs]

def timeline(myid: int, limit: int = 10) -> List[Tweet]:
    ids = set(followers.get(myid, set()))
    ids.add(myid)  # include own tweets
    pool: List[Tweet] = []
    for u in ids:
        pool.extend(users_tweets(u)[-limit:])
    pool.sort(key=lambda t: t.timestamp, reverse=True)
    return pool[:limit]

def test_timeline_basic():
    # reset globals (assumes the fixed implementation from earlier is in scope)
    global G_timestamp, tweets, followers, user_tweets
    G_timestamp = 0
    tweets = []
    followers = {}
    user_tweets = {}

    # Users: 1, 2, 3
    follow(1, 2)
    follow(1, 3)
    follow(2, 3)

    # Tweets (timestamps increase automatically)
    t20 = tweet(2, "u2: hello")
    t30 = tweet(3, "u3: first")
    t21 = tweet(2, "u2: update")
    t31 = tweet(3, "u3: second")
    t10 = tweet(1, "u1: my own tweet")

    # Timeline for user 1 (follows 2 and 3 + self)
    tl1 = timeline(1, limit=10)
    print("Timeline(1):", [(t.userid, t.timestamp, t.content) for t in tl1])
    # Basic checks
    assert len(tl1) <= 10
    assert tl1 == sorted(tl1, key=lambda x: x.timestamp, reverse=True)
    assert {t.userid for t in tl1} <= {1, 2, 3}

    # Unfollow 3; timeline should exclude user 3 tweets
    unfollow(1, 3)
    tl1_after = timeline(1, limit=10)
    print("Timeline(1) after unfollow(3):", [(t.userid, t.timestamp, t.content) for t in tl1_after])
    assert 3 not in {t.userid for t in tl1_after}

    # User 2 timeline (follows 3)
    tl2 = timeline(2, limit=5)
    print("Timeline(2):", [(t.userid, t.timestamp, t.content) for t in tl2])
    assert {t.userid for t in tl2} <= {2, 3}

    # Edge: user with no follows and no tweets
    tl999 = timeline(999, limit=5)
    print("Timeline(999) (no follows/tweets):", tl999)
    assert tl999 == []

    # Edge: limit smaller than available
    tl1_top3 = timeline(1, limit=3)
    print("Timeline(1) top 3:", [(t.userid, t.timestamp, t.content) for t in tl1_top3])
    assert len(tl1_top3) == min(3, len([t20, t21, t30, t31, t10]))

def main():
    test_timeline_basic()

if __name__ == "__main__":
  main()
