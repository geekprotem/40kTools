
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

Every YAML file should look like this:

```
units:
  - name: SOME_NAME
    datasheet: DATASHEET_NAME
    points value: POINTS_VALUE
    type: character|battleline|dedicated transport|other
    models: NUMBER_OF_MODELS
    equipment: []

```
With each unit being an item in the `units` array.


Any additional attributes are ignored, but can be useful to have.  For example, this can be used for crusade forces where you can also track that information or even details on how to assemble/paint the models.


## TODO

* make it possible to have a unit with 2 different definitions to represent optional loadouts (for those that magnetize weapons or have swappable models)

* add the ability to have a definition file to determine what picks to use
