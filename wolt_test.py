import woltapp_api
import unittest



#Testing of fee calculation

class TestWoltApp(unittest.TestCase):
    def test_fee(self):
        self.assertEqual (woltapp_api.calculate_fee(790, 2235, 4, "2021-10-12T13:00:00Z"), 710)
                
    def test_rush_hour_fee(self):
        self.assertEqual (woltapp_api.calculate_fee(790, 2235, 4, "2023-01-20T16:00:00Z"), 852)    
    
    def test_maximum_fee_cannot_surpass_15_euro(self):
        self.assertEqual (woltapp_api.calculate_fee(790, 32323232323, 4, "2021-10-12T13:00:00Z"), 1500)
        
    def test_fee_should_be_0_when_cart_value_over_100_euro(self):
        self.assertEqual (woltapp_api.calculate_fee(10100, 2235, 4, "2021-10-12T13:00:00Z"), 0)
        
    def test_default_fee(self):
        self.assertEqual (woltapp_api.calculate_fee(1000, 999, 4, "2021-10-12T13:00:00Z"), 200)
        
    def test_distance_increments(self):
        for x in range(5):
            self.assertEqual (woltapp_api.calculate_fee(1000, (1000 + (500 * x)), 4, "2021-10-12T13:00:00Z"), (200 + (woltapp_api.ADDITIONAL_DISTANCE_FEE * x)))
             
    def test_exta_item_increments(self):
        for x in range(5):
            self.assertEqual (woltapp_api.calculate_fee(1000, 1000, (4+(1*x)), "2021-10-12T13:00:00Z"), (200 + (woltapp_api.EXTRA_ITEM_FEE * x)))
                
    def test_bulk_order_fee(self):
        self.assertEqual (woltapp_api.calculate_fee(1000, 999, 12, "2021-10-12T13:00:00Z"), 600)
        self.assertEqual (woltapp_api.calculate_fee(1000, 999, 13, "2021-10-12T13:00:00Z"), 770)
    
    def test_small_order_fee(self):
        self.assertEqual (woltapp_api.calculate_fee(1000, 999, 4, "2021-10-12T13:00:00Z"), 200)      
        self.assertEqual (woltapp_api.calculate_fee(500, 999, 4, "2021-10-12T13:00:00Z"), 700)

           
if __name__ == '__main__':
    unittest.main()            