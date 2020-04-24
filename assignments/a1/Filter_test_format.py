customers = create_customers(test_dict)
process_event_history(test_dict, customers)
calls = []
hist = customers[0].get_history()
calls.extend(hist[0])
d = CustomerFilter().apply(customers, calls, 'L50')
