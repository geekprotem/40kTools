
import os
import random

import argparse
import yaml

parser = argparse.ArgumentParser(description='Generate an army from a collection.')
parser.add_argument(
  '-c',
  type=str,
  help='the path to the collection'
)
parser.add_argument(
  '-s',
  type=int,
  default=1000000,
  help='max points for the list'
)
parser.add_argument(
  '-v',
  type=str,
  choices=['simple','detailed'],
  default='simple',
  help='detail of output'
)
parser.add_argument(
  '-a',
  required=False,
  help='show full collection',
  action='store_true'
)

args = parser.parse_args()

def main(
    force = str,
    game_size = int,
    verbosity = str,
    showall = bool,
):
  unit_files = os.listdir(f"{force}/units")
  unit_files.sort()

  inventory = load_inventory(
    path=f"{force}/units"
  )

  selected = {}
  total = 0

  result = pick_unit(
    inventory = inventory,
    pick_type = 'character',
    budget = game_size,
    selected = selected,
    showall = showall,
  )
  if result is None:
    print("unable to get compulsory character!")
    exit(1)
  del inventory[result['name']]
  total = total + result['unit']['points value']
  selected[result['name']] = result['unit']

  while True:
    result = pick_unit(
      inventory = inventory,
      pick_type = None,
      budget = game_size - total,
      selected = selected,
      showall = showall,
    )
    if result is None:
      break
    del inventory[result['name']]
    total = total + result['unit']['points value']
    selected[result['name']] = result['unit']

  display_list(
    units = selected,
    verbosity=verbosity
  )


def display_list(
    units = dict,
    verbosity = str,
):
  total = 0
  output = {}
  for name, unit in units.items():
    if verbosity == 'simple':
      output[f"{unit['name']} / {name} ({unit['type']})"] = unit['points value']

    if verbosity == 'detailed':
      output[f"{unit['name']} {name}"] = {
        'points value': unit['points value'],
        'equipment': unit['equipment'],
        'type': unit['type'],
      }

    total = total + unit['points value']
  print(yaml.safe_dump(output))
  print(f"{len(output)} units for {total} points")


def pick_unit(
    inventory = dict,
    pick_type = str,
    budget = int,
    selected = dict,
    showall = bool,
):
  unit_names = list(inventory.keys())
  random.shuffle(unit_names)
  for unit_name in unit_names:
    if pick_type is not None and inventory[unit_name]['type'] == pick_type:
      continue
    if validate_pick(selected=selected,budget=budget,unit=inventory[unit_name]) is True or showall is True:
      return {
        'name': unit_name,
        'unit': inventory[unit_name]
      }
  return None


def validate_pick(
    selected = dict,
    budget = int,
    unit = dict,
):
  if unit['points value'] > budget:
    return False

  count = count_datasheet_instances(
    datasheet_name=unit['name'],
    units=selected,
  )

  if unit['type'] == 'character' and count == 3:
    return False

  if unit['type'] == 'other' and count == 3:
    return False

  if unit['type'] == 'battleline' and count == 6:
    return False
  
  if unit['type'] == 'dedicated transport':
    if count == 6:
      return False

    dedicated_transports_count = count_types_instances(
      unit_types=['dedicated transport'],
      units=selected,
    )

    not_dedicated_transports_count = count_types_instances(
      unit_types=['character','battleline','other'],
      units=selected,
    )

    if dedicated_transports_count == not_dedicated_transports_count:
      return False

  return True


def count_types_instances(
    unit_types = list,
    units = dict,
):
  count = 0
  for name, unit in units.items():
    if unit['type'] in unit_types:
      count = count + 1
  return count


def count_datasheet_instances(
    datasheet_name = str,
    units = dict,
):
  count = 0
  for name, unit in units.items():
    if unit['name'] == datasheet_name:
      count = count + 1
  return count


def load_inventory(
    path = str
):
  unit_files = os.listdir(path)
  unit_files.sort()

  inventory = {}
  for filename in unit_files:
    with open(f"{path}/{filename}", 'r') as file:
      content = yaml.safe_load(file)
      # print(filename)
      if 'units' in content:
        for unit in content['units']:
          inventory[unit['name']] = unit['datasheet']
      else:
        inventory[content['name']] = content['datasheet']
  return inventory



main(
  force=args.c,
  game_size=args.s,
  verbosity=args.v,
  showall=args.a,
)
