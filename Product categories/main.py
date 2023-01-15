class Category:
    def __init__(self, cat_name):
        self.cat_name = cat_name
        self.ledger = list()
        self.__money = 0

    def deposit(self, amount, description=str()):
        self.__money += amount
        self.ledger.append({
            'amount': amount,
            'description': description
        })

    def withdraw(self, amount, description=str()):
        if self.check_funds(amount):
            self.__money -= amount
            self.ledger.append({
                'amount': -amount,
                'description': description
            })
            return True
        return False

    def get_balance(self):
        return self.__money

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.cat_name}')
            category.deposit(amount, f'Transfer from {self.cat_name}')
            return True
        return False

    def check_funds(self, amount):
        if amount > self.__money:
            return False
        return True

    def __str__(self):
        len_head = 30 - len(self.cat_name)
        head = ''.join("*" for _ in range(len_head // 2)) + self.cat_name + ''.join("*" for _ in range(len_head // 2))
        body = ''
        for itm in self.ledger:
            amount_str = str(round(float(itm.get('amount')), 2))[0:10]
            if len(amount_str.split('.')[1]) == 1:
                amount_str += "0"
            underscore_str = 30 - len(itm.get('description')[:23]) - len(amount_str)
            itm_str = itm.get('description')[:23] + ''.join(" " for _ in range(underscore_str)) + amount_str
            body += itm_str + '\n'
        return head + '\n' + body + f'Total: {self.__money}'


def create_spend_chart(categories: list):
    all_costs = 0
    n = 100
    category_costs = {}
    category_costs_percent = {}
    res_str = 'Percentage spent by category\n'
    for category in categories:
        for costs in category.ledger:
            x = costs.get('amount')
            if x < 0:
                all_costs += x
                if category.cat_name in category_costs:
                    category_costs[category.cat_name] += x
                else:
                    category_costs[category.cat_name] = x
    for key, value in category_costs.items():
        category_costs_percent[(round(value / all_costs, 2)) * 100] = key

    # print(category_costs_percent)
    while n >= 0:
        if n == 100:
            res_str += f'{n}|'
            for key, value in category_costs_percent.items():
                if n in range(1, int(key) + 1):
                    res_str += " o "
                else:
                    res_str += "   "
            res_str += ' \n'

        if n % 10 == 0 and 0 < n < 100:
            res_str += f' {n}|'
            for key, value in category_costs_percent.items():
                if n in range(1, int(key) + 1):
                    res_str += " o "
                else:
                    res_str += "   "
            res_str += ' \n'

        if n == 0:
            res_str += f'  {n}|'
            for key, value in category_costs_percent.items():

                if n in range(0, int(key) + 1):
                    res_str += " o "
                else:
                    res_str += "   "
            res_str += ' \n'
        n -= 10
    res_str += '    ----------\n'

    for char in range(max(map(lambda x: len(x), category_costs_percent.values()))):
        res_str += "    "
        for key, value in category_costs_percent.items():
            try:
                res_str += f' {value[char]} '
            except IndexError:
                res_str += '   '
        res_str += " \n"

    return res_str[:len(res_str) - 1]


food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
