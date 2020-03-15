def priceCheck(products, productPrices, productSold, soldPrice):
    productsdict = dict(zip(products, productPrices))                # zip the products lookup list together and create a dictionary
    productsolddict = dict(zip(productSold, soldPrice))              # zip the product purchases list together and create a dictionary
    shared_items = {k: productsdict[k] for k in productsdict if k in productsolddict and productsdict[k] != productsolddict[k]} # compare the dictionaries
    return len(shared_items)                                        # return the delta between the two dictionaries


products = ['rice', 'sugar', 'wheat', 'cheese', 'water', 'rice']
productPrices=[16.89, 56.92, 20.89, 345.99, 28.99, 16.89]
productSold =['rice', 'cheese', 'water', 'rice']
soldPrice =[18.99, 400.89, 27.99, 16.89]

print(priceCheck(products,productPrices,productSold,soldPrice))