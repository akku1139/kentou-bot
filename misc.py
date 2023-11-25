from replit import db

def get_kentou_speed():
  return float(db["kentou_speed"])

def key_test_and_create(key:str):
  try:
    db[key]
  except KeyError:
    db[key] = 0
