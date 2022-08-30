def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(iterable)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield tuple(pool[i] for i in indices)



if __name__=='__main__':
    cl="123456789"
    r=5
    clist=list(combinations(cl, r))
    print(f'组合数的个数为{len(clist)}。')
    print('它们是:\n',clist)