
## Summary

Looks at your 40K collection and builds an army list following some simple rules:

* must have at least one character
* must fit within the budget
* no more `dedicated transports` than non-`dedicated transport` units
* adheres to the rule of 3/6

More logic might come later, but this is just to make pick up and casual games more interesting.

## Usage

```
python list_from_collection.py -c PATH_TO_COLLECTION -s SIZE_OF_BATTLE
```

### Additional options

Use `-h` to see all options.


## Collection

This assumes your collection is in a directory somewhere as a glob of YAML files.

Whatever directory you point this at, it will look in the `units` subdirectory within.

Every YAML file in there should look like one of these two formats:

```
name: SOME_NAME
datasheet:
  name: DATASHEET_NAME
  points value: POINTS_VALUE
  type: character|battleline|dedicated transport|other
  equipment: []
```

`name` must be unique across your whole collection.

`equipment` is optional these days, but can be a list of the options the unit/model is equipped with.

Alternatively, you can list multiple units in a single file:

```
units:
  - name: SOME_NAME
    datasheet:
      name: DATASHEET_NAME
      points value: POINTS_VALUE
      type: character|battleline|dedicated transport|other
      equipment: []

  - name: SOME_OTHER_NAME
    datasheet:
      name: DATASHEET_NAME
      points value: POINTS_VALUE
      type: character|battleline|dedicated transport|other
      equipment: []
```

Any attributes that aren't `name` or `datasheet` are ignored, but can be useful to have.  For example, this can be used for crusade forces where you can also track that information or even details on how to assemble/paint the models.


## TODO

* make it possible to have a unit with 2 different definitions to represent optional loadouts (for those that magnetize weapons or have swappable modles)

* add option to restrict the number of units of a particular type|datasheet

* add the ability to have a definition file to determine what picks to use
