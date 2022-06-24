def sort_by_param(param, data):
        from heapq import heappop, heappush
        # given param, sort items based off the param
        temp_heap = []
        map_ = {}
        res = []

        # create map
        for n in range(len(data)):
            curr = data[n]
            key = curr[param]
            if key in map_:
                map_[key].append(n)
            else:
                map_[key] = [n]
        
        print(map_)
        
        # heapify items
        for n in range(len(data)):
            curr = data[n]
            heappush(temp_heap, -curr[param])
        
        # pop the heap to get top items
        while temp_heap:
            curr = -heappop(temp_heap)
            print(curr)
            for i in map_[curr]:
                print(i)
                res.append(data[i])
        return res


def update_obj(obj):
    if 'like_count' in obj and 'comments_count' in obj:
        if obj['comments_count'] != 0:
            obj.update(
                {
                    'like_comment_ratio':obj['like_count']/obj['comments_count']
                }
            )
        else:
            obj.update({
                'like_comment_ratio': obj['like_count']/1
            })
        return obj