init python:
    def recreate_character(name):
        try:
            renpy.file("../characters/" + name + ".chr")
            delete_character(name)
            open(config.basedir + "/characters/" + name + ".chr", "wb").write(renpy.file(name + ".chr").read())
        except: pass

    # Prevent the translation of the player's name
    mc.name = 'player + "{w}"'

define config.rtl = False
define config.check_translate_none = False

translate None python:
    # Dialog suffixes and prefixes
    for char in [mc, s, m, n, y, ny]:
        char.what_prefix = '"'
        char.what_suffix = '"'

    # Replace .chr files
    recreate_character('sayori')
    recreate_character('monika')
    recreate_character('natsuki')
    recreate_character('yuri')
