class BinarySearch:
    def search(self, needle, haystack):
        haystack.sort()
        low = 0
        high = len(haystack) - 1

        while low <= high:
            mid = (low + high) // 2
            guess = haystack[mid]
            if guess == needle:
                return mid
            if guess > needle:
                high = mid - 1
            else:
                low = mid + 1
        return None
