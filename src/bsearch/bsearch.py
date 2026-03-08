class BinarySearch:

    def search(needle, haystack):
        haystack.sort()
        mid = haystack.len / 2
        current_item = haystack[mid]
        if (current_item == needle):
            return mid
        elif (current_item < needle):
            search(needle, haystack[mid..haystack.len])
        else:
            search(needle, haystack[0..mid])

