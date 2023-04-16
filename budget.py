class Category:

  def __init__(self, name) -> None:
    self.name = name
    self.balance = 0
    self.ledger = []
    pass
  
  def deposit (self, amount, description = ""):
    self.balance += amount
    self.ledger.append({
      'amount': amount,
      'description': description
    })

  def withdraw (self, amount, description = ""):
    if self.balance >= amount:
      self.balance -= amount
      self.ledger.append({
        'amount': -amount,
        'description': description
      })
      return True
    return False

  def get_balance (self):
    return self.balance

  def transfer (self, amount, budget):
    if self.balance >= amount:
      self.balance -= amount
      budget.deposit(amount,"Transfer from " + self.name)
      self.ledger.append({
        'amount': -amount,
        'description': "Transfer to " + budget.name,
      })
      return True
    return False
  
  def check_funds (self, amount):
    return self.balance >= amount
  
  def __str__(self) -> str:
    print(self.ledger)
    descriptionsLengths = map(lambda item: len(item['description']), self.ledger)
    descriptionLength = min(max(descriptionsLengths), 23)

    numbersLengths = map(lambda item: len("{:.2f}".format(item['amount'])), self.ledger)
    numberLength = max(numbersLengths)

    line_items = ""

    line_header = self.name.capitalize().center(descriptionLength+numberLength+1, '*')+'\n'

    total = 0

    for operation in self.ledger:
      description = operation['description'][0:23].ljust(descriptionLength)
      amount = "{:.2f}".format(operation['amount']).rjust(numberLength)
      line_items += (description+" "+amount+'\n')
      total += operation['amount']

    line_total = "Total: "+"{:.2f}".format(total)
    return line_header+line_items+line_total


def create_spend_chart(categories):
  total_expenses = 0
  categories_names = []

  for category in categories:
    categories_names.append(category.name)
    for operation in category.ledger:
      if(operation['amount'] < 0):
        total_expenses += operation['amount']

  percentageRows = []
  for i in range(10, -1, -1):
    filling = []

    for category in categories:

      category_expenses = 0

      for operation in category.ledger:
        if(operation['amount'] < 0):
          category_expenses += operation['amount']
      
      expenses_percentage = category_expenses / total_expenses * 100

      #print("Category",category.name,"has",category_expenses,". Percentage:",expenses_percentage)
      if(expenses_percentage >= i*10):
        filling.append(True)
      else:
        filling.append(False)

    percentageRows.append({
      "percentage": i*10,
      "values": filling
    })

  largest_category_name = max(map(lambda name: len(name), categories_names))

  title_line = "Percentage spent by category\n"
  
  formattedPercentageRows = ''
  for row in percentageRows:
    formattedPercentageRows += str(row["percentage"]).rjust(3) + "| "
    for filled in row['values']:
      if(filled):
        formattedPercentageRows += 'o  '
      else:
        formattedPercentageRows += '   '
    formattedPercentageRows += '\n'

  underline = "-".center(len(categories)*3+1, "-").rjust(5+len(categories)*3)+"\n"

  titles_lines = ""
  
  for i in range(largest_category_name):
    line = ''
    for category_name in categories_names:
      if(len(category_name) > i):
        line += category_name[i] + "  "
      else:
        line += "   "
    line = line.rjust(5+len(categories)*3)
    if(i < largest_category_name-1):
      line += "\n"
    titles_lines += line

  chart = title_line + formattedPercentageRows + underline + titles_lines
  return chart