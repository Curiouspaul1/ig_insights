def sort_by_param(param, data, desc=True):
        from heapq import heappop, heappush
        # given param, sort items based off the param
        temp_heap = []
        map_ = {}
        res = []

        # create map and heapify
        for n in range(len(data)):
            curr = data[n]
            if not curr:
                continue
            key = curr[param]
            if key in map_:
                map_[key].append(n)
            else:
                map_[key] = [n]
            if desc:
                heappush(temp_heap, -curr[param])
            else:
                heappush(temp_heap, curr[param])
        
        # pop the heap to get top items
        while temp_heap:
            if desc:
                curr = -heappop(temp_heap)
            else:
                curr = heappop(temp_heap)
            for i in map_[curr]:
                res.append(data[i])
        return res


def update_obj(obj):
    if not obj:
        return obj
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

# def check_sort(f):
#     from functools import wraps
#     from flask import request, abort, make_response

#     valid_sort_params = ['like_count', 'comments_count', 'like_comment_ratio']

#     @wraps(f)
#     def wrapped(*args, **kwargs):
#         if 'sort' in request.args:
#             param = request.args.get('sort')
#             if param not in valid_sort_params:
#                 resp = make_response(
#                     {
#                         'status': 'error',
#                         'msg': 'invalid sort param',
#                         'data': []
#                     },
#                     400
#                 )
#                 abort(resp)
#             else:
#                 resp