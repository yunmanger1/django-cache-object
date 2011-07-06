from cache_object.loading import Cache

def test_stuff():
    cache1 = Cache('cron')
    class NewCache(Cache):
        pass
    cache2 = NewCache('category')

    var = 'value'
    cache1.add_object(var, 'key')


    print cache1.get_object('key')
    print cache2.get_object('key')

