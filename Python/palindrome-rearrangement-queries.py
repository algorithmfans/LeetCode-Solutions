# Time:  O(26 * n + 26 * q)
# Space: O(26 * n)

# prefix sum
class Solution(object):
    def canMakePalindromeQueries(self, s, queries):
        """
        :type s: str
        :type queries: List[List[int]]
        :rtype: List[bool]
        """
        def check(left1, right1, left2, right2):
            min_left, max_left = min(left1, left2), max(left1, left2)
            min_right, max_right = min(right1, right2), max(right1, right2)
            if not (prefix[min_left] == 0 and prefix[max_right+1] == prefix[-1]):
                return False
            if min_right < max_left:  # non-overlapped
                return (prefix[min_right+1] == prefix[max_left] and
                        all(prefixs1[right1+1][i] == prefixs2[right1+1][i] for i in xrange(26)) and
                        all(prefixs1[right2+1][i] == prefixs2[right2+1][i] for i in xrange(26)))
            # overlapped
            if (left1 == min_left) == (right1 == max_right):  # inside another
                return all(prefixs1[max_right+1][i] == prefixs2[max_right+1][i] for i in xrange(26))
            # not inside another
            p1, p2 = (prefixs1, prefixs2) if min_left == left1 else (prefixs2, prefixs1)
            diff1 = [(p2[max_right+1][i]-p2[max_left][i])-(p1[max_right+1][i]-p1[min_right+1][i]) for i in xrange(26)]
            if not all(x >= 0 for x in diff1):
                return False
            diff2 = [(p1[min_right+1][i]-p1[min_left][i])-(p2[max_left][i]-p2[min_left][i]) for i in xrange(26)]
            return diff1 == diff2

        prefix = [0]*(len(s)//2+1)
        prefixs1 = [[0]*26 for _ in xrange(len(s)//2+1)]
        prefixs2 = [[0]*26 for _ in xrange(len(s)//2+1)]
        for i in xrange(len(s)//2):
            x, y = ord(s[i])-ord('a'), ord(s[~i])-ord('a')
            prefix[i+1] = prefix[i]+int(x != y)
            for j in xrange(26):
                prefixs1[i+1][j] = prefixs1[i][j]+int(j == x)
                prefixs2[i+1][j] = prefixs2[i][j]+int(j == y)
        return [check(a, b, (len(s)-1)-d, (len(s)-1)-c) for a, b, c, d in queries]
