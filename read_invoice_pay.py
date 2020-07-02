import json


def playFor(aPerformance):
    with open('./plays.json') as f:
        plays = json.load(f)
    play_id = aPerformance["playID"]
    play = plays[play_id]
    return play


def amountFor(aPerformance):
    result = 0
    #     play = playFor(aPerformance)
    #     play_type = playFor(aPerformance)["type"]
    if playFor(aPerformance)["type"] == "tragedy":
        result = 40000
    if aPerformance["audience"] > 30:
        result += 1000 * (aPerformance["audience"] - 30)
    elif playFor(aPerformance)["type"] == "comedy":
        result = 30000
    if aPerformance["audience"] > 20:
        result += 10000 + 500 * (aPerformance["audience"] - 20)
        result += 300 * aPerformance["audience"]
    else:
        return "unknown type"
    return result


class StatementData:
    pass


def statement(invoice: {}, plays: {}):
    statementData = StatementData()
    customer_invoice = invoice[0]
    statementData.customer = customer_invoice["customer"]
    statementData.performances = customer_invoice["performances"]
    return renderPlanText(statementData)


def renderPlanText(data):
    #     customer_invoice = invoice[0]
    result = 'Statement for {}\n'.format(data.customer)

    for perf in data.performances:
        #  // print line for this order
        result += '  {}: ${} {}seats \n'.format(
            playFor(perf)["name"],
            amountFor(perf) / 100, perf["audience"])

    result += 'Amount owed is ${}\n'.format(totalAmount(data) / 100)
    result += "You earned ${} credits".format(totalVolumeCredits(data))
    return result


def totalAmount(data):
    total_amount = 0
    for perf in data.performances:
        total_amount += amountFor(perf)
        return total_amount


def totalVolumeCredits(data):
    volumeCredits = 0
    for perf in data.performances:
        volumeCredits += volumeCreditsFor(perf)
    return volumeCredits


def volumeCreditsFor(aPerf):
    result = 0
    result += max(aPerf["audience"] - 30, 0)
    #     // add extra credit for every ten comedy attendees
    if "comedy" == playFor(aPerf)["type"]:
        result += (aPerf["audience"] // 5)
    return result


def main():
    with open('./plays.json') as f:
        plays = json.load(f)

#     print(data)

    with open('./invoices.json') as g:
        invoice = json.load(g)


#     print(invoice)

    result = statement(invoice, plays)
    print(result)

if __name__ == "__main__":
    main()
