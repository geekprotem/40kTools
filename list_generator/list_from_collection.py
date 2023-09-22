
import os
import random

import argparse
import yaml

parser = argparse.ArgumentParser(description='Generate an army from a collection.')
parser.add_argument(
  '-c', '--collection',
  type=str,
  help='the path to the collection directory'
)
parser.add_argument(
  '-s', '--size',
  type=int,
  default=2000,
  help='max points for the list'
)
parser.add_argument(
  '-v', '--verbosity',
  type=str,
  choices=['simple','detailed'],
  default='simple',
  help='detail of output'
)
parser.add_argument(
  '-a', '--all',
  required=False,
  help='show full collection',
  action='store_true'
)
parser.add_argument(
  '-d', '--datasheet',
  required=False,
  help='include datasheet',
  action='append',
  default = []
)
parser.add_argument(
  '-e', '--exclude',
  required=False,
  help='exclude datasheet',
  action='append',
  default = []
)

args = parser.parse_args()

datasheets_to_include = {}
for datasheet in args.datasheet:
  if datasheet not in datasheets_to_include:
    datasheets_to_include[datasheet] = 0
  datasheets_to_include[datasheet] = datasheets_to_include[datasheet] + 1


def main(
    force = str,
    game_size = int,
    verbosity = str,
    showall = bool,
    datasheets_to_include = dict,
    datasheets_to_exclude = list,
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
    datasheets_to_include = datasheets_to_include,
    datasheets_to_exclude = datasheets_to_exclude,
  )
  if result is None:
    print("unable to get compulsory character!")
    exit(1)

  if result['unit']['datasheet'] in datasheets_to_include:
    datasheets_to_include[result['unit']['datasheet']] = datasheets_to_include[result['unit']['datasheet']] - 1
    if datasheets_to_include[result['unit']['datasheet']] == 0:
      del datasheets_to_include[result['unit']['datasheet']]
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
      datasheets_to_include = datasheets_to_include,
      datasheets_to_exclude = datasheets_to_exclude,
    )
    if result is None:
      break

    if result['unit']['datasheet'] in datasheets_to_include:
      datasheets_to_include[result['unit']['datasheet']] = datasheets_to_include[result['unit']['datasheet']] - 1
      if datasheets_to_include[result['unit']['datasheet']] == 0:
        del datasheets_to_include[result['unit']['datasheet']]
    del inventory[result['name']]
    total = total + result['unit']['points value']
    selected[result['name']] = result['unit']

  display_list(
    units = selected,
    verbosity=verbosity,
    size=game_size,
  )


def display_list(
    units = dict,
    verbosity = str,
    size = str,
):
  total = 0
  output = {}
  for name, unit in units.items():
    if verbosity == 'simple':
      output[f"{unit['datasheet']} / {name} ({unit['type']})"] = unit['points value']

    if verbosity == 'detailed':
      output[f"{unit['datasheet']} {name}"] = {
        'points value': unit['points value'],
        'equipment': unit['equipment'],
        'type': unit['type'],
      }

    total = total + unit['points value']
  print(yaml.safe_dump(output))
  print(f"{len(output)} units for {total}/{size} points")


def pick_unit(
    inventory = dict,
    pick_type = str,
    budget = int,
    selected = dict,
    showall = bool,
    datasheets_to_include = dict,
    datasheets_to_exclude = list,
):
  # print(f" picking a {pick_type}")
  unit_names = list(inventory.keys())
  random.shuffle(unit_names)
  for unit_name in unit_names:
    # print(f" {unit_name}")
    if pick_type is not None and inventory[unit_name]['type'] != pick_type:
      continue
    if len(datasheets_to_exclude) > 0 and inventory[unit_name]['datasheet'] in datasheets_to_exclude:
      continue
    if len(datasheets_to_include) > 0 and inventory[unit_name]['datasheet'] not in datasheets_to_include:
      # print(f"{unit_name}/{inventory[unit_name]['name']} trigger skip!")
      continue
    # print(f"  validating {unit_name}")
    if validate_pick(selected=selected,budget=budget,unit=inventory[unit_name]) is True or showall is True:
      # print(f"  pick made! {unit_name}")
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
    datasheet_name=unit['datasheet'],
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
    if unit['datasheet'] == datasheet_name:
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
          unit['datasheet']['datasheet'] = unit['datasheet']['name']
          inventory[unit['name']] = unit['datasheet']
      else:
        content['datasheet']['datasheet'] = content['datasheet']['name']
        inventory[content['name']] = content['datasheet']
  return inventory



main(
  force=args.collection,
  game_size=args.size,
  verbosity=args.verbosity,
  showall=args.all,
  datasheets_to_include=datasheets_to_include,
  datasheets_to_exclude=args.exclude,
)
