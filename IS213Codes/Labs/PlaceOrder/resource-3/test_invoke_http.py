from invokes import invoke_http

# results  = invoke_http("http://localhost:5000/book", method='GET')

# print( type(results) )
# print()
# print( results )

isbn = '9213213213213'
book_details = { "availability": 5, "price": 213.00, "title": "ESD" }
create_results = invoke_http(
        "http://localhost:5000/book/" + isbn, method='POST', 
        json=book_details
    )

print()
print(create_results)
