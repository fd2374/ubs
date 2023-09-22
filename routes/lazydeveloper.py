from typing import Dict, List
""" Assumptions:
  1. word can only be key or enum
  2. When a statement asks for the next likely word 
     that represents or refers to a Polymorphic type,   
     the next likely word can either be the enum or a 
     key-value pair belonging to one of its subclasses.

     Examples (assume json is same as provided in original replit)
  1. "Ord" -> [""] exp: Ord is class so empty
  2. "Order.orderType.p" -> ["price"] exp: "only LimitOrderType has
     "price" so we know orderType's type even though if it is polymorphic"
  3. "OrderType." -> [""] exp: multiple sub classes have possible answer
  4. "OrderType.M" -> [""] exp: MarketOrderType is a Polymorphic type, so we won't output it, and there is no enum or key-value pair belonging to one of its subclasses, so we output nothing
"""

# check if type is Class or not
def isClass(obj, dict):
  if obj in dict:
    return True
  return False


"""
  check if all elements in obj are class
  obj is array of elements
"""


def allClass(obj, dict):
  for c in obj:
    if not isClass(c, dict):
      return False
  return True


"""
  extract class name from string
  E.g: List<Allocation> returns Allocation
  E.g: List<List<Allocation>> returns Allocation
"""


def extractClass(classStr):
  index1 = classStr.find("<")
  index2 = classStr.rfind(">")
  while index1 > -1 and index2 > -1:
    classStr = classStr[index1 + 1:index2]
    index1 = classStr.find("<")
    index2 = classStr.rfind(">")
  return classStr


"""
  this function will navigate through the json until
  it reaches the last class before recommendation
  E.g: Object -> orderType
"""


def search(keys, dict):
  if len(keys) == 0:
    return []
  next = dict[keys[0]]
  for i in range(1, len(keys)):
    keys[i] = extractClass(keys[i])
    #if key or type is Class then we start search from root again
    if isClass(keys[i], dict):
      next = dict[keys[i]]
    elif type(next) != str and type(next[keys[i]]) == str and isClass(extractClass(next[keys[i]]),
                                                dict):
      next = dict[extractClass(next[keys[i]])]
    elif type(next) != str:
      #otherwise we just keep going :)
      next = next[keys[i]]
  return next


"""
  if the result of search happen to polymorphic type
  we need to recursively search all subClasses to retrieve
  the words and deep_search will answers as array
  E.g: [["price": "Integer"], [""], ["password": "String"]]
"""


def deep_search(result, dict, dpVisited):
  ans = []
  if allClass(result, dict):
    for res in result:
      if res not in dpVisited:
        dpVisited[res] = 1
        ans.append(deep_search(dict[res], dict, dpVisited))
  else:
    return [result]
  return ans if len(ans) > 0 else [{"": ""}]


"""
  search how many times our answer appears
  from the deep_search result we did
  counter is how many times it appeared
"""


def checker(value, deep_result, result):
  counter = 0
  add = 0
  if type(deep_result) == list:
    for i in deep_result:
      counter += checker(value, i, result)
  else:
    for i in deep_result:
      if i.startswith(value):
        add = 1
        result.append(i)
  counter += add
  return counter


def remove_outer_lists(nested_list):
  if isinstance(nested_list, list):
    if len(nested_list) == 1 and isinstance(nested_list[0], list):
      return remove_outer_lists(nested_list[0])
    else:
      return [remove_outer_lists(item) for item in nested_list]
  else:
    return nested_list


def getNextProbableWords(classes: List[Dict],
                         statements: List[str]) -> Dict[str, List[str]]:
  #Todo-2: Speed up other functions if possible
  classes_dict = classes[0]
  #start searching for the answer
  output = {}
  for statement in statements:
    keys = statement.split(".")
    value = keys.pop()
    try:
      result = search(keys, classes_dict)
    except Exception as error:
      print(error)
      output[statement] = [""]
      continue
    #run recursion from here if last result is classes because it can go crazy long
    dpVisited = {}
    deep_result = deep_search(result, classes_dict, dpVisited)
    counter = 0
    # if polymorphic then check if there are multiple answer
    if len(deep_result) == 1 and type(deep_result[0]) == str and deep_result[0] not in classes_dict:
      output[statement] = [""]
      continue
    if len(deep_result) > 1:
      tempResult = []
      counter = checker(value, deep_result, tempResult)
      # if counter is 0 or 1 then we are sure where the answer is
      if counter < 2:
        result = tempResult
      else:
        output[statement] = [""]
    if counter < 2:
      #after deep search result can have many layers around
      deep_result = remove_outer_lists(deep_result)
      if type(deep_result[0]) == str:
        result = deep_result
      # process the result that matches with value
      answers = [res for res in result if (res.startswith(value) and res != value)]
      answers.sort()
      # if now answer then [""]
      output[statement] = [] if len(answers) > 0 else [""]
      #now just print top 5
      for i in range(min(5, len(answers))):
        output[statement].append(answers[i])
  return output