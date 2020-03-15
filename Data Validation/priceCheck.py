def priceCheck(products, productPrices, productSold, soldPrice):
    productsdict = dict(zip(products, productPrices))
    productsolddict = dict(zip(productSold, soldPrice))
    shared_items = {k: productsdict[k] for k in productsdict if k in productsolddict and productsdict[k] != productsolddict[k]}
    return len(shared_items)


products = ['rice', 'sugar', 'wheat', 'cheese', 'water', 'rice']
productPrices=[16.89, 56.92, 20.89, 345.99, 28.99, 16.89]
productSold =['rice', 'cheese', 'water', 'rice']
soldPrice =[18.99, 400.89, 27.99, 16.89]

print(priceCheck(products,productPrices,productSold,soldPrice))