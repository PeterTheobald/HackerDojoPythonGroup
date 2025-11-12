from typing import List

## Peter:
def find_ips(s: str) -> List[str]:
    if not 4 <= len(s) <= 12:
        return []
    N = len(s)

    def ok(seg: str) -> bool:
        return seg == "0" or (seg[0] != "0" and int(seg) <= 255)

    def _find_ips(s: str, i: int, k: int) -> List[str]:
        if k == 1:
            last = s[i:]
            return [last] if ok(last) else []
        # prune: remaining chars must fit into k segments (1..3 each)
        if (N - i) < k or (N - i) > 3 * k:
            return []
        return [
            s[i:i+L] + "." + tail
            for L in (1, 2, 3) if i + L <= N and ok(s[i:i+L])
            for tail in _find_ips(s, i + L, k - 1)
        ]

    return _find_ips(s, 0, 4)

## Sam:
class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        result = []
        length = len(s)
        
        # Early exit
        if length < 4 or length > 12:
            return result
        
        # Comment 1: Use three nested loops to try all valid positions for placing the 3 dots
        for i in range(1, min(4, length - 2)):
            for j in range(i + 1, min(i + 4, length - 1)):
                for k in range(j + 1, min(j + 4, length)):
                    seg1, seg2, seg3, seg4 = s[0:i], s[i:j], s[j:k], s[k:]
                    
                    # Comment 2: Validate all segments inline and add valid IP to result
                    if (len(seg4) <= 3 and
                        (seg1[0] != '0' or len(seg1) == 1) and int(seg1) <= 255 and
                        (seg2[0] != '0' or len(seg2) == 1) and int(seg2) <= 255 and
                        (seg3[0] != '0' or len(seg3) == 1) and int(seg3) <= 255 and
                        (seg4[0] != '0' or len(seg4) == 1) and int(seg4) <= 255):
                        result.append(seg1 + '.' + seg2 + '.' + seg3 + '.' + seg4)
        
        return result
