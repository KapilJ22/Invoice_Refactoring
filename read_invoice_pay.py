import json


def read_invoice_plays_print(invoice: {}, plays: {}):
    total_amount = 0
    volumeCredits = 0

    #     print(invoice)
    #     print(json.dumps(plays, indent=4, sort_keys=True))
    #     print(json.dumps(invoice, indent=4, sort_keys=True))
    customer_invoice = invoice[0]
    print()
    result = 'Statement for {}\n'.format(customer_invoice["customer"])
    print(result)
    print("customer_invoice: {}".format(customer_invoice))
    for perf in customer_invoice["performances"]:
        thisAmount = 0
        play_id = perf["playID"]
        play_type = plays[play_id]["type"]
        if play_type == "tragedy":
            thisAmount = 40000
            if perf["audience"] > 30:
                thisAmount += 1000 * (perf["audience"] - 30)
        elif play_type == "comedy":
            thisAmount = 30000
            if perf["audience"] > 20:
                thisAmount += 10000 + 500 * (perf["audience"] - 20)
                thisAmount += 300 * perf["audience"]

        else:
            return "unknown type"

        # // add volume credits
        volumeCredits += max(perf["audience"] - 30, 0)
        #     // add extra credit for every ten comedy attendees
        if "comedy" == play_type:
            volumeCredits += (perf["audience"] // 5)

        #  // print line for this order
        result += '  {}: ${} {}seats \n'.format(play_id, thisAmount / 100,
                                                perf["audience"])
        total_amount += thisAmount

    result += 'Amount owed is ${}\n'.format(total_amount / 100)
    result += "You earned ${} credits".format(volumeCredits)
    return result


def main():
    with open('./plays.json') as f:
        plays = json.load(f)

#     print(data)

    with open('./invoices.json') as g:
        invoice = json.load(g)


#     print(invoice)

    result = read_invoice_plays_print(invoice, plays)
    print(result)

if __name__ == "__main__":
    main()
