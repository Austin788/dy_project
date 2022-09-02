import sys


def combinations(iterable, r, repeat_times=sys.maxsize, max_num=2000):
    key_count = {}
    num = 0
    pool = tuple(iterable)
    n = len(iterable)
    if r > n:
        return
    indices = list(range(r))

    legal_flag = True
    for i in indices:
        if pool[i] in key_count and key_count[pool[i]] >= repeat_times:
            legal_flag = False
            break
    if legal_flag:
        for i in indices:
            if pool[i] not in key_count:
                key_count[pool[i]] = 0
            key_count[pool[i]] += 1
        if num >= max_num:
            return
        num += 1
        yield list(pool[i] for i in indices)

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return

        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1

        legal_flag = True
        for k in indices:
            if pool[k] in key_count and key_count[pool[k]] >= repeat_times:
                legal_flag = False
                break

        if legal_flag:
            for k in indices:
                if pool[k] not in key_count:
                    key_count[pool[k]] = 0
                key_count[pool[k]] += 1
            if num >= max_num:
                return
            num += 1
            yield list(pool[i] for i in indices)


def permutations(iterable, r=None, repeat_times=sys.maxsize, max_num=2000):
    key_count = {}
    num = 0
    pool = tuple(iterable)
    n = len(iterable)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n - r, -1))

    legal_flag = True
    for i in indices[:r]:
        if pool[i] in key_count and key_count[pool[i]] >= repeat_times:
            legal_flag = False
            break
    if legal_flag:
        for i in indices[:r]:
            if pool[i] not in key_count:
                key_count[pool[i]] = 0
            key_count[pool[i]] += 1
        if num >= max_num:
            return
        num += 1
        yield list(pool[i] for i in indices[:r])

    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]

                legal_flag = True
                for k in indices[:r]:
                    if pool[k] in key_count and key_count[pool[k]] >= repeat_times:
                        legal_flag = False
                        break

                if legal_flag:
                    for k in indices[:r]:
                        if pool[k] not in key_count:
                            key_count[pool[k]] = 0
                        key_count[pool[k]] += 1
                    if num >= max_num:
                        return
                    num += 1
                    yield list(pool[i] for i in indices[:r])
                break
        else:
            return


# if __name__=='__main__':
#     pl=list(range(8))
#     r=6
#     plist = list(permutations(pl, r, repeat_times=20000,))
#     print(f'排列数的个数为{len(plist)}。')
#     print('它们是:\n',plist)
#
# if __name__ == '__main__':
#     cl = list(range(42))
#     r = 6
#     clist = list(combinations(cl, r, max_num=2000))
#     print(f'组合数的个数为{len(clist)}。')
#     print('它们是:\n', clist)
