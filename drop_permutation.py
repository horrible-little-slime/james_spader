from sympy.utilities.iterables import multiset_permutations
class DropPermutation:
    too_big_skipped = []
    def __init__(self, name, drops):
        self.name = name
        self.base_drops = drops
        self.orders = list(multiset_permutations(drops)) if len(self.base_drops) <= 7 else []
        if self.orders == []:
            DropPermutation.too_big_skipped.append(name)
    
    def filter_options(self, drop_order):
        if self.orders == []: return
        drop_order = [drop for drop in drop_order if drop in self.base_drops]
        if not self.__verify_drops_make_sense(drop_order): return
        if len(drop_order) <= 1: return
        old_orders = self.orders
        self.orders = [ possible_order for possible_order in old_orders if DropPermutation.__test_drop_order(possible_order, drop_order) ]
        if not len(self.orders):
            print(str(old_orders))
            raise Exception("Drop order %s caused monster to have no valid orders remaining!" % str(drop_order))
    
    @staticmethod
    def __test_drop_order(drop_order_to_test, actual_drop_order):
        i = -1
        for drop in actual_drop_order:
            try:
                i = drop_order_to_test.index(drop, i + 1)
            except:
                return False
        return True
    
    def __verify_drops_make_sense(self, drop_order):
        for drop in drop_order:
            if drop_order.count(drop) > self.base_drops.count(drop):
                print("drops don't make sense for monster %s: %s appears too often" % (self.name, drop))
                return False
        return True
