class Intent:
  pass

class BARTQueryIntent(Intent):
  def __init__(self):
    pass

class BusQueryIntent(Intent):
  def __init__(self):
    pass

class HelpIntent(Intent):
  def __init__(self):
    pass

class IntentRecognizer: 
  def recognize(self, message):
    pass