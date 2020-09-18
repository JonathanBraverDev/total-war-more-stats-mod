import csv
import math

def opendbread(tablename):
  tsv_file = open("extract/db/" + tablename + "/" + "data__.tsv", encoding="utf-8")
  return tsv_file

def openlocread(tablename):
  tsv_file = open("extract/text/db/" + tablename + "__.tsv", encoding="utf-8")
  return tsv_file


# shield
tsv_file = opendbread("unit_shield_types_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
shields = {}

rowid = 0
shields_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        shields_keys[key] = i
        i = i + 1
  if rowid > 2:
      shields[row[shields_keys["key"]]] = row[shields_keys["missile_block_chance"]]
tsv_file.close()

# melee
tsv_file = opendbread("melee_weapons_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
melee = {}

rowid = 0
melee_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        melee_keys[key] = i
        i = i + 1
  if rowid > 2:
      melee[row[melee_keys["key"]]] = row
tsv_file.close()

# armour
tsv_file = opendbread("unit_armour_types_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
armour = {}

rowid = 0
armour_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        armour_keys[key] = i
        i = i + 1
  if rowid > 2:
      armour[row[armour_keys["key"]]] = row
tsv_file.close()

# projectiles
tsv_file = opendbread("projectiles_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
projectiles = {}

rowid = 0
projectiles_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        projectiles_keys[key] = i
        i = i + 1
  if rowid > 2:
      projectiles[row[projectiles_keys["key"]]] = row
tsv_file.close()

# ability phase stats
tsv_file = opendbread("special_ability_phase_stat_effects_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
ability_phase_stats = {}

rowid = 0
ability_phase_stats_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        ability_phase_stats_keys[key] = i
        i = i + 1
  if rowid > 2:
    key = row[ability_phase_stats_keys["phase"]]
    if key not in ability_phase_stats:
      ability_phase_stats[key] = []
    ability_phase_stats[key].append(row)
tsv_file.close()

# ability phase attributes
tsv_file = opendbread("special_ability_phase_attribute_effects_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
ability_phase_attrs = {}

rowid = 0
ability_phase_attrs_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        ability_phase_attrs_keys[key] = i
        i = i + 1
  if rowid > 2:
    key = row[ability_phase_attrs_keys["phase"]]
    if key not in ability_phase_attrs:
      ability_phase_attrs[key] = []
    ability_phase_attrs[key].append(row)
tsv_file.close()

# ability phase details - done
# requested_stance -> special_ability_stance_enums - just an animation?
# fatigue_change_ratio: This is a scalar that changes the unit's fatigue (once off) relative to the maximum. For example, -0.25 will reduce it by 25% and 1.1 will increase it by 10%
# inspiration_aura_range_mod
# ability_recharge_change: if the unit has abilities, their recharge will be changed by that amount (negative will reduce the time, positive will increase the time)
# resurrect: If ticked, when healing excess hit points will resurrect dead soldiers
# hp_change_frequency: In seconds, how often hp (hit point) change should attempt to be applied 
# heal_amount: When HP (hit points) are healed, how much total should be changed, spread amoungst the entities
# damage_chance: Per entity, per frequency, what the chance is of applying damage; the effect is not linear, mostly effective in 0.00-0.02
# damage_amount: Per entity, per frequency, what the amount of damage to apply
# max_damaged_entities: Per damage/heal frequency, how many entities can we affect (negative is no limit)
# mana_regen_mod: How much we add to the current recharge for mana per second
# mana_max_depletion_mod: How much we add to the current value for max mana depletion
# imbue_magical: Does this phase imbue the target with magical attacks?
# imbue_ignition: Does this phase imbue the target with flaming attacks?
# imbue_contact: -> special_ability_phases Does this phase imbue the target with a contact phase when attacking?
# recharge_time
# is_hidden_in_ui
# affects_allies
# affects_enemies
# replenish_ammo: How much ammunition we want to replenish when phase starts (can be negative if we want to spend), this value is in percentage of unit max ammo

tsv_file = opendbread("special_ability_phases_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
ability_phase_details = {}

rowid = 0
ability_phase_details_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        ability_phase_details_key[key] = i
        i = i + 1
  if rowid > 2:
      ability_phase_details[row[ability_phase_details_key["id"]]] = row
tsv_file.close()

def ability_phase_details_stats(phaseid, indent = 0, title=""):
  result = ""
  details = ability_phase_details[phaseid]
  affects_allies = "affects_allies " if details[ability_phase_details_key["affects_allies"]] == 'true' else ""
  affects_enemies = "affects_enemies " if details[ability_phase_details_key["affects_enemies"]] == 'true' else ""
  unbreakable = "unbreakable " if details[ability_phase_details_key["unbreakable"]] == 'true' else ""
  cantmove = "cant_move " if details[ability_phase_details_key["cant_move"]] == 'true' else ""
  freeze_fatigue = "freeze_fatigue " if details[ability_phase_details_key["freeze_fatigue"]] == 'true' else ""
  fatigue_change_ratio = "fatigue_change_ratio: " + numstr(details[ability_phase_details_key["fatigue_change_ratio"]]) + " " if details[ability_phase_details_key["fatigue_change_ratio"]] != '0.0' else ""
  duration = "(" + numstr(details[ability_phase_details_key["duration"]]) +"s) " if details[ability_phase_details_key["duration"]] != "-1.0" else ""
  col = "yellow"
  if details[ability_phase_details_key["effect_type"]] == 'positive':
    col = "green"
  elif details[ability_phase_details_key["effect_type"]] == 'negative':
    col = "red"
  replenish_ammo = "replenish_ammo: " + numstr(details[ability_phase_details_key["replenish_ammo"]]) +" " if details[ability_phase_details_key["replenish_ammo"]] != "0.0" else ""
  recharge_time = "recharge_time: " + numstr(details[ability_phase_details_key["recharge_time"]]) +" " if details[ability_phase_details_key["recharge_time"]] != "-1.0" else ""
  mana_regen_mod = "mana_recharge_mod: " + numstr(details[ability_phase_details_key["mana_regen_mod"]]) +" " if details[ability_phase_details_key["mana_regen_mod"]] != "0.0" else ""
  mana_max_depletion_mod = "mana_reserves_mod: " + numstr(details[ability_phase_details_key["mana_max_depletion_mod"]]) +" " if details[ability_phase_details_key["mana_max_depletion_mod"]] != "0.0" else ""
  aura_range_mod = "inspiration_range_mod: " + numstr(details[ability_phase_details_key["inspiration_aura_range_mod"]]) +" " if details[ability_phase_details_key["inspiration_aura_range_mod"]] != "0.0" else ""
  ability_recharge_change = "reduce_current_cooldowns: " + numstr(details[ability_phase_details_key["ability_recharge_change"]]) +" " if details[ability_phase_details_key["ability_recharge_change"]] != "0.0" else ""
  result += indentstr(indent) + title + "[[col:" + col + "]] " + duration +  replenish_ammo +  unbreakable + mana_regen_mod + mana_max_depletion_mod + cantmove + freeze_fatigue + fatigue_change_ratio + aura_range_mod  + ability_recharge_change + recharge_time + "[[/col]]\\\\n"
  # affects_allies + affects_enemies +
  if int(details[ability_phase_details_key["heal_amount"]]) != 0:
    resurect = "(or resurrect if full hp) " if details[ability_phase_details_key["resurrect"]] == "true" else ""
    result += indentstr(indent+ 2) + "heal each entity " + resurect + "by " + statstr(details[ability_phase_details_key["heal_amount"]]) + " every " + statstr(details[ability_phase_details_key["hp_change_frequency"]] + "s") + endl

  if int(details[ability_phase_details_key["damage_amount"]]) != 0:
    up_to = "up to " + statstr(details[ability_phase_details_key["max_damaged_entities"]])+ " " if int(details[ability_phase_details_key["max_damaged_entities"]]) >= 0  else ""
    chance = "chance (" + statstr(float(details[ability_phase_details_key["damage_chance"]]) * 100)  + "%) to " if float(details[ability_phase_details_key["damage_chance"]]) != 1.0 else ""
    result += indentstr(indent+ 2) + chance + "damage " + up_to + "entities, each by: " + ability_damage_stat(details[ability_phase_details_key["damage_amount"]], details[ability_phase_details_key["imbue_ignition"]], details[ability_phase_details_key["imbue_magical"]]) + " every " + statstr(details[ability_phase_details_key["hp_change_frequency"]] + "s") + endl

  if phaseid in ability_phase_stats:
    result += indentstr(indent+ 2) +"stats:\\\\n"
    effects = ability_phase_stats[phaseid]
    
    for effect in effects:
      how = "*" if effect[ability_phase_stats_keys["how"]] == 'mult' else '+'
      if how == '+' and float(effect[ability_phase_stats_keys["value"]]) < 0:
        how = ""
      result += indentstr(indent+ 2) + effect[ability_phase_stats_keys["stat"]] + " " + how + statstr(round(float(effect[ability_phase_stats_keys["value"]]), 2)) + "\\\\n"
  if phaseid in ability_phase_attrs:
    attrs = ability_phase_attrs[phaseid]
    result += indentstr(indent+ 2) + "attributes: "
    for attr in attrs:
      result += statstr(attr[ability_phase_attrs_keys["attribute"]]) + " "
    result += "\\\\n"
  if details[ability_phase_details_key["imbue_contact"]] != "":
    result += ability_phase_details_stats(details[ability_phase_details_key["imbue_contact"]], indent+2, "imbue_contact")
  return result

# projectiles_explosions_tables_projectiles_explosions
tsv_file = opendbread("projectiles_explosions_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
projectiles_explosions = {}

rowid = 0
projectiles_explosions_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        projectiles_explosions_keys[key] = i
        i = i + 1
  if rowid > 2:
      projectiles_explosions[row[projectiles_explosions_keys["key"]]] = row
tsv_file.close()

# projectiles_shrapnels
tsv_file = opendbread("projectile_shrapnels_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
shrapnels = {}

rowid = 0
shrapnels_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        shrapnels_keys[key] = i
        i = i + 1
  if rowid > 2:
      shrapnels[row[shrapnels_keys["key"]]] = row
tsv_file.close()

# unit_missile_weapon_junctions
tsv_file = opendbread("unit_missile_weapon_junctions_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
missile_weapon_junctions = {}
missile_weapon_for_junction = {}

rowid = 0
missile_weapon_junctions_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        missile_weapon_junctions_keys[key] = i
        i = i + 1
  if rowid > 2:
    key = row[missile_weapon_junctions_keys["unit"]]
    if key not in missile_weapon_junctions:
        missile_weapon_junctions[key] = []
    missile_weapon_junctions[key].append(row)

    key = row[missile_weapon_junctions_keys["id"]]
    missile_weapon_for_junction[key] = row
tsv_file.close()

# effect_bonus_missile_junction
tsv_file = opendbread("effect_bonus_value_missile_weapon_junctions_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
effect_bonus_missile_junctions = {}

rowid = 0
effect_bonus_missile_junctions_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        effect_bonus_missile_junctions_keys[key] = i
        i = i + 1
  if rowid > 2:
    key = row[effect_bonus_missile_junctions_keys["effect"]]
    if key not in effect_bonus_missile_junctions:
        effect_bonus_missile_junctions[key] = []
    effect_bonus_missile_junctions[key].append(row)
tsv_file.close()

# ground_type_to_stat_effects_tables
tsv_file = opendbread("ground_type_to_stat_effects_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
ground_type_stats = {}

rowid = 0
ground_type_stats_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        ground_type_stats_keys[key] = i
        i = i + 1
  if rowid > 2:
    key = row[ground_type_stats_keys["affected_group"]]
    if key not in ground_type_stats:
        ground_type_stats[key] = {}
    ground = row[ground_type_stats_keys["ground_type"]]
    if ground not in ground_type_stats[key]:
      ground_type_stats[key][ground] = []
    ground_type_stats[key][ground].append(row)
tsv_file.close()

# weapon_to_projectile
tsv_file = opendbread("missile_weapons_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
weapon_projectile = {}
weapon_secondary_ammo = {}

rowid = 0
weapon_projectile_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        weapon_projectile_keys[key] = i
        i = i + 1
  if rowid > 2:
      weapon_projectile[row[weapon_projectile_keys["key"]]] = row[weapon_projectile_keys["default_projectile"]]
      weapon_secondary_ammo[row[weapon_projectile_keys["key"]]] = row[weapon_projectile_keys["use_secondary_ammo_pool"]]
tsv_file.close()

# weapon additional projectiles
tsv_file = opendbread("missile_weapons_to_projectiles_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
weapon_alt_projectile = {}

rowid = 0
weapon_alt_projectile_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        weapon_alt_projectile_keys[key] = i
        i = i + 1
  if rowid > 2:
      key = row[weapon_alt_projectile_keys["missile_weapon"]]
      if key not in weapon_alt_projectile:
        weapon_alt_projectile[key] = []
      weapon_alt_projectile[key].append(row[weapon_alt_projectile_keys["projectile"]])
tsv_file.close()

# engine_to_weapon
tsv_file = opendbread("battlefield_engines_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
engine_weapon = {}
engine_entity = {}
engine_mounted = {}

rowid = 0
engine_weapon_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        engine_weapon_keys[key] = i
        i = i + 1
  if rowid > 2:
      engine_weapon[row[engine_weapon_keys["key"]]] = row[engine_weapon_keys["missile_weapon"]]
      engine_entity[row[engine_weapon_keys["key"]]] = row[engine_weapon_keys["battle_entity"]]
      engine_mounted[row[engine_weapon_keys["key"]]] = "No_Crew" in row[engine_weapon_keys["engine_type"]]
tsv_file.close()

# articulated_entity
tsv_file = opendbread("land_unit_articulated_vehicles_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
articulated_entity = {}

rowid = 0
articulated_entity_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        articulated_entity_keys[key] = i
        i = i + 1
  if rowid > 2:
      articulated_entity[row[articulated_entity_keys["key"]]] = row[articulated_entity_keys["articulated_entity"]]
tsv_file.close()

# mount_to_entity
tsv_file = opendbread("mounts_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
mount_entity = {}

rowid = 0
mount_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        mount_keys[key] = i
        i = i + 1
  if rowid > 2:
      mount_entity[row[mount_keys["key"]]] = row[mount_keys["entity"]]
tsv_file.close()

def posstr(stat, indent = 0):
  return indentstr(indent) + "[[col:green]]" + numstr(stat) +"[[/col]]"

def negstr(stat, indent = 0):
  return indentstr(indent) + "[[col:red]]" + numstr(stat) +"[[/col]]"

def indentstr(indent):
  return ("[[col:red]] [[/col]]" * indent)

def modstr(s):
  stat = float(s)
  if stat > 0:
    return posstr(s)
  if stat < 0:
    return negstr(s)
  return statstr(s)

def negmodstr(s):
  stat = float(s)
  if stat < 0:
    return posstr(s)
  if stat > 0:
    return negstr(s)
  return statstr(s)

def difftostr(stat):
  if stat > 0:
    return posstr(stat)
  if stat < 0:
    return negstr(stat)
  return ""

def negdifftostr(stat):
  if stat > 0:
    return negstr(stat)
  if stat < 0:
    return posstr(stat)
  return ""

def try_int(val):
  try:
    return int(val, 10)
  except ValueError:
    return val

def try_float(val):
  try:
    return float(val)
  except ValueError:
    return val

def numstr(stat):
  fstat = try_float(stat)
  if type(fstat) != float:
    return str(stat)
  ifstat = round(fstat, 0)
  if ifstat == fstat:
    return str(int(ifstat))
  return str(round(fstat, 2))

def colstr(s, col):
  return "[[col:"+ col + "]]" + s +"[[/col]]"

def statstr(stat):
  return "[[col:yellow]]" + numstr(stat) +"[[/col]]"

def derivedstatstr(stat):
  return "[[col:cooking_ingredients_group_3]]" + numstr(stat) +"[[/col]]"

def statindent(name, value, indent):
  return indentstr(indent) + name + " " "[[col:yellow]]" + numstr(value) +"[[/col]]" + endl

# bullet point enum
tsv_file = opendbread("ui_unit_bullet_point_enums_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_bullet_point_enums = []
new_bullet_point_enums_keys = {}
new_bullet_point_enums_proto = None
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      new_bullet_point_enums_keys[key] = i
      i = i + 1
  #if rowid <= 2:
  new_bullet_point_enums.append(row)
  new_bullet_point_enums_proto = row.copy()

# bullet point override
tsv_file = opendbread("ui_unit_bullet_point_unit_overrides_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_bullet_point_override = []
new_bullet_point_override_keys = {}
new_bullet_point_prototype = None
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      new_bullet_point_override_keys[key] = i
      i = i + 1
  #if rowid <= 2:
  new_bullet_point_override.append(row)
  new_bullet_point_override_prototype = row.copy()

# bullet point descriptions
tsv_file = openlocread("ui_unit_bullet_point_enums")
read_tsv = csv.reader(tsv_file, delimiter="\t")
bullet_points_loc_keys = {}
rowid = 0
new_bullet_points_loc = []
new_bullet_point_loc_prototype = None
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        bullet_points_loc_keys[key] = i
        i = i + 1
  #if rowid <= 2:
  new_bullet_points_loc.append(row)
  new_bullet_point_loc_prototype = row.copy()

# unit names
tsv_file = openlocread("land_units")
read_tsv = csv.reader(tsv_file, delimiter="\t")
unit_names_keys = {}
unit_name = {}
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        unit_names_keys[key] = i
        i = i + 1
  if rowid > 2:
    key = row[unit_names_keys["key"]]
    if "land_units_onscreen_name_" in key:
      key = key.replace("land_units_onscreen_name_", "", 1)
      unit_name[key] = row[unit_names_keys["text"]]


# unit table
tsv_file = opendbread("land_units_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
units = {}

rowid = 0
units_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        units_keys[key] = i
        i = i + 1
  if rowid > 2:
      units[row[units_keys["key"]]] = row
tsv_file.close()

# battle entities
tsv_file = opendbread("battle_entities_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
battle_entities = {}

rowid = 0
battle_entities_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        battle_entities_keys[key] = i
        i = i + 1
  if rowid > 2:
      battle_entities[row[battle_entities_keys["key"]]] = row
tsv_file.close()

# battle entity stats (only used by battle personalities and officers)
tsv_file = opendbread("battle_entity_stats_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
bentity_stats = {}

rowid = 0
bentity_stats_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        bentity_stats_keys[key] = i
        i = i + 1
  if rowid > 2:
      bentity_stats[row[bentity_stats_keys["key"]]] = row
tsv_file.close()

# land_units_officers_tables
tsv_file = opendbread("land_units_officers_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
officers = {}

rowid = 0
officers_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        officers_keys[key] = i
        i = i + 1
  if rowid > 2:
      officers[row[officers_keys["key"]]] = row
tsv_file.close()

# battle_personalities_tables
tsv_file = opendbread("battle_personalities_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
personalities = {}

rowid = 0
personalities_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        personalities_keys[key] = i
        i = i + 1
  if rowid > 2:
      personalities[row[personalities_keys["key"]]] = row

tsv_file.close()

# land_units_additional_personalities_groups_junctions_tables
tsv_file = opendbread("land_units_additional_personalities_groups_junctions_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
personality_group = {}

rowid = 0
personality_group_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        personality_group_keys[key] = i
        i = i + 1
  if rowid > 2:
      key = row[personality_group_keys["group"]]
      if key not in personality_group:
        personality_group[key] = []
      personality_group[key].append(row[personality_group_keys["battle_personality"]])

tsv_file.close()

# tags:
# [[img:path]] image
# {{tr:}} - locale? (translation)
# [[col]]
def damage_stat(base, ap, ignition, magic, title="dmg"):
  typestr = ""
  if magic == "true":
    typestr+="[[img:ui/skins/default/modifier_icon_magical.png]][[/img]]"
  if float(ignition) != 0:
    typestr+="[[img:ui/skins/default/modifier_icon_flaming.png]][[/img]]"
  apppct = ""
  if float(base) != 0:
    apppct = "("  + statstr(numstr(round(float(ap) * 100 / (float(base) + float(ap)), 2)) + "%") + ")" 
  return title + ": " + statstr(base) + "+ap:" + statstr(ap) + apppct + typestr

def ability_damage_stat(base, ignition, magic, title="dmg"):
  typestr = ""
  if magic == "true":
    typestr+="[[img:ui/skins/default/modifier_icon_magical.png]][[/img]]"
  if float(ignition) != 0:
    typestr+="[[img:ui/skins/default/modifier_icon_flaming.png]][[/img]]"
  return title + ": " + statstr(base) + typestr

def icon(name):
  return "[[img:ui/skins/default/" + name + ".png]][[/img]]"

stat_icon = {"armour": icon("icon_stat_armour"), "melee_damage_ap": "melee_ap ", "fatigue": icon("fatigue"), "accuracy": "accuracy", "morale": icon("icon_stat_morale"), "melee_attack": icon("icon_stat_morale"), "charging": icon("icon_stat_charge_bonus"), "charge_bonus": icon("icon_stat_charge_bonus"), "range": icon("icon_stat_range"), "speed": icon("icon_stat_speed"), "reloading": icon("icon_stat_reload_time"), "melee_attack": icon("icon_stat_attack"), "melee_defence": icon("icon_stat_defence")}

def rank_icon(rank):
  if int(rank) == 0:
    return "[]"
  return icon("experience_" + str(rank))

def explosion_stats(explosionrow, indent = 0): 
  projectiletext = ""
  
  # detonation_duration, detonation_speed, 
  # contact_phase_effect -> special_ability_phases
  # fuse_distance_from_target - This will activate the explosion n metres from target. If n is greater than distance to target, then the explosion will occur instantly when the projectile is activated. To get beyond this, add a min_range to the projectile.
  # damage/ap is per entity hit
  # detonation_force - This is how much force is applied to determine the result of being hit, for knockbacks etc.
  # fuse_fixed_time - Fixed fuse time in s. -1 means not fixed. Use EITHER fixed fuse time or distance from target
  # affects allies - yes/no
  # shrapnel: launches another projectile (projectile_shrapnels, amount is num of projectiles )
  projectiletext += indentstr(indent) + damage_stat(explosionrow[projectiles_explosions_keys['detonation_damage']], explosionrow[projectiles_explosions_keys['detonation_damage_ap']], explosionrow[projectiles_explosions_keys['ignition_amount']], explosionrow[projectiles_explosions_keys['is_magical']], "per_entity_dmg") + endl
  projectiletext += statindent("radius", explosionrow[projectiles_explosions_keys['detonation_radius']], indent)
  if explosionrow[projectiles_explosions_keys['affects_allies']] == "false":
    projectiletext += posstr("doesn't_affect_allies", indent) + endl
  if explosionrow[projectiles_explosions_keys['shrapnel']]:
    shrapnelrow = shrapnels[explosionrow[projectiles_explosions_keys['shrapnel']]]
    projectiletext += statindent("explosion_shrapnel:", "", indent)
    if shrapnelrow[shrapnels_keys['launch_type']] == "sector":
      projectiletext += statindent("angle", shrapnelrow[shrapnels_keys['sector_angle']], 2+ indent)
    projectiletext += statindent("amount", shrapnelrow[shrapnels_keys['amount']], 2 + indent)
    projectiletext += missile_stats(projectiles[shrapnelrow[shrapnels_keys['projectile']]], None, "", 2 + indent, False)
  if explosionrow[projectiles_explosions_keys['contact_phase_effect']]:
    projectiletext += ability_phase_details_stats(explosionrow[projectiles_explosions_keys['contact_phase_effect']],  2 + indent, "contact effect")
  return projectiletext


def missile_stats(projectilerow, unit, projectilename, indent, traj = True):
  projectiletext = ""
  #projectile:
  # fired_by_mount - If this flag is on (and the firing entity is a macro entity) the mount will fire, rather than the rider
  # prefer_central_targets - Prefer entities nearer the centre of the target (rather than closest in firing arc)
  # scaling_damage - If damage calculation has to be scaled based on different rules
  # shots_per_volley - Usually units shoot 1 shot per volley, but some animations chave multiple fire points, such as multi-shot artillery units. Most of the logic isn't aware of this, so this field is for reference for those systems
  # can_roll - Can the projectile roll on the ground
  # can_bounce - can bounce between targets?
  # expire_on_impact - If true, the projectile will expire on impact, and will not stick into, or deflect off the object it hit
  # is_beam_launch_burst - Launch beams will attempt to make the vfx match the projectiles travel, and apply a clipping plane when a projectile hits something, culling the projectiles in front
  # expiry_range - If this value is positive it dictactes the maximum distance a projectile can travel before it expires
  # projectile_penetration - what entity sizes can projectile pass through and how much can penetrate before it stops
  # can_target_airborne
  # is_magical
  # ignition_amount How much do we contribute to setting things on fire. Also, if this value is greater than 0, this is considered a flaming attack
  # gravity - Use this value to make projectiles be more / less affected by gravity. This is mainly used as a representation of wind resistance, so that projectiels can hang in the air. Negative means to use 'normal' gravity. 
  # mass - Mass of the projectile.
  # burst_size - Number of shots in a single burst (value of 1 means no burst mode)
  # burst_shot_delay - Determines the delay between each shot of the same burst
  # can_damage_buildings
  # can_damage_vehicles
  # shockwave_radius
  # muzzle_velocity - This describes the speed the projectile launches at (metres per second). If it is negative, the code will calculate this value based on firing at 45 degrees, hitting at the effective range. Not used when trajectory is fixed!
  # max_elevation - This is the maximum angle that the projectile can be fired at. Generally you want it high (max 90 degrees), and above 45. Except for special cases (e.g. cannon). Not used when trajectory is fixed!
  # fixed elevation - elevation of fixed trajectory
  # projectile_number: ? free projectiles not consuming ammo?
  # spread: ?
  # collision_radius: ?
  # homing_params: steering params for the projectile, increases chance to hit?
  # overhead_stat_effect -> special_ability_phase
  # contact_stat_effect -> special_ability_phase
  # high_air_resistance
  # minimum_range
  # trajectory_sight, max_elevation
  # category: misc ignores shields
  # calibration area, distance (the area in square meter a projectile aims, and the area guaranteed to hit at the calibration_distance range)

  building = " "
  if projectilerow[projectiles_keys['can_damage_buildings']] == "true":
    building += "@buildings "
  if projectilerow[projectiles_keys['can_damage_vehicles']] == "true":
    building += "@vehicles "
  if projectilerow[projectiles_keys['can_target_airborne']] == "true":
    building += "@airborne "
  projectiletext += indentstr(indent) + damage_stat(projectilerow[projectiles_keys['damage']], projectilerow[projectiles_keys['ap_damage']], projectilerow[projectiles_keys['ignition_amount']], projectilerow[projectiles_keys['is_magical']]) + building + endl

  # calibration: distance, area, spread
  volley = ""
  if projectilerow[projectiles_keys['shots_per_volley']] != "1":
    volley += "shots_per_volley " + statstr(projectilerow[projectiles_keys['shots_per_volley']])
  if projectilerow[projectiles_keys['burst_size']] != "1":
    volley += "shots_per_volley " + statstr(projectilerow[projectiles_keys['burst_size']]) + " interval " +  statstr(projectilerow[projectiles_keys['burst_shot_delay']])
  if projectilerow[projectiles_keys['projectile_number']] != "1":
    volley += "projectiles_per_shot " + statstr(projectilerow[projectiles_keys['projectile_number']])
  
  central_targets = statstr("closest_target")
  if projectilerow[projectiles_keys['prefer_central_targets']] == "false":
    central_targets = statstr("central_target")

  projectiletext += indentstr(indent) + "calibration: " + "area " + statstr(projectilerow[projectiles_keys['calibration_area']]) + " distance " + statstr(projectilerow[projectiles_keys['calibration_distance']]) + " prefers " + central_targets + endl

  if volley != "":
    projectiletext += indentstr(indent) + volley + endl
  if unit is not None:
    projectiletext += statindent("accuracy", float(projectilerow[projectiles_keys['marksmanship_bonus']]) + float(unit[units_keys['accuracy']]), indent)
    reloadtime = float(projectilerow[projectiles_keys['base_reload_time']]) * ((100 - float(unit[units_keys['accuracy']])) * 0.01)
    projectiletext += indentstr(indent) + "reload: " + "skill " + statstr(unit[units_keys['reload']]) + " time " + statstr(reloadtime)+ "s (base" + statstr(projectilerow[projectiles_keys['base_reload_time']]) + "s)" + endl

  category = projectilerow[projectiles_keys['category']]
  if category == "misc" or category == "artillery":
    category += "(ignores shields)"
  projectiletext += indentstr(indent) + "category: "+ statstr(category) + " spin " + statstr( projectilerow[projectiles_keys['spin_type']].replace("_spin", "", 1))  + endl
  if projectilerow[projectiles_keys['minimum_range']] != "0.0":
    projectiletext += statindent("min_range", projectilerow[projectiles_keys['minimum_range']], indent)

  homing = ""
  impact = ""
  if projectilerow[projectiles_keys['can_bounce']] == "true":
    impact += "bounce "
  if projectilerow[projectiles_keys['can_roll']] == "true":
    impact += "roll "
  if projectilerow[projectiles_keys['shockwave_radius']] != "-1.0":
    impact += "shockwave_radius " + projectilerow[projectiles_keys['shockwave_radius']]

  if traj == True:
    # sight - celownik
    # fixed - attached to the weapon
    # fixed trajectory != fixed sight?
    # some guide: dual_low_fixed means can use both low and fixed

    # traj examples
    # - plagueclaw sight: low max elev: 60, fixed elev 45 vel 67, grav -1, mass 50
    # - warp lightning: sight low, max elev 50, fixed elev 45 vel 110, spin: none mass: 300 grav 6
    # - poison wind mortar globe: type artillery spin axe, sight fixed, max elev 56, vel 90 grav -1, mass 25, fixed elev 50
    # - ratling gun: type musket spin none, max elev 88, vel 120, grav -1, mass 5 fix elev 45
    trajectory = "trajectory:"
    trajectory += statstr( projectilerow[projectiles_keys['trajectory_sight']])
    trajectory += " vel " + statstr( projectilerow[projectiles_keys['muzzle_velocity']])
    trajectory += " max_angle " + statstr( projectilerow[projectiles_keys['max_elevation']])
    trajectory += " fixed_angle " + statstr( projectilerow[projectiles_keys['fixed_elevation']])
    trajectory += " mass " + statstr( projectilerow[projectiles_keys['mass']]) # affects air resistance and shockwave force, doesn't affect speed/acceleration
    if float(projectilerow[projectiles_keys['gravity']]) != -1:
      trajectory += " g " + statstr( projectilerow[projectiles_keys['gravity']]) # default is 10?, affects fall/rise rate of projectile, maybe air resistance?
    projectiletext += indentstr(indent) + trajectory + endl

  if impact != "":
    projectiletext += statindent("impact", impact, indent)
  if projectilerow[projectiles_keys['spread']] != "0.0":
    projectiletext += statindent("spread", projectilerow[projectiles_keys['spread']], indent)
  if projectilerow[projectiles_keys['homing_params']] != "":
    projectiletext += statindent("homing", "true", indent)
  if projectilerow[projectiles_keys['bonus_v_infantry']] != '0':
    projectiletext += statindent("bonus vs nonlarge" ,projectilerow[projectiles_keys['bonus_v_infantry']], indent)
  if projectilerow[projectiles_keys['bonus_v_large']] != '0':
    projectiletext += statindent("bonus_vs_large ", projectilerow[projectiles_keys['bonus_v_large']], indent)
  #todo: projectile_homing details
  # projectile_scaling_damages - scales damage with somebody's health
  if projectilerow[projectiles_keys['explosion_type']] != '':
    explosionrow = projectiles_explosions[projectilerow[projectiles_keys['explosion_type']]]
    projectiletext += statindent("explosion:", "", indent)
    projectiletext += explosion_stats(explosionrow, indent+2)
  return projectiletext

def meleeweapon_stats(meleeid, indent = 0):
  unit_desc = ""
  meleerow = melee[meleeid]
  # scaling_damage If damage calculation has to be scaled based on different rules
  # col max targets: Maximum targets damaged by collision attack. This cap is refreshed by collision_attack_max_targets_cooldown.
  # col max targets cooldown: Each second, this amount of targets will be removed from the max targets list, enabling the collision attacker to deal more attacks.
  # weapon_length: Relevant for pikes, cav refusal distances and close proximity. The latter picks between this and 1m + entity radius, whatever is longer, to determine weapon "reach". Chariot riders use this to check if enemies are within reach.
  # max splash targets Maximum entities to attack per splash attack animation. Note that High Priority targets (main units table) allways get treated focussed damage.
  # splash dmg multiplier: Multiplier to knock power in splash attack metadata
  # wallbreaker attribute says if can damage walls in melee
  # todo: show dmg of a full rank of units?
  building = ""
  if int(meleerow[melee_keys['building_damage']]) > 0:
    building = " (building: "+ statstr(meleerow[melee_keys['building_damage']])+ ")" # what about kv_rules["melee_weapon_building_damage_mult"]?
  unit_desc += indentstr(indent) + damage_stat(meleerow[melee_keys['damage']], meleerow[melee_keys['ap_damage']], meleerow[melee_keys['ignition_amount']], meleerow[melee_keys['is_magical']], "melee_dmg") + building + endl
  unit_desc += statindent("melee_reach", meleerow[melee_keys['weapon_length']], indent)
  total_dmg = int(meleerow[melee_keys['damage']]) + int(meleerow[melee_keys['ap_damage']])
  dp10s = (float(total_dmg) * 10) / float(meleerow[melee_keys['melee_attack_interval']])
  unit_desc += indentstr(indent) + "melee_interval " + statstr(meleerow[melee_keys['melee_attack_interval']]) + " dp10s " + derivedstatstr(round(dp10s, 0)) + endl
  if meleerow[melee_keys['bonus_v_infantry']] != "0":
    unit_desc += statindent("bonus_v_nonlarge", meleerow[melee_keys['bonus_v_infantry']], indent)
  # never set:stats["bonus_v_cav"] = meleerow[melee_keys['bonus_v_cavalry']]
  if meleerow[melee_keys['bonus_v_large']] != "0":
    unit_desc += statindent("bonus_v_large", meleerow[melee_keys['bonus_v_large']], indent)
  if meleerow[melee_keys['splash_attack_target_size']] != "":
    unit_desc += statindent("splash dmg:", "", indent)
    # confirmed by ca: blank means no splash damage
    unit_desc += statindent("target_size","<=" + meleerow[melee_keys['splash_attack_target_size']], indent + 2)
    unit_desc += indentstr(indent + 2) + "max_targets " + statstr(meleerow[melee_keys['splash_attack_max_attacks']]) + " dmg_each " + derivedstatstr(round(total_dmg / float(meleerow[melee_keys['splash_attack_max_attacks']]), 0))  + endl
    if float(meleerow[melee_keys['splash_attack_power_multiplier']]) != 1.0: 
      unit_desc += statindent("knockback mult", round(float(meleerow[melee_keys['splash_attack_power_multiplier']]), 1), indent + 2)
  if meleerow[melee_keys['collision_attack_max_targets']] != "0":
    unit_desc  += indentstr(indent) + " collision: max targets " + statstr(meleerow[melee_keys['collision_attack_max_targets']]) + " recharge_per_sec " + statstr(meleerow[melee_keys['collision_attack_max_targets_cooldown']]) + endl
  return unit_desc


def missileweapon_stats(missileweapon, unit, indent = 0, title = "ranged"):
  projectiletext = ""
  projectileid = weapon_projectile[missileweapon]
  name = ""
  if weapon_secondary_ammo[missileweapon] == "true":
    name = "(secondary ammo)"
  projectiletext += indentstr(indent) + title + name + ":" + endl
  projectilerow = projectiles[projectileid]
  projectiletext += missile_stats(projectilerow, unit, name, indent + 2)
  if missileweapon in weapon_alt_projectile:
    for altprojectileid in weapon_alt_projectile[missileweapon]:
      altprojectilerow = projectiles[altprojectileid]
      name = altprojectilerow[projectiles_keys['shot_type']].split("_")[-1]
      if name == 'default':
        name = altprojectileid
      if weapon_secondary_ammo[missileweapon] == "true":
        name += "(secondary ammo)"
      projectiletext += indentstr(indent) + title +" (" + name + "):" + endl
      projectiletext += missile_stats(altprojectilerow, unit, name, indent + 2)
  return projectiletext

endl = "\\\\n"

# unit ability doesn't have anything intesting
# unit_special_ability uses unit_ability as key according to dave
# num_uses - charges?
# active time - If this is a projectile then set -1 for active time
# activated projectiles - projectiles table
# target_friends/enemies/ground
# assume_specific_behaviour - special_abilities_behaviour_types (cantabrian circle, etc.)
# bombardment - projectile_bombardments table
# spawned unit - land_units_table
# vortex: battle_vortexs vortex_key
# wind_up_stance, wind_down_stance -> special_ability_stance_enums
# use_loop_stance - Entities will play a loop locomotion stance
# mana_cost
# min_range - "too close" error?
# initial_recharge, recharge_time, wind_up_time
# passive
# effect_range
# affect_self
# num_effected_friendly_units
# num_effected_enemy_unuits
# update_targets_every_frame
# clear_current_order
# targetting_aoe -> area_of_effect_displays - This is the area of effect to display when targetting
# passive_aoe -> area_of_effect_displays - This is the area of effect to display when ability has been ordered but not yet cast (like if unit has to move their to cast)
# active_aoe -> area_of_effect_displays - This is the area of effect to display when ability is currently active (has been cast)
# miscast chance - The unary chance of a miscast occuring
# miscast_explosion -> projectiles_explosions
# target_ground_under_allies
# target_ground_under_enemies
# target_self
# target_intercept_range - ?
# only_affect_owned_units - If it's affecting friendly units, it only affect those in the same army as the owner
# spawn_is_decoy - If spawning a unit the new one will be understood as a decoy of the owner one, the UI will show data for the owning one
# spawn_is_transformation - If spawning a unit will mean the owner unit will be replaced by the spawned one
tsv_file = opendbread("unit_special_abilities_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
ability_details = {}

rowid = 0
ability_details_key = {}
new_ability_details = []
ability_details_maxid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        ability_details_key[key] = i
        i = i + 1
  if rowid > 2:
      ability_details[row[ability_details_key["key"]]] = row
      newid = int(row[ability_details_key["unique_id"]])
      if newid > ability_details_maxid:
        ability_details_maxid = newid
  new_ability_details.append(row)
tsv_file.close()

# unit_abilities_tables
tsv_file = opendbread("unit_abilities_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_unit_ability = [] 
new_unit_ability_keys = {}
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      new_unit_ability_keys[key] = i
      i = i + 1
  new_unit_ability.append(row)

# unit_sets_tables
tsv_file = opendbread("unit_sets_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_unit_set = [] 
new_unit_set_for_key = {}
new_unit_set_keys = {}
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      new_unit_set_keys[key] = i
      i = i + 1
  if rowid > 2:
      new_unit_set_for_key[row[new_unit_set_keys["key"]]] = row
  new_unit_set.append(row)

# unit_sets_tables
tsv_file = opendbread("unit_sets_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_unit_set = [] 
new_unit_set_keys = {}
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      new_unit_set_keys[key] = i
      i = i + 1
  new_unit_set.append(row)

# unit_set_to_unit_junctions_tables
tsv_file = opendbread("unit_set_to_unit_junctions_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_unit_set_to_unit = [] 
new_unit_set_to_unit_keys = {}
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      new_unit_set_to_unit_keys[key] = i
      i = i + 1
  new_unit_set_to_unit.append(row)

# unit_set_unit_ability_junctions_tables
tsv_file = opendbread("unit_set_unit_ability_junctions_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_unit_set_ability = [] 
new_unit_set_ability_keys = {}
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      new_unit_set_ability_keys[key] = i
      i = i + 1
  new_unit_set_ability.append(row)

# effect_bonus_value_unit_set_unit_ability_junctions_tables
tsv_file = opendbread("effect_bonus_value_unit_set_unit_ability_junctions_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_effect_bonus_ability = [] 
new_effect_bonus_ability_keys = {}
new_effect_bonus_ability_proto = None
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      new_effect_bonus_ability_keys[key] = i
      i = i + 1
  new_effect_bonus_ability.append(row)
  new_effect_bonus_ability_proto = row.copy()

# unit_abilities locales
tsv_file = openlocread("unit_abilities")
read_tsv = csv.reader(tsv_file, delimiter="\t")
new_ability_loc = []
new_ability_loc_proto = None
additional_ability_loc = []
ability_descriptions_keys = {}
rowid = 0
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
    for key in row:
      ability_descriptions_keys[key] = i
      i = i + 1
  new_ability_loc.append(row)
  new_ability_loc_proto = row.copy()

# missile_weapon_junctions and effect_bonus_value_missile_weapon_junctions_tables - alternative projectile weapons unlocked in campaign
#  - here we add a dummy ability which shows up when the custom weapon effect is enabled in campaign
#  - example: "the very latest thing" skill of ikit claw
#  - there's units with alternatives (or multiple) upgrades (grom's cooking gives different weapon types to goblins)
# unit_special_abilities_tables - add a dummy infinite ability with no effects, will not show up in ui without this
# unit_abilities_tables - add a passive ability for every weapon effect
# unit_abilities__.loc -  add both name and tooltip entry for every added ability
# effect_bonus_value_unit_ability_junctions_tables - copy every entry from effect_bonus_value_missile_weapon_junctions_tables, replace missile weapon id with new ability key
# todo: use a different table for this (I assume unit_sets_tables + unit_set_to_unit_junctions_tables + unit_set_unit_ability_junctions_tables + effect_bonus_value_unit_set_unit_ability_junctions_tables)

ability_proto_map = {"key": "ikit_claw_missile_tooltip", "requires_effect_enabling": "true", "icon_name": "ranged_weapon_stat", "type": "wh_type_augment", "uniqueness": "wh_main_anc_group_common", "is_unit_upgrade": "false", "is_hidden_in_ui": "false", "source_type": "unit", "is_hidden_in_ui_for_enemy":"false"}
ability_details_proto_map = {"key": "ikit_claw_missile_tooltip", "num_uses": "-1", "active_time": "-1", "recharge_time": "-1", "initial_recharge": "-1", "wind_up_time": "0",
 "passive": "true", "effect_range": "0", "affect_self": "false", "num_effected_friendly_units": "0", "num_effected_enemy_units": "0", "update_targets_every_frame": "0", 
 "target_friends": "false", "target_enemies": "false", "target_ground": "false", "target_intercept_range": "0", "clear_current_order": "false", "unique_id": "17224802351", "mana_cost": "0",
 "min_range": "0", "miscast_chance": "0", "voiceover_state": "vo_battle_special_ability_generic_response", "additional_melee_cp": "0", "additional_missile_cp": "0",
 "target_ground_under_allies": "false", "target_ground_under_enemies": "false", "miscast_global_bonus": "false", "target_self": "true", "spawn_is_transformation": "false", "use_loop_stance": "false",
 "spawn_is_decoy": "false", "only_affect_owned_units": "false" }

for effectid in effect_bonus_missile_junctions:
  effectrows = effect_bonus_missile_junctions[effectid]
  for effectrow in effectrows:
    abilityid = effectid + "_" + effectrow[effect_bonus_missile_junctions_keys["missile_weapon_junction"]] + "_stats"
    weaponjunction = missile_weapon_for_junction[effectrow[effect_bonus_missile_junctions_keys["missile_weapon_junction"]]]
    weaponid = weaponjunction[missile_weapon_junctions_keys["missile_weapon"]]
    abilitynamerow = new_ability_loc_proto.copy()
    abilitynamerow[ability_descriptions_keys["key"]] = "unit_abilities_onscreen_name_" + abilityid
    
    abilitynamerow[ability_descriptions_keys["text"]] = weaponid.split("_", 2)[2]
    additional_ability_loc.append(abilitynamerow)
    abilitytextrow = new_ability_loc_proto.copy()
    abilitytextrow[ability_descriptions_keys["key"]] = "unit_abilities_tooltip_text_" + abilityid
    abilitytextrow[ability_descriptions_keys["text"]] = missileweapon_stats(weaponid, None, 0)
    additional_ability_loc.append(abilitytextrow)
    abilityrow = list(new_unit_ability_keys.keys())
    for key in new_unit_ability_keys:
      if key in ability_proto_map:
        abilityrow[new_unit_ability_keys[key]] = ability_proto_map[key]
      else:
        abilityrow[new_unit_ability_keys[key]] = ""
    abilityrow[new_unit_ability_keys["key"]] = abilityid
    new_unit_ability.append(abilityrow)

    abilitydetailsrow = list(ability_details_key.keys())
    for key in ability_details_key:
      if key in ability_details_proto_map:
        abilitydetailsrow[ability_details_key[key]] = ability_details_proto_map[key]
      else:
        abilitydetailsrow[ability_details_key[key]] = ""
    abilitydetailsrow[ability_details_key["key"]] = abilityid
    ability_details_maxid = ability_details_maxid + 1
    abilitydetailsrow[ability_details_key["unique_id"]] = str(ability_details_maxid)
    new_ability_details.append(abilitydetailsrow)

    unitid = weaponjunction[missile_weapon_junctions_keys["unit"]]
    unitsetid = unitid
    if unitsetid not in new_unit_set_for_key:
      unitsetrow = list(new_unit_set_keys.keys())
      unitsetrow[new_unit_set_keys["key"]] = unitsetid
      unitsetrow[new_unit_set_keys["use_unit_exp_level_range"]] = "false"
      unitsetrow[new_unit_set_keys["min_unit_exp_level_inclusive"]] = "-1"
      unitsetrow[new_unit_set_keys["max_unit_exp_level_inclusive"]] = "-1"
      unitsetrow[new_unit_set_keys["special_category"]] = ""
      new_unit_set_for_key[unitsetid] = unitsetrow
      new_unit_set.append(unitsetrow)

      unitsettounitrow = list(new_unit_set_to_unit_keys.keys())
      unitsettounitrow[new_unit_set_to_unit_keys["unit_set"]] = unitsetid
      unitsettounitrow[new_unit_set_to_unit_keys["unit_record"]] = unitid
      unitsettounitrow[new_unit_set_to_unit_keys["unit_caste"]] = ""
      unitsettounitrow[new_unit_set_to_unit_keys["unit_category"]] = ""
      unitsettounitrow[new_unit_set_to_unit_keys["unit_class"]] = ""
      unitsettounitrow[new_unit_set_to_unit_keys["exclude"]] = "false"
      new_unit_set_to_unit.append(unitsettounitrow)

    unitsetabilityid = unitsetid + "_" + abilityid
    unitsetabilityrow = list(new_unit_set_ability_keys.keys())
    unitsetabilityrow[new_unit_set_ability_keys["key"]] = unitsetabilityid
    unitsetabilityrow[new_unit_set_ability_keys["unit_set"]] = unitsetid
    unitsetabilityrow[new_unit_set_ability_keys["unit_ability"]] = abilityid
    new_unit_set_ability.append(unitsetabilityrow)

    effectbonusabilityrow = new_effect_bonus_ability_proto.copy()
    effectbonusabilityrow[new_effect_bonus_ability_keys["effect"]] = effectid
    effectbonusabilityrow[new_effect_bonus_ability_keys["bonus_value_id"]] = effectrow[effect_bonus_missile_junctions_keys["bonus_value_id"]]
    effectbonusabilityrow[new_effect_bonus_ability_keys["unit_set_ability"]] = unitsetabilityid
    new_effect_bonus_ability.append(effectbonusabilityrow)

# new unit_abilities_tables entries
with open('unit_abilities_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_unit_ability:
      tsv_writer.writerow(row)

# new unit_special_abilities_tables entries
with open('unit_special_abilities_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_ability_details:
      tsv_writer.writerow(row)

# new unit_sets_tables entries
with open('unit_sets_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_unit_set:
      tsv_writer.writerow(row)

# new unit_set_to_unit_junctions_tables entries
with open('unit_set_to_unit_junctions_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_unit_set_to_unit:
      tsv_writer.writerow(row)

# new unit_set_unit_ability_junctions_tables entries
with open('unit_set_unit_ability_junctions_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_unit_set_ability:
      tsv_writer.writerow(row)

# new effect_bonus_value_unit_set_unit_ability_junctions_tables entries
with open('effect_bonus_value_unit_set_unit_ability_junctions_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_effect_bonus_ability:
      tsv_writer.writerow(row)

# main unit table
tsv_file = opendbread("main_units_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
main_units = {}
land_unit_to_spawn_info = {}

rowid = 0
main_units_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        main_units_keys[key] = i
        i = i + 1
  if rowid > 2:
      main_unit_entry = row
      # main_unit:
      # caste: Among other usages, caste allows the overriding of UI stat bar max values
      # is_high_threat: High threat units override the entity threshold checks of melee reactions. If they run into or attack a unit, the unit will instantly react, even if less than 25% of their entities are affected.
      # unit_scaling: Determines if the number of men / artillery pieces in this unit should be scaled with the gfx unit size setting (true) or not (false)
      # mount: mount on campaign map
      # tier: unit tier
      # melee_cp: Base Melee Combat Potential of this unit. Must be >= 0.0 or the game will crash on startup. This value is modified (increased) by other factors such as Rank and equipped Abilities / Items. Reduced by 20% for missile cav.
      # can_siege - If true, can attack the turn a settlement is besieged - do not need to wait to build siege equipment on the campaign map
      # is_monstrous - For voiceover : Is this unit regarded as monstrous?
      # vo_xx - voiceover
      # multiplayer_qb_cap - Multiplayer cap for quest battles, requested by Alisdair
      unit = units[main_unit_entry[main_units_keys["land_unit"]]]

      stats = {}
      indent = 0
      unit_desc = ""
      # looks like num of non-autonomous-rider officers needs to be subtracted to have accurate numbers (based on bloodwrack_shrine in dark elf roster, ikit_claw_doomwheel, etc)
      num_men = int(main_unit_entry[main_units_keys["num_men"]])

      if unit[units_keys['campaign_action_points']] != "2100":
        stats["campaign_range"] = unit[units_keys['campaign_action_points']]
      if unit[units_keys['hiding_scalar']] != "1.0":
        stats["hiding_scalar"] = unit[units_keys['hiding_scalar']]
      if unit[units_keys['shield']] != 'none':
        stats["missile_block"] = shields[unit[units_keys['shield']]] + "%"
      stats["capture_power"] = unit[units_keys['capture_power']] # also apparently dead vehicles have capture power?
      # land_unit
      # todo: spot dist tree/ spot dist scrub/ 
      # hiding scalar -This affects the range that the unit can be spotted at, less than 1 makes it longer, greater than 1 shorter. So 1.5 would increase the spotters range by +50%
      # sync locomotion - undead sync anim   
      # training level: deprecated
      # visibility_spotting_range_min/max
      # attribute group - lists attributes
      if main_unit_entry[main_units_keys["is_high_threat"]] == "true":
        unit_desc  += statstr("high_threat (focuses enemy attack and splash damage)") + endl

      entity = battle_entities[unit[units_keys['man_entity']]]
      # entity column doc
      # todo: figure out which entity are these stats taken from? mount/engine/man?
      # combat_reaction_radius: Radius at which entity will trigger combat with nearby enemy
      # fly_speed: Speed of the entity when in the air (as opposed to moving on the ground)
      # fly_charge_speed
      # fire_arc_close? - like the angle of the fire cone aiming cone for facing the target, can be seen by simple hover, not needed in stats?
      # projectile_intersection_radius_ratio: Ratio of the radius to use for projectile intersections (usually < 1)
      # projectile_penetration_resistance: Added to the projectile penetration counter. Higher number means this entity can stop projectiles more easily.
      # projectile_penetration_speed_change: Ratio of projectile speed retained when it penetrates this entity.
      # min_tracking_ratio: Minimum ratio of move speed that an entity can slow down for formed movement
      # can_dismember: can be dismembered
      # jump_attack_chance: percentage chance of a jump attack
      # dealt_collision_knocked_flying_threshold_multiplier: Multiplier for the collision speed delta threshold to apply to the victim of the collision
      # dealt_collision_knocked_down_threshold_multiplier: Multiplier for the collision speed delta threshold to apply to the victim of the collision
      # dealt_collision_knocked_back_threshold_multiplier: Multiplier for the collision speed delta threshold to apply to the victim of the collision
      # can_cast_projectile: does this entity cast a projectile spell

      if entity[battle_entities_keys["hit_reactions_ignore_chance"]] != "0":
        stats["hit_reactions_ignore"] = entity[battle_entities_keys["hit_reactions_ignore_chance"]] + "%"

      if entity[battle_entities_keys["knock_interrupts_ignore_chance"]] != "0":
        stats["knock_interrupts_ignore"] = entity[battle_entities_keys["knock_interrupts_ignore_chance"]] + "%"

      # officer entities, weapons and missiles - sometimes there's no primary weapon/missile, but officers have one and that's shown on the stat screen
      # example: ikit variant doomwheel
      # officers->land units officers tables, land_units_officers(additional_personalities) -> landland_units_additional_personalities_groups_junctions -> battle_personalities(battle_entity_stats, also battle_entity) -> battle_entity_stats
      # also land_units_officers(officers) -> battle_personalities(battle_entity_stats, also battle_entity) -> battle_entity_stats,
      if unit[units_keys['officers']] != "":
        officerrow = officers[unit[units_keys['officers']]]
        unitpersonalities = []
        if officerrow[officers_keys["officer_1"]] != "": # officer2 is deprecated
          unitpersonalities.append(officerrow[officers_keys["officer_1"]])
        if officerrow[officers_keys["additional_personalities"]] != "":
          additional = personality_group[officerrow[officers_keys["additional_personalities"]]]
          unitpersonalities.extend(additional)
      
      support_entities = []
      supportmeleeweapons = []
      meleeweaponsset = set()
      supportrangedweapons = []
      rangedeaponsset = set()

      if unit[units_keys['primary_melee_weapon']] != '':
          meleeweaponsset.add(unit[units_keys['primary_melee_weapon']])

      if unit[units_keys['primary_missile_weapon']] != '':
          rangedeaponsset.add(unit[units_keys['primary_missile_weapon']])

      if unit[units_keys['engine']] != "":
        if engine_weapon[unit[units_keys['engine']]] != "":
          rangedeaponsset.add(engine_weapon[unit[units_keys['engine']]])

      for personalityid in unitpersonalities:
        unitpersonality = personalities[personalityid]
        personalityentityid = unitpersonality[personalities_keys["battle_entity"]]
        if personalities_keys["autonomous_rider_hero"] != "true":
          # support entities (officers) which arent the autonomous rider entity count towards mass and health
          # they don't count towards speed
          support_entities.append(personalityentityid)
          num_men -= 1
        else:
          # main entities should always be the same as main entity and don't count towards mass/health
          if personalityentityid != unit[units_keys['man_entity']]:
            print("main entity conflict:" + personalityentityid)
          statid = unitpersonality[personalities_keys["battle_entity_stats"]]
          if statid != "":
            stats = bentity_stats[statid]
            # autonomous rider hero personalities sometimes have a weapon even if missing in land_unit_table (example: ikit claw doomwheel)
            meleeid = stats[bentity_stats_keys["primary_melee_weapon"]]
            if meleeid != "":
              meleeweaponsset.add(meleeid)
            missileid = stats[bentity_stats_keys["primary_missile_weapon"]]
            if missileid != "":
              rangedeaponsset.add(missileid)

      charge_speed = float(entity[battle_entities_keys["charge_speed"]]) * 10
      speed = float(entity[battle_entities_keys["run_speed"]]) * 10
      fly_speed = float(entity[battle_entities_keys["fly_speed"]]) * 10
      fly_charge_speed = float(entity[battle_entities_keys["flying_charge_speed"]]) * 10
      accel = float(entity[battle_entities_keys["acceleration"]])
      size = entity[battle_entities_keys["size"]]
      if unit[units_keys['engine']] != '':
          # speed characteristics are always overridden by engine and mount, even if engine is engine_mounted == false (example: catapult), verified by comparing stats
          engine = battle_entities[engine_entity[unit[units_keys['engine']]]]
          charge_speed = float(engine[battle_entities_keys["charge_speed"]]) * 10
          accel = float(engine[battle_entities_keys["acceleration"]])
          speed = float(engine[battle_entities_keys["run_speed"]]) * 10
          fly_speed = float(engine[battle_entities_keys["fly_speed"]]) * 10
          fly_charge_speed = float(engine[battle_entities_keys["flying_charge_speed"]]) * 10
          support_entities.append(engine_entity[unit[units_keys['engine']]])
          # only override size when engine is used as a mount (i.e. it's something you drive, not push), verified by comparing stats; overrides mount, verified by comparing stats
          if engine_mounted[unit[units_keys['engine']]]:
            size = engine[battle_entities_keys["size"]]
      if unit[units_keys['articulated_record']] != '': # never without an engine
        support_entities.append(articulated_entity[unit[units_keys['articulated_record']]])
      if unit[units_keys['mount']] != '':
          mount = battle_entities[mount_entity[unit[units_keys['mount']]]]
          # both engine and mount present - always chariots
          # verified, mount has higher priority than engine when it comes to determining speed (both increasing and decreasing), by comparing stats of units where speed of mount < or >  engine
          charge_speed = float(mount[battle_entities_keys["charge_speed"]]) * 10
          accel = float(mount[battle_entities_keys["acceleration"]])
          speed = float(mount[battle_entities_keys["run_speed"]]) * 10
          fly_speed = float(mount[battle_entities_keys["fly_speed"]]) * 10
          fly_charge_speed = float(mount[battle_entities_keys["flying_charge_speed"]]) * 10
          support_entities.append(mount_entity[unit[units_keys['mount']]])
          # verified that chariots use the size of the chariot, not the mount; skip overriding
          if not (unit[units_keys['engine']] != '' and engine_mounted[unit[units_keys['engine']]]):
            size = engine[battle_entities_keys["size"]]

      health = int(entity[battle_entities_keys["hit_points"]]) + int(unit[units_keys['bonus_hit_points']])
      mass = float(entity[battle_entities_keys["mass"]])

      for supportid in support_entities: 
        supportentity = battle_entities[supportid]
        mass += float(supportentity[battle_entities_keys["mass"]])
        health += int(supportentity[battle_entities_keys["hit_points"]])

      stats["health (ultra scale)"] = numstr(health)
      stats["mass"] = numstr(mass)
      targetsize = "nonlarge" if size == "small" else "large"
      stats["size"] = size + " ("+ targetsize + " target)"

      if len(meleeweaponsset) > 1:
        print("melee weapon conflict (land unit):" + unit[units_keys['key']])
      for meleeid in meleeweaponsset:
        unit_desc += meleeweapon_stats(meleeid)

      unit_desc += indentstr(indent) + "run_speed " + statstr(speed) + " charge " + statstr(charge_speed) + " acceleration " + statstr(accel*10) + endl
      if fly_speed != 0:
        unit_desc += indentstr(indent) + "fly_speed " + statstr(fly_speed) + " charge " + statstr(fly_charge_speed) + endl

      # land_unit -> ground_stat_effect_group -> ground_type_stat_effects
      if unit[units_keys['ground_stat_effect_group']] != "" and unit[units_keys['ground_stat_effect_group']] in ground_type_stats:
        ground_types = ground_type_stats[unit[units_keys['ground_stat_effect_group']]]
        
        unit_desc += "ground effects (can be cancelled by strider attr): " + endl
        for gtype in  ground_types:
          statdesc = gtype + ": "
          for statrow in ground_types[gtype]:
            statdesc += statrow[ground_type_stats_keys["affected_stat"]].replace("scalar_", "", 1).replace("stat_", "", 1) + " * " + statstr(statrow[ground_type_stats_keys["multiplier"]]) + " "
          unit_desc += indentstr(indent + 2) + statdesc + endl

      if unit[units_keys['armour']] != '':
          armourid = unit[units_keys['armour']]
          armourrow = armour[armourid]

      # ammo is number of full volleys (real ammo is num volleys * num people)
      if int(unit[units_keys['secondary_ammo']]) != 0:
        stats["secondary_ammo"] = unit[units_keys['secondary_ammo']]
      
      for stat in stats:
          unit_desc += statindent(stat, stats[stat], indent)

      if main_unit_entry[main_units_keys["unit"]] in missile_weapon_junctions:
        unit_desc += statstr("ranged_weapon_replacement_available_in_campaign [[img:ui/battle ui/ability_icons/ranged_weapon_stat.png]][[/img]]") + endl

      if len(rangedeaponsset) > 1:
        print("missile weapon conflict (land unit):" + unit[units_keys['key']])
      for missileweapon in rangedeaponsset:
        unit_desc += missileweapon_stats(missileweapon, unit, indent)

      for personalityid in unitpersonalities:
        unitpersonality = personalities[personalityid]
        statid = unitpersonality[personalities_keys["battle_entity_stats"]]
        if statid != "":
          stats = bentity_stats[statid]
          meleeid = stats[bentity_stats_keys["primary_melee_weapon"]]
          if meleeid != "" and meleeid not in meleeweaponsset:
            meleeweaponsset.add(meleeid)
            supportmeleeweapons.append(meleeid)

          missileid = stats[bentity_stats_keys["primary_missile_weapon"]]
          if missileid != "" and missileid not in rangedeaponsset:
            rangedeaponsset.add(missileid)
            supportrangedweapons.append(missileid)

      for meleeid in supportmeleeweapons:
        unit_desc += "melee_support:" + endl
        unit_desc += meleeweapon_stats(meleeid, 2)

      for missileid in supportrangedweapons:
        unit_desc += missileweapon_stats(missileid, None, 0, "ranged_support")

      spawn_info = unit_name[main_unit_entry[main_units_keys["land_unit"]]] + " (" + main_unit_entry[main_units_keys["caste"]] + ", tier " + main_unit_entry[main_units_keys["tier"]] + " men " + numstr(num_men) + ")"
      land_unit_to_spawn_info[main_unit_entry[main_units_keys["land_unit"]]] = spawn_info

      # store
      main_unit_id = main_unit_entry[main_units_keys["unit"]]
      new_bullet_id = main_unit_id + "_stats"
      new_bullet_enum = new_bullet_point_loc_prototype.copy()
      new_bullet_enum[new_bullet_point_enums_keys["key"]] = new_bullet_id
      new_bullet_enum[new_bullet_point_enums_keys["state"]] = "very_positive"
      new_bullet_enum[new_bullet_point_enums_keys["sort_order"]] = "0"
      new_bullet_point_enums.append(new_bullet_enum)
      new_override = new_bullet_point_override_prototype.copy()
      new_override[new_bullet_point_override_keys["unit_key"]] = main_unit_id
      new_override[new_bullet_point_override_keys["bullet_point"]] = new_bullet_id
      new_bullet_point_override.append(new_override)

      bullet_name_id  =  "ui_unit_bullet_point_enums_onscreen_name_" + new_bullet_id
      bullet_tooltip_id  =  "ui_unit_bullet_point_enums_tooltip_" + new_bullet_id

      bullet_point_name_loc = new_bullet_point_loc_prototype.copy()
      bullet_point_name_loc[bullet_points_loc_keys["key"]] = bullet_name_id
      bullet_point_name_loc[bullet_points_loc_keys["text"]] = "Hover for Base Stats"
      new_bullet_points_loc.append(bullet_point_name_loc)

      bullet_point_tooltip_loc = new_bullet_point_loc_prototype.copy()
      bullet_point_tooltip_loc[bullet_points_loc_keys["key"]] = bullet_tooltip_id
      bullet_point_tooltip_loc[bullet_points_loc_keys["text"]] = unit_desc
      new_bullet_points_loc.append(bullet_point_tooltip_loc)
        
tsv_file.close()

# new bullet point enum
with open('ui_unit_bullet_point_enums_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_bullet_point_enums:
      tsv_writer.writerow(row)

# new bullet point override
with open('ui_unit_bullet_point_unit_overrides_tables_data__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_bullet_point_override:
      tsv_writer.writerow(row)

# new bullet point descriptions
with open('ui_unit_bullet_point_enums__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_bullet_points_loc:
      tsv_writer.writerow(row)

## todo: optionally write a smaller version to unit description?

# ability phases
tsv_file = opendbread("special_ability_to_special_ability_phase_junctions_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
ability_phases = {}

rowid = 0
ability_phases_keys = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        ability_phases_keys[key] = i
        i = i + 1
  if rowid > 2:
    key = row[ability_phases_keys["special_ability"]]
    if key not in ability_phases:
      ability_phases[key] = []
    ability_phases[key].append(row[ability_phases_keys["phase"]])

tsv_file.close()

# battle vortexs - done
# duration
# damage/damage_ap
# expansion_speed
# start_radius
# goal_radius
# movement_speed - in metres / second
# move_change_freq
# change_max_angle
# contact_effect -> special_ability_phases
# height_off_ground
# infinite_height
# ignition_amount
# is_magical
# detonation_force
# launch_source -> battle vortex_launch_sources
# delay: We do spawn this at the same time as usual, but we wait this time to cause damage / move / collide etc.
# num_vortexes - num of vortexes spawned
# affects_allies
# launch_source_offset- distance from launch_source
# delay_between_vortexes
tsv_file = opendbread("battle_vortexs_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
vortexs = {}

rowid = 0
vortexs_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        vortexs_key[key] = i
        i = i + 1
  if rowid > 2:
      vortexs[row[vortexs_key["vortex_key"]]] = row
tsv_file.close()

# projectile bombardment - done
# num_projectiles The total number of projectiles that will spawn. Their arrival times are random, within the times specified
# start_time the minimum time (seconds) that must pass before a projectile can appear
# arrival_window The time (seconds) duration that any of the projectiles can appear
# radius_spread How far away from the target this can theoretically land
# launch_source The suggested starting location of the bombardment
# launch_height_(underground)
tsv_file = opendbread("projectile_bombardments_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
bombardments = {}

rowid = 0
bombardments_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        bombardments_key[key] = i
        i = i + 1
  if rowid > 2:
      bombardments[row[bombardments_key["bombardment_key"]]] = row
tsv_file.close()

# ability descriptions
rowid = 0
for row in new_ability_loc:
  rowid = rowid + 1
  if rowid > 2 and "unit_abilities_tooltip_text_" in row[ability_descriptions_keys["key"]]:
      newrow = row
      descid =  newrow[ability_descriptions_keys["key"]].replace("unit_abilities_tooltip_text_", "", 1)
      result = "\\\\n\\\\n"

      if descid in ability_details:
        ability = ability_details[descid]

        if ability[ability_details_key["passive"]] == "false":
          result += statindent("cast_time", ability[ability_details_key["wind_up_time"]], 0)
          result += statindent("active_time", ability[ability_details_key["active_time"]], 0)
          initial_recharge = ""
          if (float(ability[ability_details_key["initial_recharge"]]) > 0): 
            initial_recharge = ", initial " + ability[ability_details_key["initial_recharge"]]
          result += statindent("recharge_time", ability[ability_details_key["recharge_time"]] + initial_recharge, 0)
          if float(ability[ability_details_key["min_range"]]) > 0:
            result += statindent("min_range", ability[ability_details_key["min_range"]] + initial_recharge, 0)

        if int(ability[ability_details_key["num_effected_friendly_units"]]) > 0:
          result += statindent("affected_friendly_units", ability[ability_details_key["num_effected_friendly_units"]], 0)
        if int(ability[ability_details_key["num_effected_enemy_units"]]) > 0:
          result += statindent("affected_enemy_units", ability[ability_details_key["num_effected_enemy_units"]], 0)
        if ability[ability_details_key["only_affect_owned_units"]] == "true":
          result += statindent("only_affect_owned_units", ability[ability_details_key["only_affect_owned_units"]], 0)
        if ability[ability_details_key["update_targets_every_frame"]] == "true":
          result += statindent("update_targets_every_frame", ability[ability_details_key["update_targets_every_frame"]], 0)

        if ability[ability_details_key["assume_specific_behaviour"]]:
          result += statindent("behaviour", ability[ability_details_key["assume_specific_behaviour"]], 0)
        
        if ability[ability_details_key["bombardment"]] != "":
          bombardment = bombardments[ability[ability_details_key["bombardment"]]]
          result += "Bombardment:\\\\n"
          result += statindent("num_bombs", bombardment[bombardments_key["num_projectiles"]],2)
          result += statindent("radius_spread", bombardment[bombardments_key["radius_spread"]],2)
          result += statindent("launch_source", bombardment[bombardments_key["launch_source"]],2)
          result += statindent("launch_height", bombardment[bombardments_key["launch_height"]],2)
          result += statindent("start_time", bombardment[bombardments_key["start_time"]],2)
          result += statindent("arrival_window", bombardment[bombardments_key["arrival_window"]],2)
          bomb_projectile = projectiles[bombardment[bombardments_key["projectile_type"]]]
          result += missile_stats(bomb_projectile, None, "", 2)
          result += "\\\\n"
        if ability[ability_details_key["activated_projectile"]] != "":
          result += "Projectile:"
          projectile = projectiles[ability[ability_details_key["activated_projectile"]]]
          result += missile_stats(projectile, None, "", 2)
          result += "\\\\n"
        if ability[ability_details_key["vortex"]] != "":
          result += "Vortex: \\\\n"
          indent = 2
          vortex = vortexs[ability[ability_details_key['vortex']]]
          if vortex[vortexs_key['num_vortexes']] != "1":
            result += indentstr(indent) + " vortex count: " + statstr(vortex[vortexs_key['num_vortexes']]) + " vortexes " + statstr(vortex[vortexs_key['delay_between_vortexes']]) + "s delay inbetween" + endl
          radius = ""
          if vortex[vortexs_key['start_radius']] == vortex[vortexs_key['goal_radius']]:
            radius = statstr(vortex[vortexs_key['start_radius']])
          else:
            radius = "start " + statstr(vortex[vortexs_key['start_radius']]) + " goal " +  statstr(vortex[vortexs_key['goal_radius']]) + " expansion speed " +  statstr(vortex[vortexs_key['expansion_speed']])
          result += indentstr(indent) + "radius: " + radius + endl
          result += indentstr(indent) + damage_stat(vortex[vortexs_key['damage']], vortex[vortexs_key['damage_ap']], vortex[vortexs_key['ignition_amount']], vortex[vortexs_key['is_magical']]) + endl
          result += statindent("detonation_force", vortex[vortexs_key['detonation_force']], indent)
          result += statindent("initial_delay", vortex[vortexs_key['delay']], indent)
          result += statindent("duration", vortex[vortexs_key['duration']], indent)
          if vortex[vortexs_key['building_collision']] == "2.expire":
            result += indentstr(indent) + statstr("building colision expires vortex") + endl
          result += statindent("launch_source", vortex[vortexs_key['launch_source']], indent)
          if vortex[vortexs_key['launch_source_offset']] != "0.0":
            result += statindent("launch_source_offset", vortex[vortexs_key['launch_source_offset']], indent)
          if float(vortex[vortexs_key['movement_speed']]) == 0:
            path = "stationary"
          elif vortex[vortexs_key['change_max_angle']] == "0":
            path = "straight line, speed " + statstr(vortex[vortexs_key['movement_speed']])
          else:
            path = "angle changes by " + statstr("0-"+numstr(vortex[vortexs_key['change_max_angle']])) + " every " + statstr(vortex[vortexs_key['move_change_freq']]) + ", speed " + statstr(vortex[vortexs_key['movement_speed']])
          result += indentstr(indent) +  "path: " + path + endl
          if vortex[vortexs_key['affects_allies']] == "false":
            result += posstr("doesn't_affect_allies", indent) + endl
          if vortex[vortexs_key["contact_effect"]] != "":
            result += ability_phase_details_stats(phaseid, indent, "contact effect")
        if ability[ability_details_key["spawned_unit"]] != "":
          result += "Spawn: "
          if ability[ability_details_key["spawn_is_decoy"]] == "true":
            result += "(decoy) "
          if ability[ability_details_key["spawn_is_transformation"]] == "true":
            result += "(transform) "
          result += land_unit_to_spawn_info[ability[ability_details_key['spawned_unit']]]
          result += endl
        if ability[ability_details_key["miscast_explosion"]] != "":
          result += "Miscast explosion (chance:" + statstr(float(ability[ability_details_key["miscast_chance"]]) * 100) + "%):"
          explosionrow = projectiles_explosions[ability[ability_details_key['miscast_explosion']]]
          result += explosion_stats(explosionrow, 2)
          result += endl
      if descid in ability_phases:
          result += "Phases:\\\\n"
          phases = ability_phases[descid]
          i = 0
          for phaseid in phases:
            i = i + 1
            result += ability_phase_details_stats(phaseid, 2, numstr(i) + ".")


      newrow[ability_descriptions_keys["text"]] = newrow[ability_descriptions_keys["text"]] + result 
      new_ability_loc[rowid - 1] = newrow

# new unit_abilities loc entries
with open('unit_abilities__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    for row in new_ability_loc:
      tsv_writer.writerow(row)
    for row in additional_ability_loc:
      tsv_writer.writerow(row)

tsv_file = opendbread("_kv_rules_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
kv_rules = {}
rowid = 0
kv_rules_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        kv_rules_key[key] = i
        i = i + 1
  if rowid > 2:
      kv_rules[row[kv_rules_key["key"]]] = row[kv_rules_key["value"]]
tsv_file.close()

tsv_file = opendbread("_kv_fatigue_tables")

read_tsv = csv.reader(tsv_file, delimiter="\t")
kv_fatigue = {}
rowid = 0
kv_fatigue_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        kv_fatigue_key[key] = i
        i = i + 1
  if rowid > 2:
      kv_fatigue[row[kv_fatigue_key["key"]]] = row[kv_fatigue_key["value"]]
tsv_file.close()

tsv_file = opendbread("_kv_morale_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
kv_morale = {}
rowid = 0
kv_morale_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        kv_morale_key[key] = i
        i = i + 1
  if rowid > 2:
      kv_morale[row[kv_morale_key["key"]]] = row[kv_morale_key["value"]]
tsv_file.close()

fatigue_order = ["active", "winded", "tired", "very_tired", "exhausted"]

tsv_file = opendbread("unit_fatigue_effects_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
fatigue_effects = {}
rowid = 0
fatigue_effects_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        fatigue_effects_key[key] = i
        i = i + 1
  if rowid > 2:
    key = row[fatigue_effects_key["fatigue_level"]].replace("threshold_", "", 1)
    stat = row[fatigue_effects_key["stat"]].replace("scalar_", "", 1).replace("stat_", "", 1)
    if key not in fatigue_effects:
      fatigue_effects[key] = {}
    fatigue_effects[key][stat] = row[fatigue_effects_key["value"]]
tsv_file.close()

prev_level = {}
for fatigue_level in fatigue_order:
  for stat in prev_level:
    if stat not in fatigue_effects[fatigue_level]:
      fatigue_effects[fatigue_level][stat] = prev_level[stat]
  prev_level = fatigue_effects[fatigue_level]

tsv_file = opendbread("unit_experience_bonuses_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
xp_bonuses = {}
rowid = 0
xp_bonuses_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        xp_bonuses_key[key] = i
        i = i + 1
  if rowid > 2:
    key = row[xp_bonuses_key["stat"]].replace("stat_", "", 1)
    xp_bonuses[key] = row
tsv_file.close()

tsv_file = opendbread("unit_stats_land_experience_bonuses_tables")
read_tsv = csv.reader(tsv_file, delimiter="\t")
rank_bonuses = {}
rowid = 0
unit_stats_land_experience_bonuses_tables_key = {}
for row in read_tsv:
  rowid = rowid + 1
  i = 0
  if rowid == 2:
      for key in row:
        unit_stats_land_experience_bonuses_tables_key[key] = i
        i = i + 1
  if rowid > 2:
    key = row[unit_stats_land_experience_bonuses_tables_key["xp_level"]]
    #rank_fatigue_bonus[key] = row[unit_stats_land_experience_bonuses_tables_key["fatigue"]]
    result = {}
    rank = int(key)
    result["fatigue"] = statstr(row[unit_stats_land_experience_bonuses_tables_key["fatigue"]])
    for bonus_stat in xp_bonuses:
      stat_row = xp_bonuses[bonus_stat]
      growth_rate = float(stat_row[xp_bonuses_key["growth_rate"]])
      growth_scalar = float(stat_row[xp_bonuses_key["growth_scalar"]])
      if growth_rate == 0:
        # verified in game that the stats are using math rounding to integer for exp bonuses
        result[bonus_stat] = statstr(round(growth_scalar * rank))
      else: #"base"+"^" + statstr(growth_rate) + "*" + statstr(growth_scalar * rank)
        result[bonus_stat] = statstr(round((30.0 ** growth_rate) * growth_scalar * rank)) + " " + statstr(round((60.0 ** growth_rate) * growth_scalar * rank))
    rank_bonuses[key] = result
tsv_file.close()


# stat descriptions
tsv_file = openlocread("unit_stat_localisations")
read_tsv = csv.reader(tsv_file, delimiter="\t")
unit_stat_localisations_keys = {}
with open('unit_stat_localisations__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    rowid = 0
    for row in read_tsv:
        rowid = rowid + 1
        i = 0
        if rowid == 2:
            for key in row:
                unit_stat_localisations_keys[key] = i
                i = i + 1
        if rowid > 2:
            newrow = row
            newtext = ""
            key = row[unit_stat_localisations_keys["key"]]
            stats = {}
            if key == "unit_stat_localisations_tooltip_text_stat_melee_attack":
              newtext += "|| ||Melee hit pct chance formula: " + statstr(kv_rules["melee_hit_chance_base"]) + " + melee_attack - enemy_melee_def, clamp (min: " + statstr(kv_rules["melee_hit_chance_min"]) + " max: " + statstr(kv_rules["melee_hit_chance_max"])  + ")" 
            if key == "unit_stat_localisations_tooltip_text_stat_melee_defence":
              stats["melee_defence_direction_penalty_coefficient_flank"] = kv_rules["melee_defence_direction_penalty_coefficient_flank"]
              stats["melee_defence_direction_penalty_coefficient_rear"] = kv_rules["melee_defence_direction_penalty_coefficient_rear"]
            if key == "unit_stat_localisations_tooltip_text_stat_armour":
              newtext += "|| ||Armour non-ap-dmg-reduction formula: rand(" + statstr(kv_rules["armour_roll_lower_cap"]) + ",1) * armour"
            if key == "unit_stat_localisations_tooltip_text_stat_weapon_damage":
              newtext += "|| Terrain height difference dmg mod max: +/-" + statstr(float(kv_rules["melee_height_damage_modifier_max_coefficient"]) * 100) + "% at diff of +/- " + statstr(kv_rules["melee_height_damage_modifier_max_difference"]) + "m, linearly decreasing to 0"
            if key == "unit_stat_localisations_tooltip_text_stat_charge_bonus":
              newtext += "|| ||Charge bonus lasts for " + statstr(kv_rules["charge_cool_down_time"] + "s") + " after first contact, linearly going down to 0. ||"
              newtext += "Charge bonus is added to melee_attack and weapon_damage. Weapon_damage increase is split between ap and base dmg using the ap/base dmg ratio before the bonus.||"
              newtext += "All attacks on routed units are using charge bonus *" + statstr(kv_rules["pursuit_charge_bonus_modifier"]) + "||"
              newtext += " || Bracing: ||"
              newtext += indentstr(2) + "bracing is a multiplier (clamped to " +statstr(kv_rules["bracing_max_multiplier_clamp"]) + ") to the mass of the charged unit for comparison vs a charging one||"
              newtext += indentstr(2) + "to brace the unit must stand still in formation (exact time to get in formation varies) and not attack/fire||" 
              newtext += indentstr(2) + "bracing will only apply for attacks coming from the front at max " + statstr(kv_rules["bracing_attack_angle"]) + "* half-angle||"              
              newtext += indentstr(2) + "bracing from ranks: 1: " + statstr(1.0) + " ranks 2-" + statstr(kv_rules["bracing_calibration_ranks"]) + " add " + statstr((float(kv_rules["bracing_calibration_ranks_multiplier"]) - 1) / (float(kv_rules["bracing_calibration_ranks"])  - 1)) + "||"
            if key == "unit_stat_localisations_tooltip_text_stat_missile_strength":
              newtext += "|| Terrain height difference dmg mod max: +/-" + statstr(float(kv_rules["missile_height_damage_modifier_max_coefficient"]) * 100) + "% at diff of +/- " + kv_rules["missile_height_damage_modifier_max_difference"] + "m, linearly decreasing to 0||"
            if key == "unit_stat_localisations_tooltip_text_scalar_missile_range":
              newtext += "|| ||Hit chance when shooting targets hiding in forests/scrub:" + statstr((1 - float(kv_rules["missile_target_in_cover_penalty"]))  * 100) + '||'
              newtext += "Friendly fire uses bigger hitboxes than enemy fire: height *= " + statstr(kv_rules["projectile_friendly_fire_man_height_coefficient"]) + " radius *= " + statstr(kv_rules["projectile_friendly_fire_man_radius_coefficient"]) + "||" 
              newtext += "Units with " + statstr("dual") + " trajectory will switch their aim to high if "+ statstr(float(kv_rules["unit_firing_line_of_sight_considered_obstructed_ratio"]) * 100) + "% of LOS is obstructed ||"
              newtext += "Projectiles with high velocity and low aim are much better at hitting moving enemies."
              # todo: things like missile penetration, lethality seem to contradict other stat descriptions but don't seem obsolete as they weren't there in shogun2
              # need to do more testing before adding them in
            if key == "unit_stat_localisations_tooltip_text_scalar_speed":
              newtext += "|| || Fatigue effects: ||"
              for fatigue_level in fatigue_order:
                newtext += fatigue_level + ": "
                for stat in fatigue_effects[fatigue_level]:
                  newtext += " " + stat_icon[stat] + "" + statstr(float(fatigue_effects[fatigue_level][stat]) * 100) + "%"
                newtext += "||"
              newtext += " || Tiring/Resting: ||"
              kvfatiguevals = ["charging", "climbing_ladders", "combat", "gradient_shallow_movement_multiplier", "gradient_steep_movement_multiplier", "gradient_very_steep_movement_multiplier",
              "idle", "limbering", "ready", "running", "running_cavalry", "running_artillery_horse", "shooting", "walking", "walking_artillery", "walking_horse_artillery"]
              for kvfatval in kvfatiguevals:
                newtext += kvfatval + " " + negmodstr(kv_fatigue[kvfatval]) + "||"
            
            if key == "unit_stat_localisations_tooltip_text_stat_morale":
              moraletext = "Leadership mechanics: ||"
              moraletext += "total_hp_loss:" + "||"
              moraletext += indentstr(2) + " 10%:" + modstr(kv_morale["total_casualties_penalty_10"]) + " 20%:" + modstr(kv_morale["total_casualties_penalty_20"]) + " 30%:" + modstr(kv_morale["total_casualties_penalty_30"]) + " 40%:" + modstr(kv_morale["total_casualties_penalty_40"]) + "||"
              moraletext += indentstr(2) + " 50%:" + modstr(kv_morale["total_casualties_penalty_50"]) + " 60%:" + modstr(kv_morale["total_casualties_penalty_60"]) + " 70%:" + modstr(kv_morale["total_casualties_penalty_70"]) + " 80%:" + modstr(kv_morale["total_casualties_penalty_80"]) + " 90%:" + modstr(kv_morale["total_casualties_penalty_90"]) + "||"
              moraletext += "60s_hp_loss:" + " 10%:" + modstr(kv_morale["extended_casualties_penalty_10"]) + " 15%:" + modstr(kv_morale["extended_casualties_penalty_15"]) + " 33%:" + modstr(kv_morale["extended_casualties_penalty_33"])  + " 50%:" + modstr(kv_morale["extended_casualties_penalty_50"])  + " 80%:" + modstr(kv_morale["extended_casualties_penalty_80"]) + "||"
              moraletext += "4s_hp_loss:" + " 6%:" + modstr(kv_morale["recent_casualties_penalty_6"]) + " 10%:" + modstr(kv_morale["recent_casualties_penalty_10"]) + " 15%:" + modstr(kv_morale["recent_casualties_penalty_15"]) + " 33%:" + modstr(kv_morale["recent_casualties_penalty_33"]) + " 50%:" + modstr(kv_morale["recent_casualties_penalty_50"]) + "||"
              moraletext += "winning combat:" + " " + modstr(kv_morale["winning_combat"]) + " significantly " + modstr(kv_morale["winning_combat_significantly"])   +  " slightly " + modstr(kv_morale["winning_combat_slightly"]) +"||"
              moraletext += "losing combat:" + " " + modstr(kv_morale["losing_combat"]) + " significantly " + modstr(kv_morale["losing_combat_significantly"]) + "||"
              moraletext += "charging: " + modstr(kv_morale["charge_bonus"]) + " timeout " + statstr(float(kv_morale["charge_timeout"]) / 10) +"s||"
              moraletext += "attacked in the flank " + modstr(kv_morale["was_attacked_in_flank"]) +"||"
              moraletext += "attacked in the rear " + modstr(kv_morale["was_attacked_in_rear"]) +"||"
              moraletext += "high ground vs all enemies " + modstr(kv_morale["ume_encouraged_on_the_hill"]) + "||"
              moraletext += "defending walled nonbreached settlement " + modstr(kv_morale["ume_encouraged_fortification"]) + "||"
              moraletext += "defending on a plaza " + modstr(kv_morale["ume_encouraged_settlement_plaza"]) + "||"
              moraletext += "artillery:" + " hit " + modstr(kv_morale["ume_concerned_damaged_by_artillery"]) + " near miss (<="+ statstr(math.sqrt(float(kv_morale["artillery_near_miss_distance_squared"])))+") " + modstr(kv_morale["ume_concerned_attacked_by_artillery"]) + "||"
              moraletext += "projectile hit" + modstr(kv_morale["ume_concerned_attacked_by_projectile"]) + "||"
              moraletext += "vigor: " + colstr("very_tired ", "fatigue_very_tired") + " " + modstr(kv_morale["ume_concerned_very_tired"])  + colstr(" exhausted ", "fatigue_exhausted") + modstr(kv_morale["ume_concerned_exhausted"]) + '||'
              moraletext += "army loses: " + modstr(kv_morale["ume_concerned_army_destruction"]) + " power lost: " + statstr((1 - float(kv_morale["army_destruction_alliance_strength_ratio"])) * 100) + "% and balance is " + statstr((1.0 / float(kv_morale["army_destruction_enemy_strength_ratio"])) * 100) + '%||'
              moraletext += "general's death: " +  modstr(kv_morale["ume_concerned_general_dead"]) + " recently(60s?) " + modstr(kv_morale["ume_concerned_general_died_recently"]) + "||"
              moraletext += "surprise enemy discovery: " +  modstr(kv_morale["ume_concerned_surprised"]) + " timeout " + statstr(float(kv_morale["surprise_timeout"]) / 10) +"s||"
              moraletext += "flanks: " + "secure " + modstr(kv_morale["ume_encouraged_flanks_secure"]) + " 1_exposed " + modstr(kv_morale["ume_concerned_flanks_exposed_single"]) + " 2_exposed " + modstr(kv_morale["ume_concerned_flanks_exposed_multiple"]) + " range " + statstr(kv_morale["open_flanks_effect_range"]) + 'm||'
              moraletext += "routing balance: (" + statstr(kv_morale["routing_unit_effect_distance_flank"]) + "m in front/flanks)" + "||" 
              moraletext += indentstr(2) + " (allies-enemies, clamp " + negstr(kv_morale["max_routing_friends_to_consider"]) + ")*" + negstr(kv_morale["routing_friends_effect_weighting"]) + " (enemies-allies, clamp " + posstr(kv_morale["max_routing_enemies_to_consider"]) + ")*" + posstr(kv_morale["routing_enemies_effect_weighting"])+ '||'
              moraletext += "outmatched by enemies: (" + negstr("-1") + " - " + negstr("-7") + ") * " + statstr(kv_morale["enemy_numbers_morale_penalty_multiplier"]) + " range " +  statstr(kv_morale["enemy_effect_range"]) + 'm||'
              moraletext += "wavering:" + " " + statstr(kv_morale["ums_wavering_threshold_lower"])  + "-" + statstr(kv_morale["ums_wavering_threshold_upper"]) + "||"
              moraletext += indentstr(2) + "must spend " + statstr(float(kv_morale["waver_base_timeout"]) / 10)  + "s wavering before routing||"
              moraletext += "broken:" + " " + statstr(kv_morale["ums_broken_threshold_lower"]) + "-" + statstr(kv_morale["ums_broken_threshold_upper"]) + "||"
              moraletext += indentstr(2) + "can rally after " + statstr(float(kv_morale["broken_finish_base_timeout"]) / 10) + "s - level * " + statstr(float(kv_morale["broken_finish_timer_experience_bonus"]) / 10) + "s||"
              moraletext += indentstr(2) + "immune to rout for " + statstr(float(kv_morale["post_rally_no_rout_timer"])) + "s after rallying" + "||"
              moraletext += indentstr(2) + "won't rally if enemies within? "  + statstr(kv_morale["enemy_effect_range"]) + "m" + "||"
              moraletext += indentstr(2) + "max rally count before shattered "  + statstr(float(kv_morale["shatter_after_rout_count"]) - 1) + "||"
              moraletext += indentstr(2) + "1st rout shatters units with "  + statstr((1-float(kv_morale["shatter_after_first_rout_if_casulties_higher_than"])) * 100 )  + "% hp loss" + "||"
              moraletext += indentstr(2) + "2nd rout shatters units with "  + statstr((1-float(kv_morale["shatter_after_second_rout_if_casulties_higher_than"])) * 100 )  + "% hp loss" + "||"
              moraletext += "shock-rout: last 4s hp loss >=" + statstr(kv_morale["recent_casualties_shock_threshold"]) + "% and morale < 0"
              newrow[unit_stat_localisations_keys["text"]] = moraletext
            
            # todo: more kv_rules values: missile, collision, etc
            for s in stats:
              newtext += "||" + s + ": " + statstr(stats[s])
            newrow[unit_stat_localisations_keys["text"]] += newtext

            tsv_writer.writerow(newrow)
        else:
            tsv_writer.writerow(row)
tsv_file.close()

# attr descriptions
tsv_file = openlocread("unit_attributes")
read_tsv = csv.reader(tsv_file, delimiter="\t")
unit_attributes_loc_keys = {}
with open('unit_attributes__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    rowid = 0
    for row in read_tsv:
        rowid = rowid + 1
        i = 0
        if rowid == 2:
            for key in row:
                unit_attributes_loc_keys[key] = i
                i = i + 1
        if rowid > 2:
            newrow = row
            newtext = ""
            key = row[unit_attributes_loc_keys["key"]]
            stat = {}
            if key == "unit_attributes_bullet_text_causes_fear":
              newtext += "||fear aura " + modstr(kv_morale["ume_concerned_unit_frightened"]) + " range " + statstr(kv_morale["general_aura_radius"]) +""
            if key == "unit_attributes_bullet_text_causes_terror":
              newtext += "||terror " + "enemy leadership <= " + statstr(kv_morale["morale_shock_terror_morale_threshold_long"]) + " in range " + statstr(kv_morale["terror_effect_range"]) + " instant-shock-routes enemy for " + statstr(kv_morale["morale_shock_rout_timer_long"]) + "s||"
              newtext += "next terror immunity lasts for " + statstr(kv_morale["morale_shock_rout_immunity_timer"]) + "s"
            if key == "unit_attributes_bullet_text_encourages":
              newtext += "||encourage aura " + " full effect range " + statstr(kv_morale["general_aura_radius"]) + "m linear drop to 0 at " + statstr(float(kv_morale["general_aura_radius"]) * float(kv_morale["inspiration_radius_max_effect_range_modifier"])) +  "m||"
              newtext += "general's effect in full effect range " + modstr(kv_morale["general_inspire_effect_amount_min"]) + "||"
              newtext += "encourage unit's effect in full effect range " + modstr(kv_morale["unit_inspire_effect_amount"]) 
            if key == "unit_attributes_bullet_text_strider":
              newtext += "||this includes speed decrease from uphill slope, melee and missile dmg reduction from being downhill, ground_stat_type, fatigue penalties from terrain, etc."
            for s in stat:
              newtext += "||" + s + ": " + statstr(stat[s])
            newrow[unit_attributes_loc_keys["text"]] += newtext

            tsv_writer.writerow(newrow)
        else:
            tsv_writer.writerow(row)
tsv_file.close()

# misc strings
tsv_file = openlocread("random_localisation_strings")
read_tsv = csv.reader(tsv_file, delimiter="\t")
random_localisation_strings_keys = {}
with open('random_localisation_strings__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    rowid = 0
    for row in read_tsv:
        rowid = rowid + 1
        i = 0
        if rowid == 2:
            for key in row:
                unit_attributes_loc_keys[key] = i
                i = i + 1
        if rowid > 2:
            newrow = row
            newtext = ""
            key = row[unit_attributes_loc_keys["key"]]
            stat = {}

            if key == "random_localisation_strings_string_modifier_icon_tooltip_shield":
              newtext += "|| Shields only block projectiles from the front at max "+ statstr(kv_rules["shield_defence_angle_missile"]) + "* half-angle"
            if "random_localisation_strings_string_fatigue" in key:
              for fatigue_level in fatigue_order:
                if ("fatigue_" + fatigue_level) not in key:
                  continue
                for stat in fatigue_effects[fatigue_level]:
                  newtext += " " + stat_icon[stat] + " " + statstr(float(fatigue_effects[fatigue_level][stat]) * 100) + "%"
            newrow[unit_attributes_loc_keys["text"]] += newtext
            tsv_writer.writerow(newrow)
        else:
            tsv_writer.writerow(row)
tsv_file.close()

# misc strings
tsv_file = openlocread("uied_component_texts")
read_tsv = csv.reader(tsv_file, delimiter="\t")
uied_component_texts_keys = {}
with open('uied_component_texts__.tsv', 'w', newline='', encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
    rowid = 0
    for row in read_tsv:
        rowid = rowid + 1
        i = 0
        if rowid == 2:
            for key in row:
                uied_component_texts_keys[key] = i
                i = i + 1
        if rowid > 2:
            newrow = row
            newtext = ""
            key = row[uied_component_texts_keys["key"]]
            stat = {}

            if key == "uied_component_texts_localised_string_experience_tx_Tooltip_5c0016":
              newtext += "|| XP rank bonuses (melee attack and defence list values for base 30 and 60 as their bonus depends on the base value of the stat): ||"
              for rank in range(1, 10):
                newtext += rank_icon(rank)
                stats = rank_bonuses[str(rank)]
                for stat in stats:
                  newtext += stat_icon[stat] + " " + stats[stat] + " "
                newtext += "||"
            newrow[unit_attributes_loc_keys["text"]] += newtext
            tsv_writer.writerow(newrow)
        else:
            tsv_writer.writerow(row)
tsv_file.close()

#there's a dynamic accuracy stat that could be displayed on the unit panel, but it's overlapped by attributes and doesn't seem useful (doesn't include marksmanship bonus)